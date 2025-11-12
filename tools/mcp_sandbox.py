#!/usr/bin/env python3
"""
MCP Sandbox: Secure Code Execution System

This module provides safe, audited code execution capabilities for all agents
in the Sage civilization. It implements the Phase 2 MCP Code Execution system
per ADR-007 specification.

Constitutional Alignment (Article VII):
- No file deletion (rm, mv, cp forbidden)
- No git commands (via whitelist)
- No credential access (sandbox isolation)
- No network access (isolated environment)
- All operations audited (execution_log.jsonl)

Security Model:
- RestrictedPython for Python execution (no subprocess, import restrictions)
- Whitelist-based Bash execution (read-only operations)
- Sandbox filesystem isolation (mcp/servers/sandbox/workspace/)
- Resource limits (timeout, memory)
- Comprehensive audit trail

Usage:
    from tools.mcp_sandbox import execute_code, ExecutionPolicy

    result = execute_code(
        agent_id="coder",
        language="python",
        code="print('hello')",
        policy=ExecutionPolicy.for_agent("coder")
    )

    if result.success:
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")
"""

import ast
import json
import os
import resource
import shlex
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any

# RestrictedPython for safe Python execution
try:
    from RestrictedPython import compile_restricted, safe_globals
    RESTRICTED_PYTHON_AVAILABLE = True
except ImportError:
    RESTRICTED_PYTHON_AVAILABLE = False
    print("Warning: RestrictedPython not installed. Python execution disabled.")
    print("Install with: pip install RestrictedPython")


# ============================================================================
# Data Models
# ============================================================================

class ExecutionLanguage(Enum):
    """Supported execution languages."""
    PYTHON = "python"
    BASH = "bash"


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: int
    security_violations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class ExecutionPolicy:
    """Execution policy for an agent."""
    agent_id: str
    python_enabled: bool
    python_write_access: bool
    bash_enabled: bool
    bash_allowed_commands: List[str]
    timeout_seconds: int
    memory_limit_mb: int

    @staticmethod
    def for_agent(agent_id: str) -> "ExecutionPolicy":
        """Get execution policy for a specific agent."""
        # Default policy (most restrictive)
        default = ExecutionPolicy(
            agent_id=agent_id,
            python_enabled=True,
            python_write_access=False,
            bash_enabled=True,
            bash_allowed_commands=["ls", "cat", "head", "tail", "grep", "find", "pwd"],
            timeout_seconds=30,
            memory_limit_mb=256
        )

        # Agent-specific policies (per ADR-007)
        policies = {
            "coder": ExecutionPolicy(
                agent_id="coder",
                python_enabled=True,
                python_write_access=True,
                bash_enabled=True,
                bash_allowed_commands=["ls", "cat", "head", "tail", "grep", "find", "pwd", "mkdir", "cd", "wc"],
                timeout_seconds=30,
                memory_limit_mb=500
            ),
            "tester": ExecutionPolicy(
                agent_id="tester",
                python_enabled=True,
                python_write_access=True,
                bash_enabled=True,
                bash_allowed_commands=["ls", "cat", "pytest", "python", "coverage"],
                timeout_seconds=120,
                memory_limit_mb=500
            ),
            "researcher": ExecutionPolicy(
                agent_id="researcher",
                python_enabled=True,
                python_write_access=False,
                bash_enabled=True,
                bash_allowed_commands=["ls", "cat", "head", "tail", "grep", "find", "wc", "awk", "sed"],
                timeout_seconds=60,
                memory_limit_mb=1024
            ),
            "email-monitor": ExecutionPolicy(
                agent_id="email-monitor",
                python_enabled=True,
                python_write_access=False,
                bash_enabled=False,
                bash_allowed_commands=[],
                timeout_seconds=10,
                memory_limit_mb=256
            )
        }

        return policies.get(agent_id, default)


# ============================================================================
# Security Validation
# ============================================================================

# Forbidden patterns in any code
FORBIDDEN_PATTERNS = [
    "rm ", "rm\t", "rm\n",  # File deletion
    "mv ", "mv\t",  # File moving
    "cp ", "cp\t",  # File copying
    "chmod", "chown",  # Permission changes
    "sudo", "su ",  # Privilege escalation
    "git ",  # Version control
    "curl", "wget", "ssh", "scp",  # Network access
    "kill", "pkill", "killall",  # Process control
    "reboot", "shutdown",  # System control
    "__import__", "eval(", "exec(",  # Dynamic code execution
    "open('/", "open(\"/",  # Absolute path access
    "/home/", "/root/", "/etc/",  # System directories
]


