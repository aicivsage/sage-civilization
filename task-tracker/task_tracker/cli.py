"""
CLI command definitions using Typer.
Handles user input, calls storage operations, formats output.
"""

import typer
from typing import Optional
from rich.console import Console
from rich import print as rprint

from task_tracker.storage import TaskStorage
from task_tracker.utils import create_task_table, format_task_details
from task_tracker.config import get_config


app = typer.Typer(
    help="Simple task tracker for daily tasks",
    add_completion=False
)
console = Console()
storage = TaskStorage()


def version_callback(value: bool):
    """Callback for --version flag"""
    if value:
        config = get_config()
        console.print(f"task-tracker version {config['version']}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """CLI task tracker for managing daily tasks"""
    pass


@app.command()
def add(title: str = typer.Argument(..., help="Task title")):
    """Add a new task"""
    try:
        task = storage.create_task(title)
        console.print()
        console.print("[green]✓ Task added successfully![/green]")
        console.print(f"  [bold]ID:[/bold] {task.id}")
        console.print(f"  [bold]Title:[/bold] {task.title}")
        console.print(f"  [bold]Status:[/bold] {task.status}")
        console.print(f"  [bold]Created:[/bold] {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        console.print()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def list(
    status: Optional[str] = typer.Option(
        "pending",
        "--status",
        help="Filter by status (pending/completed)"
    ),
    all: bool = typer.Option(
        False,
        "--all",
        help="Show all tasks regardless of status"
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        help="Limit number of tasks shown"
    )
):
    """List tasks"""
    try:
        # Determine filter
        filter_status = None if all else status

        # Get tasks
        tasks = storage.list_tasks(status=filter_status)

        # Apply limit if specified
        if limit:
            tasks = tasks[:limit]

        console.print()

        if not tasks:
            if all:
                console.print("[yellow]No tasks found! Add one with 'task add \"Your task here\"'[/yellow]")
            else:
                console.print(f"[yellow]No {status} tasks! Add one with 'task add \"Your task here\"'[/yellow]")
        else:
            # Display header
            if all:
                title = f"All Tasks ({len(tasks)}):"
            else:
                title = f"{status.capitalize()} Tasks ({len(tasks)}):"

            console.print(f"[bold]{title}[/bold]")

            # Create and display table
            table = create_task_table(tasks, show_status=all)
            console.print(table)

        console.print()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def show(task_id: int = typer.Argument(..., help="Task ID")):
    """Show task details"""
    try:
        task = storage.get_task(task_id)

        console.print()

        if not task:
            console.print(f"[red]Error:[/red] Task #{task_id} not found")
            console.print("       Use 'task list --all' to see all tasks")
            console.print()
            raise typer.Exit(1)

        # Display task details
        rprint(format_task_details(task))
        console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def complete(
    task_id: int = typer.Argument(..., help="Task ID"),
    force: bool = typer.Option(
        False,
        "--force",
        help="Update completion time even if already completed"
    )
):
    """Mark task as completed"""
    try:
        task = storage.complete_task(task_id, force=force)

        console.print()

        if not task:
            console.print(f"[red]Error:[/red] Task #{task_id} not found")
            console.print("       Use 'task list --all' to see all tasks")
            console.print()
            raise typer.Exit(1)

        console.print(f"[green]✓ Task #{task.id} marked as completed![/green]")
        console.print(f"  [bold]Title:[/bold] {task.title}")
        console.print(f"  [bold]Completed at:[/bold] {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        console.print()

    except ValueError as e:
        # Handle "already completed" error
        console.print(f"[red]Error:[/red] {e}")
        console.print("       Use --force to update completion time")
        console.print()
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def delete(
    task_id: int = typer.Argument(..., help="Task ID"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt"
    )
):
    """Delete a task"""
    try:
        # Check if task exists first
        task = storage.get_task(task_id)

        if not task:
            console.print()
            console.print(f"[red]Error:[/red] Task #{task_id} not found")
            console.print("       Use 'task list --all' to see all tasks")
            console.print()
            raise typer.Exit(1)

        # Confirm deletion unless --force
        if not force:
            confirm = typer.confirm(
                f"Are you sure you want to delete task #{task_id}?",
                default=False
            )
            if not confirm:
                console.print("[yellow]Deletion cancelled.[/yellow]")
                raise typer.Exit(0)

        # Delete the task
        success = storage.delete_task(task_id)

        console.print()
        if success:
            console.print(f"[green]✓ Task #{task_id} deleted successfully![/green]")
        else:
            console.print(f"[red]Error:[/red] Failed to delete task #{task_id}")
        console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
