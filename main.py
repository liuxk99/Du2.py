#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import threading
import time
from activity_manager import ActivityManager
from activity import ActivityStatus


class TimeTrackerCLI:
    def __init__(self):
        self.manager = ActivityManager()
        self.current_activity = None
        self.running = False

    def start_server(self, port):
        """启动服务模式，在指定端口监听"""
        print("Starting server on port {}".format(port))
        # 这里需要实现服务器逻辑
        # 为简化起见，暂时只打印信息
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nServer stopped.")

    def start_activity(self, description, remarks="", attachments=None):
        """开始一个新活动"""
        if self.current_activity:
            print("There is already an activity in progress. Please complete or abort it first.")
            return

        self.current_activity = self.manager.start_activity(description, remarks, attachments)
        print("Started activity: {}".format(self.current_activity.uuid))
        print("Description: {}".format(description))
        print("Start time: {}".format(self.current_activity.start_time.strftime('%Y-%m-%d %H:%M:%S')))

    def complete_activity(self):
        """完成当前活动"""
        if not self.current_activity:
            print("No activity in progress.")
            return

        self.current_activity.complete()
        self.manager.save_activities()
        print("Completed activity: {}".format(self.current_activity.uuid))
        print("End time: {}".format(self.current_activity.end_time.strftime('%Y-%m-%d %H:%M:%S')))
        duration = self.current_activity.end_time - self.current_activity.start_time
        print("Duration: {}".format(duration))
        self.current_activity = None

    def abort_activity(self):
        """终止当前活动"""
        if not self.current_activity:
            print("No activity in progress.")
            return

        self.current_activity.abort()
        self.manager.save_activities()
        print("Aborted activity: {}".format(self.current_activity.uuid))
        print("End time: {}".format(self.current_activity.end_time.strftime('%Y-%m-%d %H:%M:%S')))
        self.current_activity = None

    def list_activities(self, show_all=False):
        """列出活动"""
        activities = self.manager.list_activities(show_all)
        if not activities:
            print("No activities found.")
            return

        for activity in activities:
            print(str(activity))
            print("---")

    def remove_activity(self, activity_uuid):
        """删除活动"""
        if self.manager.remove_activity(activity_uuid):
            print("Removed activity: {}".format(activity_uuid))
        else:
            print("Activity not found: {}".format(activity_uuid))

    def push_to_server(self, server_url):
        """推送活动到服务器"""
        if self.manager.push_to_server(server_url):
            print("Activities pushed to server successfully.")
        else:
            print("Failed to push activities to server.")

    def pull_from_server(self, server_url):
        """从服务器拉取活动"""
        if self.manager.pull_from_server(server_url):
            print("Activities pulled from server successfully.")
        else:
            print("Failed to pull activities from server.")

    def interactive_mode(self):
        """进入交互模式"""
        print("Entering interactive mode. Press Ctrl+C to abort current activity or 'F' to finish.")
        print("Commands: start <description> | list | list --all | remove <uuid> | quit")
        
        try:
            while True:
                try:
                    command = input("> ").strip().split()
                    if not command:
                        continue

                    if command[0] == "start":
                        if len(command) < 2:
                            print("Please provide a description for the activity.")
                            continue
                        description = " ".join(command[1:])
                        self.start_activity(description)
                    
                    elif command[0] == "list":
                        show_all = "--all" in command
                        self.list_activities(show_all)
                    
                    elif command[0] == "remove":
                        if len(command) < 2:
                            print("Please provide the UUID of the activity to remove.")
                            continue
                        self.remove_activity(command[1])
                    
                    elif command[0] == "quit":
                        break
                    
                    else:
                        print("Unknown command. Available commands: start, list, remove, quit")

                except KeyboardInterrupt:
                    if self.current_activity:
                        self.abort_activity()
                    else:
                        print("\nUse 'quit' to exit the program.")
        
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")

    def run(self):
        parser = argparse.ArgumentParser(description="Distributed Time Management Tool")
        parser.add_argument("--server", action="store_true", help="Start in server mode")
        parser.add_argument("--port", type=int, default=5678, help="Port to listen on in server mode")
        parser.add_argument("--start", nargs="+", help="Start a new activity with description")
        parser.add_argument("--complete", action="store_true", help="Complete current activity")
        parser.add_argument("--abort", action="store_true", help="Abort current activity")
        parser.add_argument("--list", action="store_true", help="List activities")
        parser.add_argument("--all", action="store_true", help="Show all activities including removed/aborted")
        parser.add_argument("--remove", help="Remove activity by UUID")
        parser.add_argument("--push", help="Push activities to server URL")
        parser.add_argument("--pull", help="Pull activities from server URL")
        parser.add_argument("--interactive", "-i", action="store_true", help="Enter interactive mode")

        args = parser.parse_args()

        # 服务模式
        if args.server:
            self.start_server(args.port)
            return

        # 处理命令行参数
        if args.start:
            description = " ".join(args.start)
            self.start_activity(description)
        
        elif args.complete:
            self.complete_activity()
        
        elif args.abort:
            self.abort_activity()
        
        elif args.list:
            self.list_activities(args.all)
        
        elif args.remove:
            self.remove_activity(args.remove)
        
        elif args.push:
            self.push_to_server(args.push)
        
        elif args.pull:
            self.pull_from_server(args.pull)
        
        elif args.interactive:
            self.interactive_mode()
        
        else:
            # 默认显示帮助信息
            parser.print_help()


if __name__ == "__main__":
    cli = TimeTrackerCLI()
    cli.run()