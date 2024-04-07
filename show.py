# ----------------------------------------------------------活跃的变更者

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

# 执行查询，获取每个作者的变更次数
query = "SELECT author, COUNT(*) as changes FROM git_log GROUP BY author"
cursor.execute(query)
data = cursor.fetchall()

# 将数据转换为DataFrame
df_changes = pd.DataFrame(data, columns=['committer', 'changes'])

# 关闭游标和数据库连接
cursor.close()
db.close()

# 展示DataFrame
print(df_changes.head())


import matplotlib.pyplot as plt
import seaborn as sns

# 缩短名字：只取前10个字符
df_changes['committer_short'] = df_changes['committer'].apply(lambda x: x[:10] + '...' if len(x) > 10 else x)

plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='committer', y='changes', data=df_changes.sort_values(by='changes', ascending=False))
plt.xlabel('Committer')
plt.ylabel('Number of Changes')
plt.title('Activity of Committers')
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()


