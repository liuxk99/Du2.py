# Distributed Time Management Tool

A command-line tool for recording and managing activities with distributed capabilities.

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
python main.py --start "Activity description" --comments "Optional comments" --attachments file1.txt file2.pdf
```

Start a new activity and wait for user input to finish:
```bash
python main.py --start "Activity description" --wait
```
Then press Enter to finish the activity or CTRL+C to abort it.
(Note: F key support requires special permissions on macOS)

Finish the current activity:
```bash
python main.py --finish
```

Abort the current activity:
```bash
python main.py --abort
```

List activities:
```bash
python main.py --list [--all]
```

Delete an activity (soft delete):
```bash
python main.py --delete <activity-uuid>
```

### Distributed Features

Run in server mode:
```bash
python main.py --server [--port 5678]
```

Push local activities to remote server:
```bash
python main.py --push http://remote-server:5678
```

Pull activities from remote server:
```bash
python main.py --pull http://remote-server:5678
```

## Interactive Mode

To use the tool in interactive mode with F key support, run it directly in a terminal:
```bash
python main.py --start "Activity description" --wait
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