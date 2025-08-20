import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List
import json


class ActivityStatus(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABORTED = "aborted"
    REMOVED = "removed"


class Activity:
    def __init__(self, description, start_time=None, 
                 end_time=None, remarks="", 
                 attachments=None):
        self.uuid = str(uuid.uuid4())
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.description = description
        self.remarks = remarks
        self.attachments = attachments or []
        self.status = ActivityStatus.IN_PROGRESS if not end_time else ActivityStatus.COMPLETED

    def complete(self):
        """结束一个活动，记录结束时间，状态为正常"""
        self.end_time = datetime.now()
        self.status = ActivityStatus.COMPLETED

    def abort(self):
        """终止一个活动，记录结束时间，状态为终止"""
        self.end_time = datetime.now()
        self.status = ActivityStatus.ABORTED

    def remove(self):
        """标记活动为删除状态"""
        self.status = ActivityStatus.REMOVED

    def to_dict(self):
        """将活动转换为字典格式"""
        return {
            "uuid": self.uuid,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "description": self.description,
            "remarks": self.remarks,
            "attachments": self.attachments,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建活动对象"""
        activity = cls(
            description=data["description"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]) if data["end_time"] else None,
            remarks=data["remarks"],
            attachments=data["attachments"]
        )
        activity.uuid = data["uuid"]
        activity.status = ActivityStatus(data["status"])
        return activity

    def __str__(self):
        """格式化输出活动信息"""
        start_time_str = self.start_time.strftime("%H:%M")
        end_time_str = self.end_time.strftime("%H:%M") if self.end_time else "--:--"
        date_str = self.start_time.strftime("%Y-%m-%d")
        
        result = "{} {} {} {} {} {}\n".format(self.uuid, date_str, start_time_str, end_time_str, self.description, self.remarks)
        if self.attachments:
            result += "attachments: {}\n".format(', '.join(self.attachments))
        return result