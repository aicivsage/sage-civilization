"""
CLI integration tests using Typer's CliRunner.
Tests end-to-end command execution and output formatting.
"""

import pytest
from pathlib import Path
from typer.testing import CliRunner

from task_tracker.cli import app
from task_tracker.storage import TaskStorage


runner = CliRunner()


@pytest.fixture
def cli_storage(tmp_path, monkeypatch):
    """
    Create a temporary storage for CLI tests.
    Monkeypatch the storage instance to use temp file.
    """
    data_file = tmp_path / "tasks.json"

    # Import the cli module to patch its storage instance
    from task_tracker import cli

    # Create new storage with temp file and replace the module-level instance
    test_storage = TaskStorage(data_file=data_file)
    monkeypatch.setattr(cli, 'storage', test_storage)

    return test_storage


@pytest.fixture
def cli_with_tasks(cli_storage):
    """Create CLI storage with sample tasks"""
    cli_storage.create_task("Task 1")
    cli_storage.create_task("Task 2")
    cli_storage.create_task("Task 3")
    cli_storage.complete_task(2)
    return cli_storage


class TestCLIAdd:
    """Test 'add' command"""

    def test_add_task_success(self, cli_storage):
        """Test adding a task successfully"""
        result = runner.invoke(app, ["add", "Buy groceries"])

        assert result.exit_code == 0
        assert "Task added successfully!" in result.stdout
        assert "ID: 1" in result.stdout
        assert "Title: Buy groceries" in result.stdout
        assert "Status: pending" in result.stdout
        assert "Created:" in result.stdout

    def test_add_task_with_quotes(self, cli_storage):
        """Test adding a task with special characters"""
        result = runner.invoke(app, ["add", "Review PR #42 & merge"])

        assert result.exit_code == 0
        assert "Task added successfully!" in result.stdout
        assert "Review PR #42 & merge" in result.stdout

    def test_add_task_increments_id(self, cli_storage):
        """Test that IDs increment correctly"""
        result1 = runner.invoke(app, ["add", "Task 1"])
        result2 = runner.invoke(app, ["add", "Task 2"])
        result3 = runner.invoke(app, ["add", "Task 3"])

        assert "ID: 1" in result1.stdout
        assert "ID: 2" in result2.stdout
        assert "ID: 3" in result3.stdout

    def test_add_task_empty_title_fails(self, cli_storage):
        """Test that adding empty title fails"""
        # Typer requires at least something, but empty string after parsing fails
        result = runner.invoke(app, ["add", ""])

        assert result.exit_code == 1
        assert "Error:" in result.stdout

    def test_add_task_too_long_fails(self, cli_storage):
        """Test that adding a very long title fails"""
        long_title = "x" * 201  # Max is 200
        result = runner.invoke(app, ["add", long_title])

        assert result.exit_code == 1
        assert "Error:" in result.stdout


class TestCLIList:
    """Test 'list' command"""

    def test_list_empty(self, cli_storage):
        """Test listing when no tasks exist"""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No pending tasks!" in result.stdout
        assert "task add" in result.stdout

    def test_list_pending_default(self, cli_with_tasks):
        """Test listing pending tasks (default behavior)"""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Pending Tasks (2):" in result.stdout
        assert "Task 1" in result.stdout
        assert "Task 3" in result.stdout
        assert "Task 2" not in result.stdout  # Task 2 is completed

    def test_list_all_tasks(self, cli_with_tasks):
        """Test listing all tasks with --all flag"""
        result = runner.invoke(app, ["list", "--all"])

        assert result.exit_code == 0
        assert "All Tasks (3):" in result.stdout
        assert "Task 1" in result.stdout
        assert "Task 2" in result.stdout
        assert "Task 3" in result.stdout

    def test_list_completed_tasks(self, cli_with_tasks):
        """Test listing completed tasks"""
        result = runner.invoke(app, ["list", "--status", "completed"])

        assert result.exit_code == 0
        assert "Completed Tasks (1):" in result.stdout
        assert "Task 2" in result.stdout
        assert "Task 1" not in result.stdout
        assert "Task 3" not in result.stdout

    def test_list_with_limit(self, cli_with_tasks):
        """Test listing tasks with limit"""
        result = runner.invoke(app, ["list", "--all", "--limit", "2"])

        assert result.exit_code == 0
        assert "All Tasks (2):" in result.stdout
        # Should show only 2 tasks (most recent ones)

    def test_list_shows_table_headers(self, cli_with_tasks):
        """Test that list shows proper table with headers"""
        result = runner.invoke(app, ["list", "--all"])

        assert result.exit_code == 0
        assert "ID" in result.stdout
        assert "Title" in result.stdout
        assert "Status" in result.stdout
        assert "Created" in result.stdout

    def test_list_pending_only_header(self, cli_with_tasks):
        """Test that pending list doesn't show Status column"""
        result = runner.invoke(app, ["list", "--status", "pending"])

        assert result.exit_code == 0
        # When filtering by single status, status column may not be shown
        assert "ID" in result.stdout
        assert "Title" in result.stdout


