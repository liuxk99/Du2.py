# -*- coding: utf-8 -*-
# 使用Python3写一个控制台程序，进入活动计时显示Elapse时间，按F键结束，按CTRL+C终止(Abort)，记录结束时间，显示开始时间、结束时间。
import time
import threading
import sys
import signal
from datetime import datetime

# Global variables
start_time = None
end_time = None
elapsed_seconds = 0
running = True
timer_thread = None

def format_time(seconds):
    """Format seconds to HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def display_timer():
    """Display timer on console"""
    global elapsed_seconds, running, start_time
    while running:
        if not running or start_time is None:
            break
        # Convert datetime to timestamp for calculation
        current_time = time.time()
        start_timestamp = start_time.timestamp()
        current_elapsed = elapsed_seconds + (current_time - start_timestamp)
        print(f"\rElapsed: {format_time(current_elapsed)}", end="", flush=True)
        time.sleep(0.1)  # Update frequency

def signal_handler(signum, frame):
    """Handle CTRL+C signal"""
    global running, end_time
    end_time = datetime.now()
    running = False
    print(f"\n\nProgram aborted by user (CTRL+C)")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0)

def main():
    global start_time, end_time, elapsed_seconds, running, timer_thread
    
    # Set signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Activity Timer")
    print("Press F to end timing, CTRL+C to abort")
    print("-" * 40)
    
    # Record start time
    start_time = datetime.now()
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Start display thread
    timer_thread = threading.Thread(target=display_timer, daemon=True)
    timer_thread.start()
    
    try:
        while running:
            # Check for keyboard input
            try:
                # Use msvcrt on Windows, tty and termios on Unix
                if sys.platform == "win32":
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                        if key == 'f':
                            end_time = datetime.now()
                            running = False
                            break
                else:
                    # Unix/Linux/Mac
                    try:
                        import tty
                        import termios
                        import select
                        
                        # Set non-blocking mode
                        fd = sys.stdin.fileno()
                        old_settings = termios.tcgetattr(fd)
                        try:
                            tty.setcbreak(sys.stdin.fileno())
                            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                                key = sys.stdin.read(1).lower()
                                if key == 'f':
                                    end_time = datetime.now()
                                    running = False
                                    break
                        finally:
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    except (ImportError, Exception):
                        # Fallback method - just sleep
                        time.sleep(0.1)
                        continue
                        
            except Exception:
                time.sleep(0.1)
                continue
                
    except KeyboardInterrupt:
        pass
    
    # Program end
    if not running and end_time:
        total_elapsed = (end_time - start_time).total_seconds()
        print(f"\n\nTiming ended")
        print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Elapsed Time: {format_time(total_elapsed)}")

if __name__ == "__main__":
    main()