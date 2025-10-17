"""
Session Manager - Handles browser session lifecycle and state
"""

import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


@dataclass
class BrowserSession:
    """Represents an active browser session"""
    session_id: str
    created_at: str
    viewport_width: int
    viewport_height: int
    headless: bool
    current_url: Optional[str] = None
    screenshot_count: int = 0

    def to_dict(self):
        return asdict(self)


class SessionManager:
    """Manages browser sessions and their metadata"""

    def __init__(self, base_dir: str = "/tmp/browser-vision"):
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        self.active_sessions: Dict[str, BrowserSession] = {}

    def create_session(
        self,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        headless: bool = True
    ) -> BrowserSession:
        """Create a new browser session"""
        session_id = str(uuid.uuid4())

        session = BrowserSession(
            session_id=session_id,
            created_at=datetime.utcnow().isoformat(),
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            headless=headless
        )

        # Create session directory structure
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        (session_dir / "screenshots").mkdir(exist_ok=True)

        # Initialize metadata file
        metadata = {
            "session": session.to_dict(),
            "screenshots": [],
            "console_logs": []
        }

        with open(session_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        self.active_sessions[session_id] = session

        return session

    def get_session(self, session_id: str) -> Optional[BrowserSession]:
        """Get session by ID"""
        return self.active_sessions.get(session_id)

    def get_session_dir(self, session_id: str) -> Path:
        """Get session directory path"""
        return self.sessions_dir / session_id

    def update_session_url(self, session_id: str, url: str):
        """Update current URL for session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id].current_url = url
            self._save_session_metadata(session_id)

    def increment_screenshot_count(self, session_id: str):
        """Increment screenshot counter"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id].screenshot_count += 1
            return self.active_sessions[session_id].screenshot_count
        return 0

    def close_session(self, session_id: str):
        """Close and archive session"""
        if session_id in self.active_sessions:
            # Mark session as closed in metadata
            session_dir = self.get_session_dir(session_id)
            metadata_path = session_dir / "metadata.json"

            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

                metadata["session"]["closed_at"] = datetime.utcnow().isoformat()

                with open(metadata_path, "w") as f:
                    json.dump(metadata, f, indent=2)

            del self.active_sessions[session_id]

    def _save_session_metadata(self, session_id: str):
        """Save session metadata to disk"""
        session = self.active_sessions.get(session_id)
        if not session:
            return

        session_dir = self.get_session_dir(session_id)
        metadata_path = session_dir / "metadata.json"

        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            metadata["session"] = session.to_dict()

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