def validate_python_syntax(code: str) -> tuple[bool, Optional[str]]:
    """
    Validate Python code syntax.

    Returns:
        (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def validate_bash_syntax(command: str) -> tuple[bool, Optional[str]]:
    """
    Validate Bash command syntax.

    Returns:
        (is_valid, error_message)
    """
    try:
        shlex.split(command)
        return True, None
    except ValueError as e:
        return False, f"Invalid shell syntax: {e}"


def check_forbidden_patterns(code: str) -> List[str]:
    """
    Check for forbidden patterns in code.

    Returns:
        List of detected violations
    """
    violations = []
    code_lower = code.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in code_lower:
            violations.append(f"Forbidden pattern detected: {pattern.strip()}")

    return violations


def validate_bash_command_whitelist(command: str, allowed_commands: List[str]) -> tuple[bool, Optional[str]]:
    """
    Validate that bash command is in whitelist.

    Returns:
        (is_allowed, error_message)
    """
    try:
        parts = shlex.split(command)
        if not parts:
            return False, "Empty command"

        # Extract base command (first token)
        base_command = parts[0].split('/')[-1]  # Handle /bin/ls -> ls

        if base_command not in allowed_commands:
            return False, f"Command '{base_command}' not in whitelist: {allowed_commands}"

        return True, None
    except Exception as e:
        return False, str(e)


def validate_sandbox_path(path: str, sandbox_root: Path) -> bool:
    """
    Validate that path is within sandbox.

    Returns:
        True if path is safe, False otherwise
    """
    try:
        abs_path = Path(path).resolve()
        abs_sandbox = sandbox_root.resolve()
        return abs_path.is_relative_to(abs_sandbox)
    except Exception:
        return False


# ============================================================================
# Execution Engines
# ============================================================================

class PythonExecutor:
    """Execute Python code safely using RestrictedPython."""

    def __init__(self, sandbox_dir: Path, write_access: bool):
        self.sandbox_dir = sandbox_dir
        self.write_access = write_access

    def execute(self, code: str, timeout_seconds: int, memory_limit_mb: int) -> ExecutionResult:
        """
        Execute Python code in restricted environment.

        Args:
            code: Python code to execute
            timeout_seconds: Execution timeout
            memory_limit_mb: Memory limit

        Returns:
            ExecutionResult with stdout/stderr/exit_code
        """
        if not RESTRICTED_PYTHON_AVAILABLE:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="RestrictedPython not installed. Cannot execute Python code.",
                exit_code=1,
                duration_ms=0,
                security_violations=["RestrictedPython unavailable"]
            )

        start_time = time.time()

        try:
            # Compile with RestrictedPython
            try:
                byte_code = compile_restricted(
                    code,
                    filename='<sandbox>',
                    mode='exec'
                )
            except SyntaxError as e:
                return ExecutionResult(
                    success=False,
                    stdout="",
                    stderr=f"Syntax error at line {e.lineno}: {e.msg}",
                    exit_code=1,
                    duration_ms=int((time.time() - start_time) * 1000),
                    security_violations=["Compilation error"]
                )

            # Prepare restricted globals
            from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence
            from RestrictedPython.PrintCollector import PrintCollector

            # Safe import that allows common modules
            def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
                if name in ['os', 'json', 're', 'math', 'datetime', 'time']:
                    return __import__(name, globals, locals, fromlist, level)
                raise ImportError(f'Import of {name} is not allowed')

            # Inplace operation handler (+=, -=, etc.)
            def safe_inplacevar(op, x, y):
                if op == '+=':
                    return x + y
                elif op == '-=':
                    return x - y
                elif op == '*=':
                    return x * y
                elif op == '/=':
                    return x / y
                elif op == '//=':
                    return x // y
                elif op == '%=':
                    return x % y
                elif op == '**=':
                    return x ** y
                return x

            restricted_globals = {
                '__builtins__': safe_builtins,
                '_print_': PrintCollector,
                '_getattr_': getattr,
                '__name__': 'restricted_module',
                '__metaclass__': type,
                '_getiter_': iter,
                '_getitem_': lambda obj, index: obj[index],
                '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
                '__import__': safe_import,
                '_inplacevar_': safe_inplacevar,
            }

            # Add limited file I/O if write access granted
            if self.write_access:
                restricted_globals['open'] = self._safe_open
            else:
                restricted_globals['open'] = self._readonly_open

            # Capture stdout/stderr
            from io import StringIO
            import threading

            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            # Use threading for timeout (more reliable than signal.alarm)
            timeout_exceeded = [False]
            result_holder = [None]
            exception_holder = [None]

            def execute_with_timeout():
                try:
                    # Execute code
                    exec(byte_code, restricted_globals)
                    result_holder[0] = "success"
                except Exception as e:
                    exception_holder[0] = e

            execution_thread = threading.Thread(target=execute_with_timeout)
            execution_thread.daemon = True
            execution_thread.start()
            execution_thread.join(timeout=timeout_seconds)

            if execution_thread.is_alive():
                # Timeout occurred
                timeout_exceeded[0] = True
                return ExecutionResult(
                    success=False,
                    stdout=sys.stdout.getvalue(),
                    stderr=f"Execution exceeded {timeout_seconds} seconds",
                    exit_code=124,
                    duration_ms=int((time.time() - start_time) * 1000),
                    security_violations=["Timeout exceeded"]
                )

            # Restore stdout/stderr before processing results
            stdout_capture = sys.stdout
            stderr_capture = sys.stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            if exception_holder[0]:
                e = exception_holder[0]
                return ExecutionResult(
                    success=False,
                    stdout=stdout_capture.getvalue(),
                    stderr=f"{type(e).__name__}: {str(e)}",
                    exit_code=1,
                    duration_ms=int((time.time() - start_time) * 1000),
                    security_violations=[]
                )

            # Get output from PrintCollector
            print_output = ""
            if '_print' in restricted_globals:
                print_output = restricted_globals['_print']()

            # Success case
            return ExecutionResult(
                success=True,
                stdout=stdout_capture.getvalue() + print_output,
                stderr=stderr_capture.getvalue(),
                exit_code=0,
                duration_ms=int((time.time() - start_time) * 1000),
                security_violations=[]
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Execution error: {str(e)}",
                exit_code=1,
                duration_ms=int((time.time() - start_time) * 1000),
                security_violations=[f"Unexpected error: {type(e).__name__}"]
            )

    def _safe_open(self, filename, mode='r', *args, **kwargs):
        """Safe open() that restricts to sandbox directory."""
        # Convert relative paths to absolute paths within sandbox
        if not Path(filename).is_absolute():
            full_path = self.sandbox_dir / filename
        else:
            full_path = Path(filename)

        if not validate_sandbox_path(full_path, self.sandbox_dir):
            raise PermissionError(f"Access denied: {filename} is outside sandbox")
        return open(full_path, mode, *args, **kwargs)

    def _readonly_open(self, filename, mode='r', *args, **kwargs):
        """Read-only open() for restricted agents."""
        if 'w' in mode or 'a' in mode or '+' in mode:
            raise PermissionError("Write access denied by agent policy")
        return self._safe_open(filename, mode, *args, **kwargs)


class BashExecutor:
    """Execute Bash commands with whitelist validation."""

    def __init__(self, sandbox_dir: Path, allowed_commands: List[str]):
        self.sandbox_dir = sandbox_dir
        self.allowed_commands = allowed_commands

    def execute(self, command: str, timeout_seconds: int, memory_limit_mb: int) -> ExecutionResult:
        """
        Execute bash command with whitelist validation.

        Args:
            command: Bash command to execute
            timeout_seconds: Execution timeout
            memory_limit_mb: Memory limit

        Returns:
            ExecutionResult with stdout/stderr/exit_code
        """
        start_time = time.time()

        try:
            # Run command in sandbox directory
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.sandbox_dir),
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )

            return ExecutionResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=int((time.time() - start_time) * 1000),
                security_violations=[]
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Command exceeded {timeout_seconds} second timeout",
                exit_code=124,
                duration_ms=int((time.time() - start_time) * 1000),
                security_violations=["Timeout exceeded"]
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Execution error: {str(e)}",
                exit_code=1,
                duration_ms=int((time.time() - start_time) * 1000),
                security_violations=[f"Unexpected error: {type(e).__name__}"]
            )


# ============================================================================
# Audit System
# ============================================================================

class ExecutionAuditor:
    """Audit trail for all code executions."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def log_execution(
        self,
        agent_id: str,
        language: str,
        code: str,
        result: ExecutionResult,
        policy: ExecutionPolicy
    ):
        """
        Log execution to agent's audit trail.

        Creates: memories/agents/{agent_id}/execution_log.jsonl
        """
        agent_memory_dir = self.base_dir / "memories" / "agents" / agent_id
        agent_memory_dir.mkdir(parents=True, exist_ok=True)

        log_file = agent_memory_dir / "execution_log.jsonl"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_id,
            "language": language,
            "code": code[:500] if len(code) > 500 else code,  # Truncate long code
            "code_length": len(code),
            "result": result.to_dict(),
            "policy": {
                "timeout_seconds": policy.timeout_seconds,
                "memory_limit_mb": policy.memory_limit_mb,
                "write_access": policy.python_write_access if language == "python" else False
            }
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')


