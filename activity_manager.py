import json
import os
from typing import List, Optional
from datetime import datetime
from activity import Activity, ActivityStatus


class ActivityManager:
    def __init__(self, data_file="activities.json"):
        self.data_file = data_file
        self.activities = []
        self.load_activities()

    def start_activity(self, description, remarks="", attachments=None):
        """开始一个活动，记录开始时间，状态为进行中"""
        activity = Activity(description, remarks=remarks, attachments=attachments or [])
        self.activities.append(activity)
        self.save_activities()
        return activity

    def complete_activity(self, activity_uuid):
        """结束一个活动，记录结束时间，状态为正常"""
        activity = self.get_activity(activity_uuid)
        if activity and activity.status == ActivityStatus.IN_PROGRESS:
            activity.complete()
            self.save_activities()
            return True
        return False

    def abort_activity(self, activity_uuid):
        """终止一个活动，记录结束时间，状态为终止"""
        activity = self.get_activity(activity_uuid)
        if activity and activity.status == ActivityStatus.IN_PROGRESS:
            activity.abort()
            self.save_activities()
            return True
        return False

    def remove_activity(self, activity_uuid):
        """删除活动(标记为删除)"""
        activity = self.get_activity(activity_uuid)
        if activity:
            activity.remove()
            self.save_activities()
            return True
        return False

    def get_activity(self, activity_uuid):
        """根据UUID获取活动"""
        for activity in self.activities:
            if activity.uuid == activity_uuid:
                return activity
        return None

    def list_activities(self, show_all=False):
        """列出活动，默认不包含removed or aborted activities"""
        if show_all:
            return self.activities
        return [a for a in self.activities if a.status not in [ActivityStatus.REMOVED, ActivityStatus.ABORTED]]

    def save_activities(self):
        """保存活动到文件"""
        data = [activity.to_dict() for activity in self.activities]
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_activities(self):
        """从文件加载活动"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.activities = [Activity.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                self.activities = []

    def push_to_server(self, server_url):
        """推送本地活动记录到远程服务器"""
        # 这里需要实现与服务器的通信逻辑
        # 为简化起见，暂时返回True
        print("Pushing activities to {}".format(server_url))
        return True

    def pull_from_server(self, server_url):
        """从远程服务器拉取活动记录"""
        # 这里需要实现与服务器的通信逻辑
        # 为简化起见，暂时返回True
        print("Pulling activities from {}".format(server_url))
        return True