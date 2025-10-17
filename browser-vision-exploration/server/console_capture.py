"""
Console Capture - Captures browser console output via CDP
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from playwright.async_api import Page, CDPSession


class ConsoleCapture:
    """Captures and stores browser console output"""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.console_log_path = session_dir / "console.log"
        self.metadata_path = session_dir / "metadata.json"

        self.console_logs: List[Dict] = []

    async def setup(self, page: Page):
        """Set up console event listeners"""

        # Standard console event listener
        page.on("console", self._handle_console_message)

        # Page error listener (for uncaught exceptions)
        page.on("pageerror", self._handle_page_error)

        # Try to set up CDP for more detailed logs
        try:
            # Get CDP session
            cdp_session = await page.context.new_cdp_session(page)

            # Enable Log and Runtime domains
            await cdp_session.send("Log.enable")
            await cdp_session.send("Runtime.enable")

            # Listen for CDP log events
            cdp_session.on("Log.entryAdded", self._handle_cdp_log_entry)
            cdp_session.on("Runtime.consoleAPICalled", self._handle_cdp_console_api)
            cdp_session.on("Runtime.exceptionThrown", self._handle_cdp_exception)

        except Exception as e:
            # CDP might not be available in all contexts, fallback to standard listeners
            self._log_to_file({
                "type": "warning",
                "text": f"CDP setup failed, using standard listeners only: {e}",
                "timestamp": datetime.utcnow().isoformat()
            })

    def _handle_console_message(self, msg):
        """Handle standard Playwright console messages"""
        log_entry = {
            "type": msg.type,
            "text": msg.text,
            "location": msg.location,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "playwright"
        }

        self._store_log(log_entry)

    def _handle_page_error(self, error):
        """Handle page errors (uncaught exceptions)"""
        log_entry = {
            "type": "error",
            "text": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "pageerror"
        }

        self._store_log(log_entry)

    def _handle_cdp_log_entry(self, entry):
        """Handle CDP Log.entryAdded events"""
        log_entry = {
            "type": entry.get("entry", {}).get("level", "log"),
            "text": entry.get("entry", {}).get("text", ""),
            "url": entry.get("entry", {}).get("url", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "cdp-log"
        }

        self._store_log(log_entry)

    def _handle_cdp_console_api(self, event):
        """Handle CDP Runtime.consoleAPICalled events"""
        args = event.get("args", [])
        text_parts = []

        for arg in args:
            if arg.get("type") == "string":
                text_parts.append(arg.get("value", ""))
            else:
                # For non-string types, use description
                text_parts.append(arg.get("description", str(arg)))

        log_entry = {
            "type": event.get("type", "log"),
            "text": " ".join(text_parts),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "cdp-console-api",
            "stack_trace": event.get("stackTrace")
        }

        self._store_log(log_entry)

    def _handle_cdp_exception(self, event):
        """Handle CDP Runtime.exceptionThrown events"""
        exception_details = event.get("exceptionDetails", {})

        log_entry = {
            "type": "error",
            "text": exception_details.get("text", "Unknown exception"),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "cdp-exception",
            "stack_trace": exception_details.get("stackTrace"),
            "url": exception_details.get("url"),
            "line_number": exception_details.get("lineNumber"),
            "column_number": exception_details.get("columnNumber")
        }

        self._store_log(log_entry)

    def _store_log(self, log_entry: dict):
        """Store log entry in memory and write to disk"""
        self.console_logs.append(log_entry)
        self._log_to_file(log_entry)
        self._update_metadata(log_entry)

    def _log_to_file(self, log_entry: dict):
        """Append log entry to console.log file"""
        with open(self.console_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def _update_metadata(self, log_entry: dict):
        """Update metadata.json with console log summary"""
        if not self.metadata_path.exists():
            return

        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)

        metadata.setdefault("console_logs", []).append(log_entry)

        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def get_logs(
        self,
        log_types: List[str] = None,
        limit: int = None
    ) -> List[Dict]:
        """
        Get console logs with optional filtering

        Args:
            log_types: Filter by log type (e.g., ['error', 'warning'])
            limit: Maximum number of logs to return (most recent)

        Returns:
            List of log entries
        """
        logs = self.console_logs

        # Filter by type if specified
        if log_types:
            logs = [log for log in logs if log.get("type") in log_types]

        # Apply limit (most recent N logs)
        if limit:
            logs = logs[-limit:]

        return logs

    def get_error_count(self) -> int:
        """Get count of error logs"""
        return len([log for log in self.console_logs if log.get("type") == "error"])

    def get_warning_count(self) -> int:
        """Get count of warning logs"""
        return len([log for log in self.console_logs if log.get("type") in ["warn", "warning"]])
