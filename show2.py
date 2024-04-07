# ----------------------------------------------------频繁变更的文件的热图

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

# 执行查询，这里获取所有记录的 changed_files 字段
# 注意：我们这里假设每条记录的 changed_files 字段可能包含由逗号分隔的多个文件名
query = "SELECT changed_files FROM git_log"
cursor.execute(query)
data = cursor.fetchall()

# 初始化一个空的字典来存储每个文件的变更次数
file_changes = {}

# 遍历数据，分割 `changed_files` 字段，并更新计数
# 注意：这里假设每个记录的changed_files字段是第0个元素
for record in data:
    # 分割每条记录的 changed_files 字段
    if record[0]:  # 确保字段不是 None
        files = record[0].split(',')  # 假设文件名之间是用逗号分隔的
        for file in files:
            file = file.strip()  # 移除可能的前后空白字符
            if file:
                if file in file_changes:
                    file_changes[file] += 1
                else:
                    file_changes[file] = 1

# 关闭游标和数据库连接
cursor.close()
db.close()

# 将字典转换为DataFrame
df_file_changes = pd.DataFrame(list(file_changes.items()), columns=['file_name', 'changes'])

# 展示前几行数据以确认结果
print(df_file_changes.head())

# ----------------------- 频繁变更的文件的热图

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 对数据进行排序，确保条形图按变更次数降序排列
df_file_changes_sorted = df_file_changes.sort_values(by='changes', ascending=False)

plt.figure(figsize=(10, 8))
sns.barplot(x='changes', y='file_name', data=df_file_changes_sorted.head(10))
plt.xlabel('Number of Changes')
plt.ylabel('File Name')
plt.title('Top 10 Frequently Changed Files')
plt.show()


