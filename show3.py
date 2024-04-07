# ----------------------------  软件更新的重大节点

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

# 执行查询，获取每个日期的变更次数
query = "SELECT date, COUNT(*) AS changes FROM git_log GROUP BY date ORDER BY date"
cursor.execute(query)
data = cursor.fetchall()

# 将数据转换为DataFrame
df_time = pd.DataFrame(data, columns=['date', 'changes'])

# 关闭游标和数据库连接
cursor.close()
db.close()

# 展示DataFrame
print(df_time.head())


import matplotlib.pyplot as plt

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(df_time['date'], df_time['changes'], marker='o', linestyle='-')
plt.xlabel('Date')
plt.ylabel('Number of Changes')
plt.title('Major Changes Over Time')
plt.show()
