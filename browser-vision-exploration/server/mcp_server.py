#!/usr/bin/env python3
"""
Browser Vision MCP Server

Vision-powered browser automation for AI agents via Model Context Protocol
"""

import asyncio
import sys
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

from session_manager import SessionManager
from playwright_controller import BrowserController


# Tool argument models
class LaunchBrowserArgs(BaseModel):
    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width in pixels")
    viewport_height: int = Field(default=1080, description="Viewport height in pixels")


class NavigateArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    url: str = Field(description="URL to navigate to")
    wait_until: str = Field(default="networkidle", description="When to consider navigation complete")
    capture_screenshot: bool = Field(default=True, description="Capture screenshot after navigation")


class ClickArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    selector: str = Field(description="CSS selector for element to click")
    wait_for_navigation: bool = Field(default=False, description="Wait for navigation after click")
    capture_before: bool = Field(default=True, description="Capture screenshot before click")
    capture_after: bool = Field(default=True, description="Capture screenshot after click")


class TypeTextArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    selector: str = Field(description="CSS selector for input element")
    text: str = Field(description="Text to type")
    press_enter: bool = Field(default=False, description="Press Enter after typing")
    capture_after: bool = Field(default=True, description="Capture screenshot after typing")


class CaptureScreenshotArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    full_page: bool = Field(default=False, description="Capture full scrollable page")
    label: Optional[str] = Field(default=None, description="Optional label for screenshot")


class GetConsoleLogsArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    log_types: Optional[list] = Field(default=None, description="Filter by log types (e.g., ['error', 'warning'])")


class EvaluateJsArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    script: str = Field(description="JavaScript code to execute")
    capture_screenshot: bool = Field(default=False, description="Capture screenshot after execution")


class GetElementInfoArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    selector: str = Field(description="CSS selector for element")


class GetSessionStateArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")


class CloseSessionArgs(BaseModel):
    session_id: str = Field(description="Browser session ID")
    archive: bool = Field(default=True, description="Archive session data")


# Initialize server
app = Server("browser-vision")

# Initialize managers
session_manager = SessionManager()
browser_controller = BrowserController(session_manager)


# Define tools
TOOLS = [
    Tool(
        name="launch_browser",
        description="Launch a new browser session with Chromium. Returns session_id and screenshot directory.",
        inputSchema=LaunchBrowserArgs.model_json_schema()
    ),
    Tool(
        name="navigate",
        description="Navigate to a URL and optionally capture screenshot. Returns page info, screenshot path, and console errors.",
        inputSchema=NavigateArgs.model_json_schema()
    ),
    Tool(
        name="click",
        description="Click an element by CSS selector. Captures before/after screenshots. Returns element info and screenshot paths.",
        inputSchema=ClickArgs.model_json_schema()
    ),
    Tool(
        name="type_text",
        description="Type text into an input field. Returns screenshot path after typing.",
        inputSchema=TypeTextArgs.model_json_schema()
    ),
    Tool(
        name="capture_screenshot",
        description="Manually capture a screenshot of current page state. Returns screenshot metadata.",
        inputSchema=CaptureScreenshotArgs.model_json_schema()
    ),
    Tool(
        name="get_console_logs",
        description="Get browser console logs (errors, warnings, logs). Returns list of console messages.",
        inputSchema=GetConsoleLogsArgs.model_json_schema()
    ),
    Tool(
        name="evaluate_js",
        description="Execute JavaScript in the browser context. Returns result and optional screenshot.",
        inputSchema=EvaluateJsArgs.model_json_schema()
    ),
    Tool(
        name="get_element_info",
        description="Get detailed information about an element (visibility, text, bounding box, etc.).",
        inputSchema=GetElementInfoArgs.model_json_schema()
    ),
    Tool(
        name="get_session_state",
        description="Get comprehensive session state (URL, screenshot count, console errors, etc.).",
        inputSchema=GetSessionStateArgs.model_json_schema()
    ),
    Tool(
        name="close_session",
        description="Close browser session and optionally archive data.",
        inputSchema=CloseSessionArgs.model_json_schema()
    )
]


# Tool handlers
@app.list_tools()
async def list_tools():
    """List available tools"""
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    import json

    try:
        if name == "launch_browser":
            args = LaunchBrowserArgs(**arguments)
            result = await browser_controller.launch_browser(
                viewport_width=args.viewport_width,
                viewport_height=args.viewport_height,
                headless=args.headless
            )

        elif name == "navigate":
            args = NavigateArgs(**arguments)
            result = await browser_controller.navigate(
                session_id=args.session_id,
                url=args.url,
                wait_until=args.wait_until,
                capture_screenshot=args.capture_screenshot
            )

        elif name == "click":
            args = ClickArgs(**arguments)
            result = await browser_controller.click(
                session_id=args.session_id,
                selector=args.selector,
                wait_for_navigation=args.wait_for_navigation,
                capture_before=args.capture_before,
                capture_after=args.capture_after
            )

        elif name == "type_text":
            args = TypeTextArgs(**arguments)
            result = await browser_controller.type_text(
                session_id=args.session_id,
                selector=args.selector,
                text=args.text,
                press_enter=args.press_enter,
                capture_after=args.capture_after
            )

        elif name == "capture_screenshot":
            args = CaptureScreenshotArgs(**arguments)
            result = await browser_controller.capture_screenshot(
                session_id=args.session_id,
                full_page=args.full_page,
                label=args.label
            )

        elif name == "get_console_logs":
            args = GetConsoleLogsArgs(**arguments)
            result = await browser_controller.get_console_logs(
                session_id=args.session_id,
                log_types=args.log_types
            )

        elif name == "evaluate_js":
            args = EvaluateJsArgs(**arguments)
            result = await browser_controller.evaluate_js(
                session_id=args.session_id,
                script=args.script,
                capture_screenshot=args.capture_screenshot
            )

        elif name == "get_element_info":
            args = GetElementInfoArgs(**arguments)
            result = await browser_controller.get_element_info(
                session_id=args.session_id,
                selector=args.selector
            )

        elif name == "get_session_state":
            args = GetSessionStateArgs(**arguments)
            result = await browser_controller.get_session_state(
                session_id=args.session_id
            )

        elif name == "close_session":
            args = CloseSessionArgs(**arguments)
            result = await browser_controller.close_session(
                session_id=args.session_id,
                archive=args.archive
            )

        else:
            raise ValueError(f"Unknown tool: {name}")

        # Return result as TextContent
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "detail": error_detail
            }, indent=2)
        )]


async def main():
    """Main entry point"""
    # Initialize Playwright
    await browser_controller.initialize()

    try:
        # Run MCP server
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    finally:
        # Cleanup
        await browser_controller.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