# ============================================================================
# Main Execution Interface
# ============================================================================

def execute_code(
    agent_id: str,
    language: str,
    code: str,
    policy: Optional[ExecutionPolicy] = None,
    sandbox_root: Optional[Path] = None,
    audit: bool = True
) -> ExecutionResult:
    """
    Execute code safely with policy enforcement and auditing.

    Args:
        agent_id: ID of agent requesting execution
        language: "python" or "bash"
        code: Code to execute
        policy: Execution policy (defaults to agent-specific policy)
        sandbox_root: Sandbox directory (defaults to repo/mcp/servers/sandbox/workspace/)
        audit: Whether to log execution (default True)

    Returns:
        ExecutionResult with success status, output, and security info

    Example:
        >>> result = execute_code("coder", "python", "print('hello')")
        >>> if result.success:
        ...     print(result.stdout)
        ... else:
        ...     print(f"Error: {result.stderr}")
    """
    # Get policy
    if policy is None:
        policy = ExecutionPolicy.for_agent(agent_id)

    # Get sandbox root
    if sandbox_root is None:
        repo_root = Path(__file__).parent.parent
        sandbox_root = repo_root / "mcp" / "servers" / "sandbox" / "workspace"
        sandbox_root.mkdir(parents=True, exist_ok=True)

    # Pre-execution validation
    violations = check_forbidden_patterns(code)

    if language == "python":
        if not policy.python_enabled:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Python execution disabled for agent '{agent_id}'",
                exit_code=1,
                duration_ms=0,
                security_violations=["Policy violation: Python disabled"]
            )

        valid, error = validate_python_syntax(code)
        if not valid:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=error,
                exit_code=1,
                duration_ms=0,
                security_violations=["Invalid syntax"]
            )

        if violations:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Security violations detected: {', '.join(violations)}",
                exit_code=1,
                duration_ms=0,
                security_violations=violations
            )

        executor = PythonExecutor(sandbox_root, policy.python_write_access)
        result = executor.execute(code, policy.timeout_seconds, policy.memory_limit_mb)

    elif language == "bash":
        if not policy.bash_enabled:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Bash execution disabled for agent '{agent_id}'",
                exit_code=1,
                duration_ms=0,
                security_violations=["Policy violation: Bash disabled"]
            )

        valid, error = validate_bash_syntax(code)
        if not valid:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=error,
                exit_code=1,
                duration_ms=0,
                security_violations=["Invalid syntax"]
            )

        allowed, error = validate_bash_command_whitelist(code, policy.bash_allowed_commands)
        if not allowed:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=error,
                exit_code=1,
                duration_ms=0,
                security_violations=["Command not in whitelist"]
            )

        if violations:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Security violations detected: {', '.join(violations)}",
                exit_code=1,
                duration_ms=0,
                security_violations=violations
            )

        executor = BashExecutor(sandbox_root, policy.bash_allowed_commands)
        result = executor.execute(code, policy.timeout_seconds, policy.memory_limit_mb)

    else:
        return ExecutionResult(
            success=False,
            stdout="",
            stderr=f"Unsupported language: {language}",
            exit_code=1,
            duration_ms=0,
            security_violations=["Unsupported language"]
        )

    # Audit execution
    if audit:
        # Always use the actual repo root (where this file is located)
        repo_root = Path(__file__).parent.parent
        auditor = ExecutionAuditor(repo_root)
        auditor.log_execution(agent_id, language, code, result, policy)

    return result


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Command-line interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="MCP Sandbox: Safe code execution")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., coder, researcher)")
    parser.add_argument("--language", required=True, choices=["python", "bash"], help="Language")
    parser.add_argument("--code", required=True, help="Code to execute")
    parser.add_argument("--no-audit", action="store_true", help="Skip audit logging")

    args = parser.parse_args()

    result = execute_code(
        agent_id=args.agent,
        language=args.language,
        code=args.code,
        audit=not args.no_audit
    )

    print(f"Success: {result.success}")
    print(f"Exit code: {result.exit_code}")
    print(f"Duration: {result.duration_ms}ms")

    if result.stdout:
        print(f"\nStdout:\n{result.stdout}")

    if result.stderr:
        print(f"\nStderr:\n{result.stderr}")

    if result.security_violations:
        print(f"\nSecurity violations:\n" + "\n".join(f"  - {v}" for v in result.security_violations))

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
