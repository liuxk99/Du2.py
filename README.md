# Distributed Time Management Tool

A command-line tool for recording and managing activities with distributed capabilities.

[中文版 README](README_ZH.md)

## Features

- Start, finish, and abort activities
- Record activity details including UUID, start time, end time, description, comments, and attachments
- List activities with customizable filters
- Mark activities as deleted (soft delete)
- Distributed functionality:
  - Run in server mode to accept remote activity data
  - Push local activities to remote server
  - Pull activities from remote server and merge data

## Requirements

- Python 3.13

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

Start a new activity:
```bash
python du2.py --start "Activity description" --comments "Optional comments" --attachments file1.txt file2.pdf
```

Start a new activity and wait for user input to finish:
```bash
python du2.py --start "Activity description" --wait
```
Then press Enter to finish the activity or CTRL+C to abort it.
(Note: F key support requires special permissions on macOS)

Finish the current activity:
```bash
python du2.py --finish
```

Abort the current activity:
```bash
python du2.py --abort
```

List activities:
```bash
python du2.py --list [--all]
```

Delete an activity (soft delete):
```bash
python du2.py --delete <activity-uuid>
```

Modify an activity:
```bash
python du2.py --modify <activity-uuid> --start "New description" --comments "New comments"
```

### Distributed Features

Run in server mode:
```bash
python du2.py --server [--port 5678]
```

Push local activities to remote server:
```bash
python du2.py --push http://remote-server:5678
```

Pull activities from remote server:
```bash
python du2.py --pull http://remote-server:5678
```

### Testing Distributed Features

1. Start the server:
```bash
python du2.py --server --port 5678
```

2. In another terminal, create and push activities:
```bash
python du2.py --start "Test activity" --comments "This is a test"
python du2.py --push http://localhost:5678
```

3. Retrieve activities from server:
```bash
curl http://localhost:5678/activities
```

4. Pull activities from server:
```bash
python du2.py --pull http://localhost:5678
```

5. Screenshots
<img src="https://raw.githubusercontent.com/liuxk99/Du2.py/refs/heads/master/screenshots/cli-serv-02.png" width="400">

## Interactive Mode

To use the tool in interactive mode with F key support, run it directly in a terminal:
```bash
python du2.py --start "Activity description" --wait
```

## Activity Status

- `ongoing`: Activity is currently in progress
- `finished`: Activity was completed normally
- `aborted`: Activity was terminated unexpectedly
- `deleted`: Activity was marked as deleted (soft delete)

## Data Storage

Activities are stored in a local JSON file (`activities.json`) in the same directory as the script.

## License

MIT