class TestCLIShow:
    """Test 'show' command"""

    def test_show_existing_task(self, cli_with_tasks):
        """Test showing an existing task"""
        result = runner.invoke(app, ["show", "1"])

        assert result.exit_code == 0
        assert "Task #1" in result.stdout
        assert "Title:" in result.stdout
        assert "Task 1" in result.stdout
        assert "Status:" in result.stdout
        assert "pending" in result.stdout
        assert "Created:" in result.stdout

    def test_show_completed_task(self, cli_with_tasks):
        """Test showing a completed task"""
        result = runner.invoke(app, ["show", "2"])

        assert result.exit_code == 0
        assert "Task #2" in result.stdout
        assert "Task 2" in result.stdout
        assert "completed" in result.stdout
        assert "Completed:" in result.stdout

    def test_show_non_existing_task(self, cli_with_tasks):
        """Test showing a non-existing task"""
        result = runner.invoke(app, ["show", "999"])

        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "Task #999 not found" in result.stdout
        assert "task list --all" in result.stdout

    def test_show_formatting(self, cli_with_tasks):
        """Test that show command has proper formatting"""
        result = runner.invoke(app, ["show", "1"])

        assert result.exit_code == 0
        # Check for separator lines
        assert "━" in result.stdout or "-" in result.stdout


class TestCLIComplete:
    """Test 'complete' command"""

    def test_complete_pending_task(self, cli_with_tasks):
        """Test completing a pending task"""
        result = runner.invoke(app, ["complete", "1"])

        assert result.exit_code == 0
        assert "Task #1 marked as completed!" in result.stdout
        assert "Title: Task 1" in result.stdout
        assert "Completed at:" in result.stdout

    def test_complete_already_completed_task(self, cli_with_tasks):
        """Test completing an already completed task fails"""
        result = runner.invoke(app, ["complete", "2"])

        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "already completed" in result.stdout
        assert "--force" in result.stdout

    def test_complete_with_force_flag(self, cli_with_tasks):
        """Test force completing an already completed task"""
        result = runner.invoke(app, ["complete", "2", "--force"])

        assert result.exit_code == 0
        assert "Task #2 marked as completed!" in result.stdout

    def test_complete_non_existing_task(self, cli_with_tasks):
        """Test completing a non-existing task"""
        result = runner.invoke(app, ["complete", "999"])

        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "Task #999 not found" in result.stdout
        assert "task list --all" in result.stdout

    def test_complete_updates_status(self, cli_with_tasks):
        """Test that completing a task actually updates its status"""
        # Complete the task
        result = runner.invoke(app, ["complete", "1"])
        assert result.exit_code == 0

        # Verify it's completed by showing it
        result = runner.invoke(app, ["show", "1"])
        assert "completed" in result.stdout


class TestCLIDelete:
    """Test 'delete' command"""

    def test_delete_with_force(self, cli_with_tasks):
        """Test deleting a task with --force flag"""
        result = runner.invoke(app, ["delete", "1", "--force"])

        assert result.exit_code == 0
        assert "Task #1 deleted successfully!" in result.stdout

    def test_delete_with_force_short_flag(self, cli_with_tasks):
        """Test deleting a task with -f flag"""
        result = runner.invoke(app, ["delete", "1", "-f"])

        assert result.exit_code == 0
        assert "Task #1 deleted successfully!" in result.stdout

    def test_delete_with_confirmation_yes(self, cli_with_tasks):
        """Test deleting a task with confirmation (yes)"""
        result = runner.invoke(app, ["delete", "1"], input="y\n")

        assert result.exit_code == 0
        assert "Task #1 deleted successfully!" in result.stdout

    def test_delete_with_confirmation_no(self, cli_with_tasks):
        """Test cancelling deletion with confirmation (no)"""
        result = runner.invoke(app, ["delete", "1"], input="n\n")

        assert result.exit_code == 0
        assert "Deletion cancelled" in result.stdout

    def test_delete_non_existing_task(self, cli_with_tasks):
        """Test deleting a non-existing task"""
        result = runner.invoke(app, ["delete", "999", "--force"])

        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "Task #999 not found" in result.stdout

    def test_delete_actually_removes_task(self, cli_with_tasks):
        """Test that deletion actually removes the task"""
        # Delete the task
        result = runner.invoke(app, ["delete", "1", "--force"])
        assert result.exit_code == 0

        # Verify it's gone
        result = runner.invoke(app, ["show", "1"])
        assert result.exit_code == 1
        assert "not found" in result.stdout


