# 导入 git 库，用于操作 Git 仓库
import git
# 从 git 库中导入 Repo 类，用于操作 Git 仓库
from git import Repo
# 导入 mysql.connector 库，用于连接和操作 MySQL 数据库
import mysql.connector
# 导入 os 库，用于操作系统功能，如文件和目录
import os
# 设置 git 命令的执行路径，指定 Git 二进制文件的位置
# git.Git().set_binary('E:\\grok\\Git-2.44.0-64-bit.exe')
import subprocess
# 连接到 MySQL 数据库，使用给定的参数（主机、端口、用户、密码、数据库名称）
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="chengcheng",
    password="171612cgj",
    database="db"
)
print("1")
# 创建数据库游标，用于执行数据库操作
cursor = db.cursor()

# 创建存储 Git 日志信息的表，如果已经创建，这部分代码需要被注释掉以避免错误
# 注意：这里的 cursor.execute() 应该有 SQL 语句作为参数，但是遗漏了
#try:
#    cursor.execute()
#except mysql.connector.Error as err:
#    print("Failed creating table: {}".format(err))

# 定义 Git 仓库的本地存储路径
repo_path = 'E:\\pythonProject\\dbHub\\numpy'

# 打开位于 repo_path 的 Git 仓库
repo = Repo(repo_path)

# 获取指定分支（这里是 'main'）的所有提交记录，并转换为列表
commits = list(repo.iter_commits('main'))
print("4")
# 遍历所有的提交记录
for commit in commits:
    # 提取提交的哈希值
    commit_hash = commit.hexsha
    print(commit_hash)
    # 提取提交作者的名称
    author = commit.author.name
    print(author)
    # 格式化提交的日期和时间
    date = commit.authored_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(date)
    # 提取提交的标题（通常是提交信息的第一行）
    title = commit.summary
    print(title)
    # 提取完整的提交信息
    description = commit.message
    print(description)
    print("5")

    # 提取文件级别的修改信息
    file_changes = commit.stats.files
    changed_files = list(file_changes.keys())  # 提取修改的文件列表
    change_type = {}  # 存储修改类型的字典
    for file, changes in file_changes.items():
        change_type[file] = 'added' if changes['insertions'] > 0 else 'deleted' if changes['deletions'] > 0 else 'modified'

    # 计算修改的总行数
    lines_code = 0
    for value in file_changes.values():
        lines_code += value['insertions'] + value['deletions']

    # 截断 changed_files 列中超过长度的部分
    max_length = 255
    for i in range(len(changed_files)):
        changed_files[i] = changed_files[i][:max_length]

    # 将提取的信息存储到 MySQL 数据库中的 git_log 表
    # 使用参数化查询防止 SQL 注入
    try:
        cursor.execute(
            "INSERT INTO git_log (commit_hash, author, date, title, description, changed_files, lines_code, change_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (commit_hash, author, date, title, description, str(changed_files), lines_code, str(change_type)))
        db.commit()  # 提交事务，确保数据被保存
        print("finish")
    except mysql.connector.Error as err:
        print("Failed inserting data: {}".format(err))
        db.rollback()  # 如果出现错误，回滚事务
print("ok")

# 完成数据库操作后，关闭数据库连接
db.close()


