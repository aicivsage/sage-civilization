"""
Playwright Controller - Manages browser automation and interactions
"""

from typing import Dict, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from pathlib import Path

from session_manager import SessionManager, BrowserSession
from screenshot_manager import ScreenshotManager
from console_capture import ConsoleCapture


class BrowserController:
    """High-level browser controller integrating Playwright with our systems"""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.playwright = None
        self.browsers: Dict[str, Browser] = {}
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
        self.screenshot_managers: Dict[str, ScreenshotManager] = {}
        self.console_captures: Dict[str, ConsoleCapture] = {}

    async def initialize(self):
        """Initialize Playwright"""
        self.playwright = await async_playwright().start()

    async def shutdown(self):
        """Shutdown Playwright and close all browsers"""
        for browser in self.browsers.values():
            await browser.close()

        if self.playwright:
            await self.playwright.stop()

    async def launch_browser(
        self,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        headless: bool = True
    ) -> Dict:
        """
        Launch a new browser session

        Returns:
            dict with session_id, screenshot_dir, status
        """
        # Create session
        session = self.session_manager.create_session(
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            headless=headless
        )

        session_id = session.session_id

        # Launch browser
        browser = await self.playwright.chromium.launch(
            headless=headless,
            args=["--enable-logging", "--v=1"]  # Enable logging for console capture
        )

        # Create context
        context = await browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height}
        )

        # Create page
        page = await context.new_page()

        # Store references
        self.browsers[session_id] = browser
        self.contexts[session_id] = context
        self.pages[session_id] = page

        # Set up screenshot manager
        session_dir = self.session_manager.get_session_dir(session_id)
        self.screenshot_managers[session_id] = ScreenshotManager(session_dir)

        # Set up console capture
        console_capture = ConsoleCapture(session_dir)
        await console_capture.setup(page)
        self.console_captures[session_id] = console_capture

        return {
            "session_id": session_id,
            "browser_type": "chromium",
            "screenshot_dir": str(session_dir / "screenshots"),
            "viewport": {"width": viewport_width, "height": viewport_height},
            "headless": headless,
            "status": "ready"
        }

    async def navigate(
        self,
        session_id: str,
        url: str,
        wait_until: str = "networkidle",
        capture_screenshot: bool = True
    ) -> Dict:
        """
        Navigate to URL

        Args:
            session_id: Browser session ID
            url: URL to navigate to
            wait_until: When to consider navigation succeeded
            capture_screenshot: Whether to auto-capture screenshot

        Returns:
            dict with url, title, screenshot_path, console_errors
        """
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        # Navigate
        await page.goto(url, wait_until=wait_until)

        # Update session URL
        self.session_manager.update_session_url(session_id, url)

        # Capture screenshot if requested
        screenshot_path = None
        if capture_screenshot:
            screenshot_manager = self.screenshot_managers.get(session_id)
            screenshot_meta = await screenshot_manager.capture_screenshot(
                page,
                label="navigation"
            )
            screenshot_path = screenshot_meta["filepath"]

        # Get console errors
        console_capture = self.console_captures.get(session_id)
        console_errors = console_capture.get_logs(log_types=["error"])

        return {
            "url": page.url,
            "title": await page.title(),
            "screenshot_path": screenshot_path,
            "console_errors": console_errors,
            "timestamp": screenshot_meta["timestamp"] if screenshot_path else None
        }

    async def click(
        self,
        session_id: str,
        selector: str,
        wait_for_navigation: bool = False,
        capture_before: bool = True,
        capture_after: bool = True
    ) -> Dict:
        """
        Click an element

        Returns:
            dict with action, selector, screenshots, navigation_occurred
        """
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        screenshot_manager = self.screenshot_managers.get(session_id)

        # Capture before screenshot
        screenshot_before = None
        if capture_before:
            meta = await screenshot_manager.capture_screenshot(page, label="before-click")
            screenshot_before = meta["filepath"]

        # Get element text for metadata
        element = await page.wait_for_selector(selector)
        element_text = await element.text_content()

        # Click
        if wait_for_navigation:
            async with page.expect_navigation():
                await page.click(selector)
            navigation_occurred = True
        else:
            await page.click(selector)
            navigation_occurred = False

        # Wait a moment for UI updates
        await page.wait_for_timeout(500)

        # Capture after screenshot
        screenshot_after = None
        if capture_after:
            meta = await screenshot_manager.capture_screenshot(page, label="after-click")
            screenshot_after = meta["filepath"]

        return {
            "action": "click",
            "selector": selector,
            "element_text": element_text,
            "screenshot_before": screenshot_before,
            "screenshot_after": screenshot_after,
            "navigation_occurred": navigation_occurred,
            "current_url": page.url
        }

    async def type_text(
        self,
        session_id: str,
        selector: str,
        text: str,
        press_enter: bool = False,
        capture_after: bool = True
    ) -> Dict:
        """Type text into an input field"""
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        # Type text
        await page.fill(selector, text)

        if press_enter:
            await page.press(selector, "Enter")

        # Capture screenshot
        screenshot_path = None
        if capture_after:
            screenshot_manager = self.screenshot_managers.get(session_id)
            meta = await screenshot_manager.capture_screenshot(page, label="after-type")
            screenshot_path = meta["filepath"]

        return {
            "action": "type",
            "selector": selector,
            "text": text,
            "pressed_enter": press_enter,
            "screenshot_path": screenshot_path
        }

    async def capture_screenshot(
        self,
        session_id: str,
        full_page: bool = False,
        label: Optional[str] = None
    ) -> Dict:
        """Manually capture a screenshot"""
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        screenshot_manager = self.screenshot_managers.get(session_id)
        return await screenshot_manager.capture_screenshot(
            page,
            label=label,
            full_page=full_page
        )

    async def get_console_logs(
        self,
        session_id: str,
        log_types: Optional[list] = None
    ) -> Dict:
        """Get console logs for session"""
        console_capture = self.console_captures.get(session_id)
        if not console_capture:
            return {"logs": [], "error_count": 0, "warning_count": 0}

        logs = console_capture.get_logs(log_types=log_types)

        return {
            "logs": logs,
            "error_count": console_capture.get_error_count(),
            "warning_count": console_capture.get_warning_count()
        }

    async def evaluate_js(
        self,
        session_id: str,
        script: str,
        capture_screenshot: bool = False
    ) -> Dict:
        """Execute JavaScript in browser context"""
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        result = await page.evaluate(script)

        screenshot_path = None
        if capture_screenshot:
            screenshot_manager = self.screenshot_managers.get(session_id)
            meta = await screenshot_manager.capture_screenshot(page, label="after-js")
            screenshot_path = meta["filepath"]

        return {
            "result": result,
            "screenshot_path": screenshot_path
        }

    async def get_element_info(
        self,
        session_id: str,
        selector: str
    ) -> Dict:
        """Get detailed element information"""
        page = self.pages.get(session_id)
        if not page:
            raise ValueError(f"No active page for session {session_id}")

        try:
            element = await page.wait_for_selector(selector, timeout=5000)

            # Get element properties
            text = await element.text_content()
            is_visible = await element.is_visible()
            is_enabled = await element.is_enabled()
            bounding_box = await element.bounding_box()

            return {
                "exists": True,
                "visible": is_visible,
                "enabled": is_enabled,
                "text": text,
                "bounding_box": bounding_box
            }
        except Exception as e:
            return {
                "exists": False,
                "error": str(e)
            }

    async def get_session_state(self, session_id: str) -> Dict:
        """Get comprehensive session state"""
        session = self.session_manager.get_session(session_id)
        page = self.pages.get(session_id)

        if not session or not page:
            return {"error": f"Session {session_id} not found"}

        screenshot_manager = self.screenshot_managers.get(session_id)
        latest_screenshot = screenshot_manager.get_latest_screenshot()

        console_capture = self.console_captures.get(session_id)

        return {
            "session_id": session_id,
            "current_url": page.url,
            "title": await page.title(),
            "screenshot_count": session.screenshot_count,
            "latest_screenshot": latest_screenshot.get("filepath") if latest_screenshot else None,
            "console_error_count": console_capture.get_error_count(),
            "console_warning_count": console_capture.get_warning_count(),
            "viewport": {
                "width": session.viewport_width,
                "height": session.viewport_height
            },
            "created_at": session.created_at
        }

    async def close_session(self, session_id: str, archive: bool = True) -> Dict:
        """Close browser session"""
        # Close browser components
        if session_id in self.pages:
            await self.pages[session_id].close()
            del self.pages[session_id]

        if session_id in self.contexts:
            await self.contexts[session_id].close()
            del self.contexts[session_id]

        if session_id in self.browsers:
            await self.browsers[session_id].close()
            del self.browsers[session_id]

        # Clean up managers
        if session_id in self.screenshot_managers:
            del self.screenshot_managers[session_id]

        if session_id in self.console_captures:
            del self.console_captures[session_id]

        # Close session in session manager
        self.session_manager.close_session(session_id)

        return {
            "session_id": session_id,
            "status": "closed",
            "archived": archive
        }
