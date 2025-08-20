# 概述
设计一个分布式时间管理工具，使用命令行界面，记录活动(Activity)的参数，具体包括uuid、开始时间、结束时间、工作描述、备注(可选)、附件(可选)，可以终止和正常结束。
# 工作模式
## 服务模式
+ 默认使用本地模式，用了记录、查询、管理活动的状态；
+ 使用`--server`启动服务模式，在5678端口监听；
+ 接受远程推送Activity数据到服务器，并合并；
+ 结束远程主机从拉取Activity数据，在本地合并；
# 具体要求
## 命令行界面，交互
 + CTRL+C，终止(Abort)
 + F键，结束
## 功能列表
 + 开始一个活动，此时记录开始时间，状态为进行中
 + 结束一个活动，此时记录结束时间，状态为正常
 + 终止一个活动，此时记录结束时间，状态为终止
 + 列出活动，默认不包含removed or aborted activities，除非使用`--all` option。格式为
```
uuid 日期 begin-time end-time description comments
attachattachments files
---
uuid 日期 begin-time end-time description comments
attachattachments files
```
 + 根据uuid删除活动(并非真实删除该数据，只是作为一个删除标记)
 + 推送本地的活动记录到远程服务器。
 + 从远程服务器拉取活动记录，并合并数据。