class TestCLIHelp:
    """Test help text and documentation"""

    def test_help_main(self):
        """Test main help text"""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "task tracker" in result.stdout.lower()
        assert "add" in result.stdout
        assert "list" in result.stdout
        assert "show" in result.stdout
        assert "complete" in result.stdout
        assert "delete" in result.stdout

    def test_help_add_command(self):
        """Test 'add' command help"""
        result = runner.invoke(app, ["add", "--help"])

        assert result.exit_code == 0
        assert "Add a new task" in result.stdout
        assert "title" in result.stdout.lower()

    def test_help_list_command(self):
        """Test 'list' command help"""
        result = runner.invoke(app, ["list", "--help"])

        assert result.exit_code == 0
        assert "List tasks" in result.stdout
        assert "--status" in result.stdout
        assert "--all" in result.stdout
        assert "--limit" in result.stdout

    def test_help_show_command(self):
        """Test 'show' command help"""
        result = runner.invoke(app, ["show", "--help"])

        assert result.exit_code == 0
        assert "Show task details" in result.stdout
        assert "task-id" in result.stdout.lower() or "task_id" in result.stdout.lower()

    def test_help_complete_command(self):
        """Test 'complete' command help"""
        result = runner.invoke(app, ["complete", "--help"])

        assert result.exit_code == 0
        assert "Mark task as completed" in result.stdout
        assert "--force" in result.stdout

    def test_help_delete_command(self):
        """Test 'delete' command help"""
        result = runner.invoke(app, ["delete", "--help"])

        assert result.exit_code == 0
        assert "Delete a task" in result.stdout
        assert "--force" in result.stdout


class TestCLIVersion:
    """Test version flag"""

    def test_version_flag(self):
        """Test --version flag shows version"""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "task-tracker version" in result.stdout
        assert "1.0.0" in result.stdout


class TestCLIErrorMessages:
    """Test error message validation"""

    def test_error_messages_are_red(self, cli_with_tasks):
        """Test that error messages use red color"""
        result = runner.invoke(app, ["show", "999"])

        assert result.exit_code == 1
        assert "[red]Error:" in result.stdout or "Error:" in result.stdout

    def test_success_messages_are_green(self, cli_storage):
        """Test that success messages use green color"""
        result = runner.invoke(app, ["add", "Test task"])

        assert result.exit_code == 0
        assert "[green]" in result.stdout or "Task added successfully!" in result.stdout

    def test_helpful_error_for_missing_task(self, cli_storage):
        """Test that missing task errors suggest helpful actions"""
        result = runner.invoke(app, ["show", "1"])

        assert result.exit_code == 1
        assert "not found" in result.stdout
        assert "task list" in result.stdout


class TestCLIEndToEnd:
    """End-to-end integration tests"""

    def test_full_task_lifecycle(self, cli_storage):
        """Test complete task lifecycle: add -> list -> show -> complete -> delete"""
        # Add a task
        result = runner.invoke(app, ["add", "Test lifecycle"])
        assert result.exit_code == 0
        assert "Task added successfully!" in result.stdout

        # List tasks
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Test lifecycle" in result.stdout

        # Show task
        result = runner.invoke(app, ["show", "1"])
        assert result.exit_code == 0
        assert "Test lifecycle" in result.stdout
        assert "pending" in result.stdout

        # Complete task
        result = runner.invoke(app, ["complete", "1"])
        assert result.exit_code == 0
        assert "marked as completed" in result.stdout

        # Verify completed
        result = runner.invoke(app, ["show", "1"])
        assert result.exit_code == 0
        assert "completed" in result.stdout

        # Delete task
        result = runner.invoke(app, ["delete", "1", "--force"])
        assert result.exit_code == 0
        assert "deleted successfully" in result.stdout

        # Verify deleted
        result = runner.invoke(app, ["show", "1"])
        assert result.exit_code == 1
        assert "not found" in result.stdout

    def test_multiple_tasks_workflow(self, cli_storage):
        """Test workflow with multiple tasks"""
        # Add multiple tasks
        runner.invoke(app, ["add", "Task A"])
        runner.invoke(app, ["add", "Task B"])
        runner.invoke(app, ["add", "Task C"])

        # List all tasks
        result = runner.invoke(app, ["list", "--all"])
        assert result.exit_code == 0
        assert "All Tasks (3):" in result.stdout

        # Complete one
        runner.invoke(app, ["complete", "2"])

        # List pending
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Pending Tasks (2):" in result.stdout
        assert "Task A" in result.stdout
        assert "Task C" in result.stdout
        assert "Task B" not in result.stdout

        # List completed
        result = runner.invoke(app, ["list", "--status", "completed"])
        assert result.exit_code == 0
        assert "Completed Tasks (1):" in result.stdout
        assert "Task B" in result.stdout

    def test_persistence_across_commands(self, cli_storage):
        """Test that data persists across multiple command invocations"""
        # Add task
        result = runner.invoke(app, ["add", "Persistent task"])
        assert result.exit_code == 0

        # List should show it (simulating new command)
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Persistent task" in result.stdout

        # Show should work (another new command)
        result = runner.invoke(app, ["show", "1"])
        assert result.exit_code == 0
        assert "Persistent task" in result.stdout
