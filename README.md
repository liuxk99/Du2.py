# Distributed Time Management Tool

分布式时间管理工具是一个命令行应用程序，用于跟踪和管理活动时间。

## 功能特性

- 开始、结束和终止活动
- 记录活动的开始时间、结束时间、描述、备注和附件
- 列出活动历史
- 标记删除活动（非真实删除）
- 服务模式支持远程数据同步

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行模式

```bash
# 开始一个新活动
python main.py --start "编写项目文档" "整理需求文档"

# 完成当前活动
python main.py --complete

# 终止当前活动
python main.py --abort

# 列出活动
python main.py --list

# 列出所有活动（包括已删除和终止的）
python main.py --list --all

# 删除活动（标记为删除）
python main.py --remove <activity-uuid>

# 启动服务模式
python main.py --server --port 5678

# 推送活动到远程服务器
python main.py --push http://example.com/api/activities

# 从远程服务器拉取活动
python main.py --pull http://example.com/api/activities
```

### 交互模式

```bash
# 进入交互模式
python main.py --interactive
```

在交互模式中：
- 使用 `start <description>` 开始新活动
- 使用 `list` 列出活动
- 使用 `list --all` 列出所有活动
- 使用 `remove <uuid>` 删除活动
- 使用 `quit` 退出程序
- 按 `Ctrl+C` 终止当前活动

## 数据存储

活动数据默认存储在 `activities.json` 文件中。