import mysql.connector
import pandas as pd

# 数据库连接参数
db_params = {
    "host": "localhost",
    "user": "chengcheng",
    "password": "171612cgj",
    "database": "db"
}

# 连接数据库
db = mysql.connector.connect(**db_params)
cursor = db.cursor()

# 执行查询，获取change_category的频率
query = "SELECT change_category, COUNT(*) AS count FROM git_log GROUP BY change_category"
cursor.execute(query)
data = cursor.fetchall()

# 将数据转换为DataFrame
df_category_counts = pd.DataFrame(data, columns=['change_category', 'count'])

# 关闭游标和数据库连接
cursor.close()
db.close()

# 映射change_category到具体的含义
category_mapping = {0: 'Bug Fix', 1: 'Feature Addition', 2: 'Version Maintenance', 3: 'Others'}
df_category_counts['change_category'] = df_category_counts['change_category'].map(category_mapping)

# 展示DataFrame
print(df_category_counts)



import matplotlib.pyplot as plt
import seaborn as sns

# 绘制条形图
plt.figure(figsize=(10, 6))
sns.barplot(x='change_category', y='count', data=df_category_counts)
plt.xlabel('Change Category')
plt.ylabel('Count')
plt.title('Distribution of Change Categories')
plt.xticks(rotation=45)
plt.show()
