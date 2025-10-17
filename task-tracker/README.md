# Task Tracker

Simple CLI tool for tracking daily tasks with zero configuration required.

## Features

- **Zero Setup**: Works immediately without any configuration
- **Simple Commands**: Add, list, complete, show, and delete tasks
- **Local Storage**: All data stored locally in JSON format
- **Beautiful Output**: Rich terminal formatting with colors and tables
- **Type Safe**: Built with Pydantic for data validation
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Installation

### Using pip

```bash
pip install -e .
```

### From source

```bash
git clone https://github.com/yourusername/task-tracker.git
cd task-tracker
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
# Add a task
task add "Implement user authentication"

# List pending tasks
task list

# Complete a task
task complete 1

# Show task details
task show 1

# Delete a task
task delete 1

# List all tasks (including completed)
task list --all

# Show help
task --help
```

## Usage

### Add a Task

```bash
task add "Your task description"
```

Output:
```
✓ Task added successfully!
  ID: 1
  Title: Your task description
  Status: pending
  Created: 2025-10-01 14:30:00
```

### List Tasks

```bash
# List pending tasks (default)
task list

# List completed tasks
task list --status completed

# List all tasks
task list --all

# Limit number of tasks shown
task list --limit 5
```

### Show Task Details

```bash
task show <task_id>
```

Output:
```
Task #1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:      Implement user authentication
Status:     pending
Created:    2025-10-01 14:30:00
Completed:  -
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Complete a Task

```bash
task complete <task_id>

# Force update completion time if already completed
task complete <task_id> --force
```

### Delete a Task

```bash
# With confirmation prompt
task delete <task_id>

# Skip confirmation
task delete <task_id> --force
```

## Configuration

### Data File Location

By default, tasks are stored in `~/.task-tracker/tasks.json`.

You can customize this location using the `TASK_TRACKER_DATA_FILE` environment variable:

```bash
export TASK_TRACKER_DATA_FILE="/path/to/custom/tasks.json"
```

### Environment Variables

- `TASK_TRACKER_DATA_FILE`: Custom location for tasks.json
- `TASK_TRACKER_BACKUP`: Enable/disable backups (default: true)

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=task_tracker

# Format code
black task_tracker/

# Lint code
ruff task_tracker/
```

### Project Structure

```
task-tracker/
├── task_tracker/
│   ├── __init__.py
│   ├── __main__.py       # Entry point
│   ├── cli.py            # CLI commands
│   ├── models.py         # Pydantic models
│   ├── storage.py        # JSON storage
│   ├── config.py         # Configuration
│   └── utils.py          # Utilities
├── tests/
│   └── fixtures/
├── setup.py
├── requirements.txt
└── README.md
```

## Data Format

Tasks are stored in JSON format at `~/.task-tracker/tasks.json`:

```json
{
  "version": "1.0.0",
  "last_id": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Implement user authentication",
      "status": "completed",
      "created_at": "2025-10-01T14:30:00",
      "completed_at": "2025-10-01T16:20:00"
    },
    {
      "id": 2,
      "title": "Write API documentation",
      "status": "pending",
      "created_at": "2025-10-01T15:45:00",
      "completed_at": null
    }
  ]
}
```

## Requirements

- Python 3.9 or higher
- typer[all] >= 0.9.0
- pydantic >= 2.0.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

Potential features for future versions:
- Priority levels for tasks
- Due dates
- Tags/categories
- Search functionality
- Task statistics
- Export to CSV/JSON
- Recurring tasks

## Troubleshooting

### Corrupted Data File

If you encounter a corrupted data file error:

```bash
# Backup your current file (if recoverable)
cp ~/.task-tracker/tasks.json ~/.task-tracker/tasks.json.backup

# Remove the corrupted file to start fresh
rm ~/.task-tracker/tasks.json

# The tool will create a new empty file on next run
task list
```

### Permission Issues

If you get permission errors:

```bash
# Check file permissions
ls -la ~/.task-tracker/

# Fix permissions if needed
chmod 755 ~/.task-tracker
chmod 644 ~/.task-tracker/tasks.json
```

## Support

For issues and questions, please open an issue on GitHub.
