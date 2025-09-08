#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive script for the Distributed Time Management Tool
"""

import subprocess
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python interactive_demo.py <activity_description>")
        sys.exit(1)
    
    description = " ".join(sys.argv[1:])
    
    # Start an activity with wait mode
    cmd = [sys.executable, "du2.py", "--start", description, "--wait"]
    
    print(f"Starting activity: {description}")
    print("The program will block until you press Enter to finish or CTRL+C to abort.")
    
    try:
        # Run the command and let it wait for user input
        result = subprocess.run(cmd, check=True)
        print("Activity completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")

if __name__ == "__main__":
    main()