#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Distributed Time Management Tool
Command line interface for recording and managing activities
"""

import argparse
import sys
import uuid
import json
import os
import signal
from datetime import datetime
import http.server
import socketserver
import threading
import urllib.request
import urllib.parse
import time


class Activity:
    """Activity class to record activity parameters"""
    
    def __init__(self, description, comments="", attachments=None):
        self.uuid = str(uuid.uuid4())
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.description = description
        self.comments = comments
        self.attachments = attachments or []
        self.status = "ongoing"  # ongoing, finished, aborted, deleted
    
    def finish(self):
        """Finish activity normally"""
        self.end_time = datetime.now().isoformat()
        self.status = "finished"
    
    def abort(self):
        """Abort activity"""
        self.end_time = datetime.now().isoformat()
        self.status = "aborted"
    
    def delete(self):
        """Mark activity as deleted"""
        self.status = "deleted"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "uuid": self.uuid,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description,
            "comments": self.comments,
            "attachments": self.attachments,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create activity instance from dictionary"""
        activity = cls.__new__(cls)
        activity.uuid = data["uuid"]
        activity.start_time = data["start_time"]
        activity.end_time = data["end_time"]
        activity.description = data["description"]
        activity.comments = data["comments"]
        activity.attachments = data["attachments"]
        activity.status = data["status"]
        return activity


