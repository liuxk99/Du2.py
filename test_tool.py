#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Distributed Time Management Tool
"""

import subprocess
import time
import os

def run_command(command, description):
    """Run a command and print its output"""
    print(f"\n--- {description} ---")
    print(f"Command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Error:\n{result.stderr}")
    return result

def main():
    # Clean up any existing activities file
    if os.path.exists("activities.json"):
        os.remove("activities.json")
    
    print("Distributed Time Management Tool - Test Script")
    
    # Test creating activities
    run_command("python main.py --start 'Test Activity 1' --comments 'First test activity'", "Create first activity")
    run_command("python main.py --start 'Test Activity 2' --comments 'Second test activity' --attachments doc1.pdf doc2.txt", "Create second activity with attachments")
    
    # Test listing activities
    run_command("python main.py --list", "List activities")
    
    # Test finishing activities
    run_command("python main.py --finish", "Finish current activity")
    run_command("python main.py --list", "List activities after finishing")
    
    # Test aborting activities
    run_command("python main.py --start 'Test Activity 3' --comments 'Third test activity'", "Create third activity")
    run_command("python main.py --abort", "Abort current activity")
    run_command("python main.py --list", "List activities after aborting")
    run_command("python main.py --list --all", "List all activities including aborted")
    
    # Test deleting activities
    run_command("python main.py --delete $(python main.py --list --all | head -n 1 | cut -d' ' -f1)", "Delete first activity")
    run_command("python main.py --list --all", "List all activities after deletion")
    
    print("\n--- Test completed ---")

if __name__ == "__main__":
    main()