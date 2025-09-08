# 分布式时间管理工具

一个用于记录和管理活动的命令行工具，具有分布式功能。

## 功能

- 开始、结束和中止活动
- 记录活动详情，包括 UUID、开始时间、结束时间、描述、评论和附件
- 使用可自定义过滤器列出活动
- 将活动标记为已删除（软删除）
- 分布式功能：
  - 以服务器模式运行以接受远程活动数据
  - 将本地活动推送到远程服务器
  - 从远程服务器拉取活动并合并数据

## 要求

- Python 3.13

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本命令

开始一个新活动：
```bash
python du2.py --start "活动描述" --comments "可选评论" --attachments file1.txt file2.pdf
```

开始一个新活动并等待用户输入以结束：
```bash
python du2.py --start "活动描述" --wait
```
然后按 Enter 键结束活动或按 CTRL+C 中止活动。
（注意：F 键支持需要在 macOS 上具有特殊权限）

结束当前活动：
```bash
python du2.py --finish
```

中止当前活动：
```bash
python du2.py --abort
```

列出活动：
```bash
python du2.py --list [--all]
```

删除活动（软删除）：
```bash
python du2.py --delete <activity-uuid>
```

修改活动：
```bash
python du2.py --modify <activity-uuid> --start "新描述" --comments "新评论"
```

### 分布式功能

以服务器模式运行：
```bash
python du2.py --server [--port 5678]
```

将本地活动推送到远程服务器：
```bash
python du2.py --push http://remote-server:5678
```

从远程服务器拉取活动：
```bash
python du2.py --pull http://remote-server:5678
```

### 测试分布式功能

1. 启动服务器：
```bash
python du2.py --server --port 5678
```

2. 在另一个终端中，创建并推送活动：
```bash
python du2.py --start "测试活动" --comments "这是一个测试"
python du2.py --push http://localhost:5678
```

3. 从服务器检索活动：
```bash
curl http://localhost:5678/activities
```

4. 从服务器拉取活动：
```bash
python du2.py --pull http://localhost:5678
```

5. 截图
<img src="https://raw.githubusercontent.com/liuxk99/Du2.py/refs/heads/master/screenshots/cli-serv-02.png" width="400">

## 交互模式

要在具有 F 键支持的交互模式下使用该工具，请直接在终端中运行：
```bash
python du2.py --start "活动描述" --wait
```

## 活动状态

- `ongoing`：活动正在进行中
- `finished`：活动正常完成
- `aborted`：活动意外终止
- `deleted`：活动被标记为已删除（软删除）

## 数据存储

活动存储在脚本所在目录的本地 JSON 文件 (`activities.json`) 中。

## 许可证

MIT