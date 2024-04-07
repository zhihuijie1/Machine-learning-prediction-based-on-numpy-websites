import mysql.connector
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

from featureEnginng import df, tfidf_df

# 假设 vectorizer 和 df 已经定义且处理完毕

# 数据库连接参数
db_params = {
    "host": "localhost",
    "user": "chengcheng",
    "password": "171612cgj",
    "database": "db",
    "port": 3306
}

# 连接数据库
db = mysql.connector.connect(**db_params)
cursor = db.cursor()

# 检查数据库中 change_category 为 NULL 的记录数量
cursor.execute("SELECT COUNT(*) FROM git_log WHERE change_category IS NULL")
unlabeled_count = cursor.fetchone()[0]
print(f"未标注的数据数量：{unlabeled_count}")

if unlabeled_count > 0:
    # 分割已标注和未标注数据
    df_train = df[df['change_category'] != -1].copy()  # 假设之前已经填充了-1
    df_predict = df[df['change_category'] == -1].copy()

    # 使用特征工程的结果
    X_train = tfidf_df.loc[df_train.index].to_numpy()
    y_train = df_train['change_category'].astype(int)

    # 训练模型
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    if not df_predict.empty:
        X_predict = tfidf_df.loc[df_predict.index].to_numpy()
        y_predict = classifier.predict(X_predict)

        # 更新数据库
        cursor = db.cursor()
        for index, prediction in zip(df_predict.index, y_predict):
            update_query = "UPDATE git_log SET change_category = %s WHERE id = %s"
            # 使用int()确保prediction和ID是标准Python整型
            cursor.execute(update_query, (int(prediction), int(df_predict.loc[index, 'id'])))
        db.commit()
        print("Database updated with predicted categories.")

    else:
        print("No data to predict after re-check.")
else:
    print("数据库中没有未标注的数据进行预测。")

cursor.close()
db.close()