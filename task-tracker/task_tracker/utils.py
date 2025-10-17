"""
Utility functions for formatting and display.
"""

from datetime import datetime
from typing import List
from rich.table import Table
from rich.console import Console

from task_tracker.models import Task


def format_datetime(dt: datetime) -> str:
    """
    Format datetime for display.

    Args:
        dt: Datetime to format

    Returns:
        Formatted string in YYYY-MM-DD HH:MM format
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def create_task_table(tasks: List[Task], show_status: bool = False) -> Table:
    """
    Create Rich table for task list.

    Args:
        tasks: List of tasks to display
        show_status: Whether to include status column (for --all view)

    Returns:
        Configured Rich Table object
    """
    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="white")
    if show_status:
        table.add_column("Status", style="yellow")
    table.add_column("Created", style="green")

    for task in tasks:
        row = [
            str(task.id),
            task.title,
        ]
        if show_status:
            status_style = "green" if task.status == "completed" else "yellow"
            row.append(f"[{status_style}]{task.status}[/{status_style}]")
        row.append(format_datetime(task.created_at))

        table.add_row(*row)

    return table


def format_task_details(task: Task) -> str:
    """
    Format task details for the 'show' command.

    Args:
        task: Task to format

    Returns:
        Formatted multi-line string with task details
    """
    completed_str = format_datetime(task.completed_at) if task.completed_at else "-"

    lines = [
        f"[bold cyan]Task #{task.id}[/bold cyan]",
        "━" * 60,
        f"[bold]Title:[/bold]      {task.title}",
        f"[bold]Status:[/bold]     {task.status}",
        f"[bold]Created:[/bold]    {format_datetime(task.created_at)}",
        f"[bold]Completed:[/bold]  {completed_str}",
        "━" * 60,
    ]

    return "\n".join(lines)