class ActivityManager:
    """Activity manager"""
    
    def __init__(self, data_file="activities.json"):
        self.data_file = data_file
        self.activities = []
        self.current_activity = None
        self.load_activities()
        # Set current_activity if there's an ongoing activity
        for activity in self.activities:
            if activity.status == "ongoing":
                self.current_activity = activity
                break
    
    def load_activities(self):
        """Load activities from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.activities = [Activity.from_dict(activity_data) for activity_data in data]
            except (json.JSONDecodeError, KeyError):
                self.activities = []
    
    def save_activities(self):
        """Save activities to file"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([activity.to_dict() for activity in self.activities], f, ensure_ascii=False, indent=2)
    
    def start_activity(self, description, comments="", attachments=None):
        """Start a new activity"""
        # If there is an ongoing activity, finish it first
        if self.current_activity:
            self.current_activity.finish()
            # self.activities.append(self.current_activity) - already in the list
        
        activity = Activity(description, comments, attachments)
        self.current_activity = activity
        # Add the new activity to the list
        self.activities.append(activity)
        self.save_activities()
        return activity
    
    def finish_current_activity(self):
        """Finish current activity"""
        if self.current_activity:
            self.current_activity.finish()
            # The activity is already in the list, just save the changes
            self.current_activity = None
            self.save_activities()
            return True
        return False
    
    def abort_current_activity(self):
        """Abort current activity"""
        if self.current_activity:
            self.current_activity.abort()
            # The activity is already in the list, just save the changes
            self.current_activity = None
            self.save_activities()
            return True
        return False
    
    def list_activities(self, show_all=False):
        """List activities"""
        if show_all:
            return self.activities
        else:
            # By default, don't include removed or aborted activities
            return [activity for activity in self.activities if activity.status not in ["deleted", "aborted"]]
    
    def delete_activity(self, activity_uuid):
        """Delete activity by uuid (mark as deleted)"""
        for activity in self.activities:
            if activity.uuid == activity_uuid:
                activity.delete()
                self.save_activities()
                return True
        return False
    
    def push_to_server(self, server_url):
        """Push local activities to remote server"""
        try:
            data = json.dumps([activity.to_dict() for activity in self.activities]).encode('utf-8')
            req = urllib.request.Request(
                server_url + "/activities",
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except Exception:
            return False
    
    def pull_from_server(self, server_url):
        """Pull activities from remote server and merge data"""
        try:
            with urllib.request.urlopen(server_url + "/activities") as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    server_activities = [Activity.from_dict(activity_data) for activity_data in data]
                    
                    # Merge data: add activities not present locally
                    local_uuids = {activity.uuid for activity in self.activities}
                    for server_activity in server_activities:
                        if server_activity.uuid not in local_uuids:
                            self.activities.append(server_activity)
                    
                    self.save_activities()
                    return True
        except Exception:
            return False


class ActivityHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler"""
    
    def do_POST(self):
        """Handle POST request (receive activity data)"""
        if self.path == "/activities":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                activities_data = json.loads(post_data.decode('utf-8'))
                # Here we should merge received activity data into server's activity list
                # For simplicity, we assume manager is global
                global manager
                server_activities = [Activity.from_dict(data) for data in activities_data]
                
                # Merge data
                local_uuids = {activity.uuid for activity in manager.activities}
                for server_activity in server_activities:
                    if server_activity.uuid not in local_uuids:
                        manager.activities.append(server_activity)
                
                manager.save_activities()
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Activities received and merged")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("Error processing data: {}".format(str(e)).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET request (provide activity data)"""
        if self.path == "/activities":
            # Return all activity data
            global manager
            # Reload activities data to ensure it's up to date
            manager.load_activities()
            activities_data = [activity.to_dict() for activity in manager.activities]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(activities_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def format_activity_list(activities):
    """Format activity list according to requirements"""
    if not activities:
        return "No activities found."
    
    result = []
    for activity in activities:
        # Date part (extracted from start time)
        start_date = activity.start_time.split("T")[0] if activity.start_time else ""
        
        # Extract time parts
        start_time = activity.start_time.split("T")[1].split(".")[0] if activity.start_time else ""
        end_time = activity.end_time.split("T")[1].split(".")[0] if activity.end_time else ""
        
        # Format activity info
        activity_str = "{} {} {} {} {} {}".format(
            activity.uuid, 
            start_date, 
            start_time, 
            end_time, 
            activity.description, 
            activity.comments
        )
        result.append(activity_str)
        
        # If there are attachments, add attachment info
        if activity.attachments:
            attachments_str = " ".join(activity.attachments)
            result.append("attach {}".format(attachments_str))
        
        # Add separator if there are more activities
        if len(activities) > 1 and activity != activities[-1]:
            result.append("---")
    
    return "\n".join(result)


def run_server(port=5678):
    """Run server mode"""
    global manager
    # Initialize manager for server mode
    manager = ActivityManager()
    with socketserver.TCPServer(("", port), ActivityHTTPRequestHandler) as httpd:
        print("Server running on port {}".format(port))
        httpd.serve_forever()


def setup_signal_handlers(manager):
    """Setup signal handlers"""
    def signal_handler(sig, frame):
        if sig == signal.SIGINT:
            # CTRL+C aborts current activity
            if manager.current_activity:
                manager.abort_current_activity()
                print("\nCurrent activity aborted.")
            sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)


def wait_for_user_input(manager):
    """Wait for user input to finish or abort the activity"""
    print("\nActivity is ongoing. Options:")
    print("  Press F to finish the activity")
    print("  Press CTRL+C to abort the activity and exit")
    
    try:
        input("Press Enter to finish the activity (F key support requires special permissions on macOS): ")
        if manager.finish_current_activity():
            print("Current activity finished.")
        else:
            print("No ongoing activity.")
    except KeyboardInterrupt:
        # CTRL+C will be handled by signal handler
        pass


def main():
    parser = argparse.ArgumentParser(description="Distributed Time Management Tool")
    parser.add_argument("--server", action="store_true", help="Run in server mode")
    parser.add_argument("--port", type=int, default=5678, help="Port for server mode")
    parser.add_argument("--start", metavar="DESCRIPTION", help="Start a new activity")
    parser.add_argument("--finish", action="store_true", help="Finish current activity")
    parser.add_argument("--abort", action="store_true", help="Abort current activity")
    parser.add_argument("--list", action="store_true", help="List activities")
    parser.add_argument("--all", action="store_true", help="Show all activities including deleted/aborted")
    parser.add_argument("--delete", metavar="UUID", help="Delete activity by UUID")
    parser.add_argument("--push", metavar="SERVER_URL", help="Push activities to remote server")
    parser.add_argument("--pull", metavar="SERVER_URL", help="Pull activities from remote server")
    parser.add_argument("--comments", metavar="COMMENTS", help="Comments for the activity")
    parser.add_argument("--attachments", metavar="FILES", nargs="*", help="Attachment files for the activity")
    parser.add_argument("--wait", action="store_true", help="Wait for user input after starting activity")
    
    args = parser.parse_args()
    
    global manager
    manager = ActivityManager()
    
    # Setup signal handlers
    setup_signal_handlers(manager)
    
    # Server mode
    if args.server:
        run_server(args.port)
        return
    
    # Handle command line arguments
    if args.start:
        activity = manager.start_activity(args.start, args.comments or "", args.attachments or [])
        print("Activity started: {}".format(activity.uuid))
        
        # If wait mode is requested, wait for user input
        if args.wait:
            wait_for_user_input(manager)
        return
    
    if args.finish:
        if manager.finish_current_activity():
            print("Current activity finished.")
        else:
            print("No ongoing activity.")
        return
    
    if args.abort:
        if manager.abort_current_activity():
            print("Current activity aborted.")
        else:
            print("No ongoing activity.")
        return
    
    if args.list:
        activities = manager.list_activities(args.all)
        print(format_activity_list(activities))
        return
    
    if args.delete:
        if manager.delete_activity(args.delete):
            print("Activity {} marked as deleted.".format(args.delete))
        else:
            print("Activity {} not found.".format(args.delete))
        return
    
    if args.push:
        if manager.push_to_server(args.push):
            print("Activities pushed to server successfully.")
        else:
            print("Failed to push activities to server.")
        return
    
    if args.pull:
        if manager.pull_from_server(args.pull):
            print("Activities pulled from server and merged successfully.")
        else:
            print("Failed to pull activities from server.")
        return
    
    # Default behavior: show help if no arguments provided
    parser.print_help()


if __name__ == "__main__":
    main()