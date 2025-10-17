"""
Screenshot Manager - Handles screenshot capture and metadata
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from playwright.async_api import Page


class ScreenshotManager:
    """Manages screenshot capture and metadata tracking"""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.screenshots_dir = session_dir / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_path = session_dir / "metadata.json"

    async def capture_screenshot(
        self,
        page: Page,
        label: Optional[str] = None,
        full_page: bool = False
    ) -> Dict[str, any]:
        """
        Capture screenshot and save with metadata

        Returns:
            dict with screenshot_path, sequence, timestamp, etc.
        """
        # Load current metadata
        metadata = self._load_metadata()
        sequence = len(metadata.get("screenshots", [])) + 1

        # Generate filename
        label_part = f"-{label}" if label else ""
        filename = f"{sequence:03d}{label_part}.png"
        filepath = self.screenshots_dir / filename

        # Capture screenshot
        await page.screenshot(path=str(filepath), full_page=full_page)

        # Get file size
        file_size = filepath.stat().st_size

        # Create screenshot metadata
        screenshot_meta = {
            "sequence": sequence,
            "filename": filename,
            "filepath": str(filepath),
            "label": label,
            "url": page.url,
            "timestamp": datetime.utcnow().isoformat(),
            "viewport_width": page.viewport_size.get("width"),
            "viewport_height": page.viewport_size.get("height"),
            "full_page": full_page,
            "file_size_bytes": file_size
        }

        # Update metadata
        metadata.setdefault("screenshots", []).append(screenshot_meta)
        self._save_metadata(metadata)

        return screenshot_meta

    def get_latest_screenshot(self) -> Optional[Dict[str, any]]:
        """Get metadata for the most recent screenshot"""
        metadata = self._load_metadata()
        screenshots = metadata.get("screenshots", [])
        return screenshots[-1] if screenshots else None

    def get_screenshot_by_sequence(self, sequence: int) -> Optional[Dict[str, any]]:
        """Get screenshot metadata by sequence number"""
        metadata = self._load_metadata()
        screenshots = metadata.get("screenshots", [])

        for screenshot in screenshots:
            if screenshot.get("sequence") == sequence:
                return screenshot

        return None

    def list_screenshots(self) -> list:
        """List all screenshots for this session"""
        metadata = self._load_metadata()
        return metadata.get("screenshots", [])

    def _load_metadata(self) -> dict:
        """Load metadata from disk"""
        if self.metadata_path.exists():
            with open(self.metadata_path, "r") as f:
                return json.load(f)
        return {}

    def _save_metadata(self, metadata: dict):
        """Save metadata to disk"""
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
