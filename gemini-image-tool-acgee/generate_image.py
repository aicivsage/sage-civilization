#!/usr/bin/env python3
"""
Gemini Image Generation Tool

CLI tool for generating images using Google Gemini 2.5 Flash API (Latest model).
All 15 A-C-Gee agents can invoke via Bash.

Model: gemini-2.5-flash (production, October 2025)
Free Tier: 15 RPM, 1500 RPD
Paid Tier: Higher limits, $0.10-0.30 per 1M tokens

Usage:
    python3 tools/generate_image.py --prompt "A futuristic AI logo" --size 1024x1024

Returns JSON with image path or error details.
"""

import argparse
import json
import os
import sys
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

try:
    import google.generativeai as genai
except ImportError:
    print(json.dumps({
        'success': False,
        'error': 'google-generativeai not installed. Run: pip install google-generativeai'
    }))
    sys.exit(2)


class RateLimiter:
    """Local rate limit enforcement (15 RPM, 1500 RPD)"""

    def __init__(self, state_file: Path, rpm_limit: int, rpd_limit: int):
        self.state_file = state_file
        self.rpm_limit = rpm_limit
        self.rpd_limit = rpd_limit
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load rate limit state from file"""
        if not self.state_file.exists():
            return {
                'requests_per_minute': [],
                'requests_per_day': {},
                'last_cleanup': datetime.now().isoformat()
            }

        try:
            with open(self.state_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {
                'requests_per_minute': [],
                'requests_per_day': {},
                'last_cleanup': datetime.now().isoformat()
            }

    def _save_state(self):
        """Save rate limit state to file"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _cleanup_old_data(self):
        """Remove old data from state"""
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')

        # Clean up RPM (keep only last minute)
        one_minute_ago = (now - timedelta(minutes=1)).isoformat()
        self.state['requests_per_minute'] = [
            ts for ts in self.state['requests_per_minute']
            if ts > one_minute_ago
        ]

        # Clean up RPD (keep only today and yesterday)
        yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
        self.state['requests_per_day'] = {
            date: count for date, count in self.state['requests_per_day'].items()
            if date in (today, yesterday)
        }

        self.state['last_cleanup'] = now.isoformat()

    def check_and_increment(self) -> Tuple[bool, Optional[int], Dict[str, int]]:
        """
        Check if request is allowed, increment counters if yes.

        Returns:
            (allowed, retry_after_seconds, quota_info)
        """
        self._cleanup_old_data()
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')

        # Check RPM
        rpm_count = len(self.state['requests_per_minute'])
        if rpm_count >= self.rpm_limit:
            # Calculate retry_after (seconds until oldest request expires)
            oldest = datetime.fromisoformat(self.state['requests_per_minute'][0])
            retry_after = int((oldest + timedelta(minutes=1) - now).total_seconds()) + 1
            return False, retry_after, self._get_quota_info()

        # Check RPD
        rpd_count = self.state['requests_per_day'].get(today, 0)
        if rpd_count >= self.rpd_limit:
            # Calculate retry_after (seconds until midnight UTC)
            tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
            retry_after = int((tomorrow - now).total_seconds())
            return False, retry_after, self._get_quota_info()

        # Allowed - increment counters
        self.state['requests_per_minute'].append(now.isoformat())
        self.state['requests_per_day'][today] = rpd_count + 1
        self._save_state()

        return True, None, self._get_quota_info()

    def _get_quota_info(self) -> Dict[str, int]:
        """Get current quota usage info"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_count = self.state['requests_per_day'].get(today, 0)

        return {
            'today': today_count,
            'limit': self.rpd_limit,
            'remaining': self.rpd_limit - today_count
        }


class GenerationLogger:
    """Log all image generations"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.logs = self._load_logs()

    def _load_logs(self) -> list:
        """Load existing logs"""
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_logs(self):
        """Save logs to file"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def log(self, entry: Dict[str, Any]):
        """Add log entry"""
        self.logs.append(entry)
        self._save_logs()


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    config_file = Path(config_path)

    if not config_file.exists():
        return {
            'success': False,
            'error': f'Config file not found: {config_path}. Create it from config/gemini_config.example.json'
        }

    try:
        with open(config_file) as f:
            config = json.load(f)

        # Validate required fields
        required = ['api_key', 'model', 'rate_limits', 'defaults']
        missing = [field for field in required if field not in config]
        if missing:
            return {
                'success': False,
                'error': f'Config missing required fields: {", ".join(missing)}'
            }

        return config

    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'Invalid JSON in config file: {str(e)}'
        }
    except IOError as e:
        return {
            'success': False,
            'error': f'Cannot read config file: {str(e)}'
        }


def sanitize_prompt_for_filename(prompt: str, max_length: int = 30) -> str:
    """Convert prompt to safe filename prefix"""
    # Remove non-alphanumeric characters
    safe = re.sub(r'[^a-zA-Z0-9\s-]', '', prompt)
    # Replace spaces with hyphens
    safe = re.sub(r'\s+', '-', safe)
    # Lowercase
    safe = safe.lower()
    # Truncate
    safe = safe[:max_length]
    # Remove trailing hyphens
    safe = safe.rstrip('-')

    return safe if safe else 'image'


def generate_image(
    prompt: str,
    size: str,
    safety_level: str,
    config: Dict[str, Any],
    rate_limiter: RateLimiter,
    logger: GenerationLogger
) -> Dict[str, Any]:
    """
    Generate image using Gemini API.

    Returns JSON result with image_path or error.
    """
    start_time = time.time()

    # Check rate limits
    allowed, retry_after, quota_info = rate_limiter.check_and_increment()
    if not allowed:
        error_msg = f'Rate limit exceeded. Try again in {retry_after} seconds.'
        logger.log({
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'success': False,
            'error': error_msg,
            'quota_used': quota_info['today']
        })

        return {
            'success': False,
            'error': error_msg,
            'retry_after': retry_after,
            'quota_used': quota_info
        }

    # Check quota warnings
    percent_used = (quota_info['today'] / quota_info['limit']) * 100
    warn_percent = config.get('monitoring', {}).get('warn_at_quota_percent', 80)
    alert_percent = config.get('monitoring', {}).get('alert_at_quota_percent', 95)

    warning = None
    if percent_used >= alert_percent:
        warning = f'ALERT: {percent_used:.1f}% of daily quota used ({quota_info["today"]}/{quota_info["limit"]})'
    elif percent_used >= warn_percent:
        warning = f'WARNING: {percent_used:.1f}% of daily quota used ({quota_info["today"]}/{quota_info["limit"]})'

    # Configure Gemini API
    api_key = config.get('api_key')
    if not api_key or api_key == 'YOUR_GOOGLE_API_KEY_HERE':
        error_msg = 'API key not configured. Set api_key in config file.'
        logger.log({
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'success': False,
            'error': error_msg,
            'quota_used': quota_info['today']
        })

        return {
            'success': False,
            'error': error_msg,
            'quota_used': quota_info
        }

    genai.configure(api_key=api_key)

    # Prepare generation config
    # Gemini 2.5 Flash (latest, Oct 2025) with native image generation via imagen-3.0 grounding
    # Safety settings map to HarmCategory
    safety_settings = None
    if safety_level:
        # Map our safety levels to Gemini's HarmBlockThreshold
        safety_map = {
            'BLOCK_NONE': 'BLOCK_NONE',
            'BLOCK_LOW': 'BLOCK_ONLY_HIGH',
            'BLOCK_MEDIUM_AND_ABOVE': 'BLOCK_MEDIUM_AND_ABOVE',
            'BLOCK_ONLY_HIGH': 'BLOCK_ONLY_HIGH'
        }
        threshold = safety_map.get(safety_level, 'BLOCK_MEDIUM_AND_ABOVE')

        # Apply to all harm categories
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold[threshold],
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold[threshold],
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold[threshold],
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold[threshold],
        }

    # Retry logic (3 attempts with exponential backoff)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Create model
            model = genai.GenerativeModel(
                model_name=config['model'],
                safety_settings=safety_settings
            )

            # Generate image
            # Gemini 2.5 Flash uses native image generation with imagen-3.0 grounding
            # High-fidelity text rendering and conversational editing capabilities
            response = model.generate_content(
                f"Generate a high-quality image: {prompt}. Image should be {size} pixels.",
                generation_config={
                    'candidate_count': 1,
                    'max_output_tokens': 2048,
                }
            )

            # Check for safety filter block
            if response.prompt_feedback.block_reason:
                error_msg = f'Safety filter triggered: {response.prompt_feedback.block_reason}'
                logger.log({
                    'timestamp': datetime.now().isoformat(),
                    'prompt': prompt,
                    'size': size,
                    'success': False,
                    'error': error_msg,
                    'safety_level': safety_level,
                    'quota_used': quota_info['today']
                })

                return {
                    'success': False,
                    'error': error_msg,
                    'quota_used': quota_info
                }

            # Extract image data
            # Gemini returns images in response.parts
            image_part = None
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    if part.inline_data.mime_type.startswith('image/'):
                        image_part = part
                        break

            if not image_part:
                raise ValueError('No image data in response. Model may not support image generation.')

            image_data = image_part.inline_data.data

            # Save image to file
            timestamp = datetime.now().strftime('%H%M%S')
            prompt_prefix = sanitize_prompt_for_filename(prompt)
            filename = f"{timestamp}-{prompt_prefix}.png"

            # Create date-based folder
            output_base = Path(config['defaults']['output_dir'])
            date_folder = datetime.now().strftime('%Y%m%d')
            output_dir = output_base / date_folder
            output_dir.mkdir(parents=True, exist_ok=True)

            filepath = output_dir / filename

            # Write image data
            with open(filepath, 'wb') as f:
                f.write(image_data)

            # Success!
            duration_ms = int((time.time() - start_time) * 1000)

            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'prompt': prompt,
                'size': size,
                'success': True,
                'image_path': str(filepath.absolute()),
                'quota_used': quota_info['today'],
                'duration_ms': duration_ms,
                'attempts': attempt + 1
            }
            logger.log(log_entry)

            result = {
                'success': True,
                'image_path': str(filepath.absolute()),
                'timestamp': datetime.now().isoformat(),
                'model': config['model'],
                'prompt': prompt,
                'size': size,
                'safety_level': safety_level,
                'quota_used': quota_info,
                'duration_ms': duration_ms
            }

            if warning:
                result['warning'] = warning

            return result

        except Exception as e:
            error_msg = str(e)

            # Check if this is a retryable error
            retryable_errors = [
                'DeadlineExceeded',
                'ServiceUnavailable',
                'InternalServerError',
                'ResourceExhausted'
            ]

            is_retryable = any(err in error_msg for err in retryable_errors)

            if is_retryable and attempt < max_retries - 1:
                # Exponential backoff: 2^attempt seconds
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                # Non-retryable or final attempt - fail
                logger.log({
                    'timestamp': datetime.now().isoformat(),
                    'prompt': prompt,
                    'size': size,
                    'success': False,
                    'error': error_msg,
                    'quota_used': quota_info['today'],
                    'attempts': attempt + 1
                })

                # Determine appropriate error code
                if 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                    error_code = 5  # Quota exhausted
                elif 'safety' in error_msg.lower() or 'block' in error_msg.lower():
                    error_code = 4  # Safety filter
                else:
                    error_code = 2  # Generic API error

                return {
                    'success': False,
                    'error': error_msg,
                    'quota_used': quota_info,
                    'error_code': error_code
                }

    # Should never reach here (loop handles all cases)
    return {
        'success': False,
        'error': 'Max retries exceeded',
        'quota_used': quota_info,
        'error_code': 2
    }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate images using Google Gemini 2.5 Flash API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/generate_image.py --prompt "A futuristic AI logo"
  python3 tools/generate_image.py --prompt "Architecture diagram" --size 1024x768
  python3 tools/generate_image.py --prompt "Safe content" --safety BLOCK_LOW

Returns JSON with image_path or error details.
        """
    )

    parser.add_argument(
        '--prompt',
        required=True,
        help='Text description of image to generate'
    )

    parser.add_argument(
        '--size',
        default='1024x1024',
        choices=['1024x1024', '1024x768', '768x1024'],
        help='Image size (default: 1024x1024)'
    )

    parser.add_argument(
        '--safety',
        default='BLOCK_MEDIUM_AND_ABOVE',
        choices=['BLOCK_NONE', 'BLOCK_LOW', 'BLOCK_MEDIUM_AND_ABOVE', 'BLOCK_ONLY_HIGH'],
        help='Safety filter level (default: BLOCK_MEDIUM_AND_ABOVE)'
    )

    parser.add_argument(
        '--output-dir',
        default=None,
        help='Override default output directory'
    )

    parser.add_argument(
        '--config',
        default='config/gemini_config.json',
        help='Path to config file (default: config/gemini_config.json)'
    )

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    if not isinstance(config, dict) or 'error' in config:
        print(json.dumps(config))
        return 1

    # Override output dir if specified
    if args.output_dir:
        config['defaults']['output_dir'] = args.output_dir

    # Initialize rate limiter
    output_base = Path(config['defaults']['output_dir'])
    rate_limit_file = output_base / '.rate_limit_state.json'
    rate_limiter = RateLimiter(
        rate_limit_file,
        config['rate_limits']['requests_per_minute'],
        config['rate_limits']['requests_per_day']
    )

    # Initialize logger
    log_file = output_base / '.generation_log.json'
    logger = GenerationLogger(log_file)

    # Generate image
    result = generate_image(
        args.prompt,
        args.size,
        args.safety,
        config,
        rate_limiter,
        logger
    )

    # Print JSON result
    print(json.dumps(result, indent=2))

    # Return appropriate exit code
    if result['success']:
        return 0
    elif 'error_code' in result:
        return result['error_code']
    elif 'rate limit' in result.get('error', '').lower():
        return 3
    elif 'safety' in result.get('error', '').lower():
        return 4
    elif 'quota' in result.get('error', '').lower():
        return 5
    else:
        return 2


if __name__ == '__main__':
    sys.exit(main())
