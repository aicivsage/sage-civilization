#!/usr/bin/env python3
"""
Health Bot Handler - Telegram bot for manual health data entry

Handles:
- Manual health data reporting (weight, BP, steps)
- Natural language and slash command parsing
- Database insertion
- Health-coach agent invocation for responses
- Daily 8 AM check-ins
"""

import os
import sys
import re
import sqlite3
import argparse
from datetime import datetime, date
from pathlib import Path
import json
import subprocess
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import telebot
except ImportError:
    print("❌ python-telebot not installed. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"], check=True)
    import telebot


class HealthBotHandler:
    """Telegram bot for health data entry and coaching"""

    def __init__(self, token: str, db_path: str = None):
        self.bot = telebot.TeleBot(token)
        self.db_path = db_path or str(PROJECT_ROOT / "health_gamification" / "data" / "health.db")
        self.corey_chat_id = 437939400  # Corey's Telegram user ID

        # Ensure database exists
        self._init_database()

        # Register handlers
        self._register_handlers()

    def _init_database(self):
        """Initialize health database if doesn't exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables if not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_date DATE NOT NULL,
                weight_lbs REAL,
                bp_systolic INTEGER,
                bp_diastolic INTEGER,
                steps INTEGER,
                weight_source TEXT DEFAULT 'telegram',
                bp_source TEXT DEFAULT 'telegram',
                steps_source TEXT DEFAULT 'telegram',
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score_date DATE NOT NULL,
                weight_change_lbs REAL,
                weight_score_dollars REAL,
                bp_check_score_dollars REAL,
                steps_score_dollars REAL,
                daily_total_dollars REAL,
                running_balance_dollars REAL,
                metric_id INTEGER REFERENCES health_metrics(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")

    def _register_handlers(self):
        """Register Telegram message handlers"""

        @self.bot.message_handler(commands=['start', 'help'])
        def handle_help(message):
            self._send_help(message.chat.id)

        @self.bot.message_handler(commands=['weight'])
        def handle_weight_command(message):
            # Extract value from /weight 195
            match = re.search(r'/weight\s+(\d+\.?\d*)', message.text, re.IGNORECASE)
            if match:
                weight = float(match.group(1))
                self._log_weight(message.chat.id, weight)
            else:
                self.bot.send_message(message.chat.id, "Usage: /weight 195")

        @self.bot.message_handler(commands=['bp'])
        def handle_bp_command(message):
            # Extract value from /bp 120/80
            match = re.search(r'/bp\s+(\d+)/(\d+)', message.text, re.IGNORECASE)
            if match:
                systolic = int(match.group(1))
                diastolic = int(match.group(2))
                self._log_bp(message.chat.id, systolic, diastolic)
            else:
                self.bot.send_message(message.chat.id, "Usage: /bp 120/80")

        @self.bot.message_handler(commands=['steps'])
        def handle_steps_command(message):
            # Extract value from /steps 7000
            match = re.search(r'/steps\s+(\d+)', message.text, re.IGNORECASE)
            if match:
                steps = int(match.group(1))
                self._log_steps(message.chat.id, steps)
            else:
                self.bot.send_message(message.chat.id, "Usage: /steps 7000")

        @self.bot.message_handler(commands=['status'])
        def handle_status(message):
            self._send_status(message.chat.id)

        @self.bot.message_handler(commands=['streak'])
        def handle_streak(message):
            self._send_streak(message.chat.id)

        @self.bot.message_handler(func=lambda m: True)
        def handle_text(message):
            """Parse natural language health data"""
            text = message.text.lower()

            # Weight patterns: "weight 195", "195 lbs", "w: 195"
            weight_match = re.search(r'(?:weight|w)[\s:]+(\d+\.?\d*)', text) or \
                           re.search(r'(\d+\.?\d*)\s*(?:lbs?|pounds?)', text)

            # BP patterns: "BP 120/80", "blood pressure 118/76", "120/80"
            bp_match = re.search(r'(?:bp|blood\s*pressure|b\.?p\.?)[\s:]*(\d+)/(\d+)', text) or \
                       re.search(r'\b(\d{2,3})/(\d{2,3})\b', text)

            # Steps patterns: "steps 7000", "7000 steps", "s: 7000"
            steps_match = re.search(r'(?:steps?|s)[\s:]+(\d+)', text) or \
                          re.search(r'(\d{4,5})\s*steps?', text)

            logged_something = False

            if weight_match:
                weight = float(weight_match.group(1))
                self._log_weight(message.chat.id, weight)
                logged_something = True

            if bp_match:
                systolic = int(bp_match.group(1))
                diastolic = int(bp_match.group(2))
                self._log_bp(message.chat.id, systolic, diastolic)
                logged_something = True

            if steps_match:
                steps = int(steps_match.group(1))
                self._log_steps(message.chat.id, steps)
                logged_something = True

            if not logged_something:
                self.bot.send_message(
                    message.chat.id,
                    "I didn't understand that. Try:\n"
                    "• weight 195\n"
                    "• BP 120/80\n"
                    "• steps 7000\n"
                    "Or /help for more info"
                )

    def _log_weight(self, chat_id: int, weight: float):
        """Log weight measurement"""
        today = date.today().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if today already has weight
            cursor.execute(
                "SELECT id, weight_lbs FROM health_metrics WHERE metric_date = ?",
                (today,)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing
                cursor.execute(
                    "UPDATE health_metrics SET weight_lbs = ?, weight_source = 'telegram', collected_at = CURRENT_TIMESTAMP WHERE metric_date = ?",
                    (weight, today)
                )
                action = "updated"
            else:
                # Insert new
                cursor.execute(
                    "INSERT INTO health_metrics (metric_date, weight_lbs, weight_source) VALUES (?, ?, 'telegram')",
                    (today, weight)
                )
                action = "logged"

            conn.commit()

            # Calculate score if it's Sunday (weigh-in day)
            today_date = date.today()
            if today_date.weekday() == 6:  # Sunday = 6
                score_info = self._calculate_weight_score(weight)
                response = f"✅ Weight {action}: {weight} lbs\n\n{score_info}"
            else:
                response = f"✅ Weight {action}: {weight} lbs\n\n(Score updates on Sunday weigh-ins)"

            self.bot.send_message(chat_id, response)

            # Log audit
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_weight", "success", f"{action} {weight} lbs")
            )
            conn.commit()

        except Exception as e:
            self.bot.send_message(chat_id, f"❌ Error logging weight: {str(e)}")
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_weight", "error", str(e))
            )
            conn.commit()
        finally:
            conn.close()

    def _calculate_weight_score(self, current_weight: float) -> str:
        """Calculate weight score based on change from last week"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get last week's weight (last Sunday)
            cursor.execute("""
                SELECT weight_lbs FROM health_metrics
                WHERE weight_lbs IS NOT NULL
                AND metric_date < date('now')
                ORDER BY metric_date DESC
                LIMIT 1
            """)
            result = cursor.fetchone()

            if not result:
                return "First weigh-in! No score yet (need baseline)."

            last_weight = result[0]
            change = last_weight - current_weight  # Positive = weight loss
            score = change * 100  # $100 per pound

            # Get current running balance
            cursor.execute("""
                SELECT running_balance_dollars FROM health_scores
                ORDER BY score_date DESC
                LIMIT 1
            """)
            balance_result = cursor.fetchone()
            current_balance = balance_result[0] if balance_result else 0
            new_balance = current_balance + score

            # Insert score record
            today = date.today().isoformat()
            cursor.execute("""
                INSERT INTO health_scores
                (score_date, weight_change_lbs, weight_score_dollars, daily_total_dollars, running_balance_dollars)
                VALUES (?, ?, ?, ?, ?)
            """, (today, change, score, score, new_balance))
            conn.commit()

            # Format response
            if change > 0:
                emoji = "🎉"
                direction = "lost"
            elif change < 0:
                emoji = "📈"
                direction = "gained"
            else:
                emoji = "➡️"
                direction = "no change"

            return (
                f"{emoji} {abs(change):.1f} lbs {direction} → {score:+.0f} dollars\n"
                f"Running balance: ${new_balance:.0f}"
            )

        except Exception as e:
            return f"Error calculating score: {str(e)}"
        finally:
            conn.close()

    def _log_bp(self, chat_id: int, systolic: int, diastolic: int):
        """Log blood pressure measurement"""
        today = date.today().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if today already has entry
            cursor.execute(
                "SELECT id FROM health_metrics WHERE metric_date = ?",
                (today,)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing
                cursor.execute(
                    "UPDATE health_metrics SET bp_systolic = ?, bp_diastolic = ?, bp_source = 'telegram', collected_at = CURRENT_TIMESTAMP WHERE metric_date = ?",
                    (systolic, diastolic, today)
                )
                action = "updated"
            else:
                # Insert new
                cursor.execute(
                    "INSERT INTO health_metrics (metric_date, bp_systolic, bp_diastolic, bp_source) VALUES (?, ?, ?, 'telegram')",
                    (today, systolic, diastolic)
                )
                action = "logged"

            conn.commit()

            # Calculate score (+$10 for BP check)
            score = 10

            # Get current running balance
            cursor.execute("""
                SELECT running_balance_dollars FROM health_scores
                ORDER BY score_date DESC
                LIMIT 1
            """)
            balance_result = cursor.fetchone()
            current_balance = balance_result[0] if balance_result else 0
            new_balance = current_balance + score

            # Insert/update score record
            cursor.execute("""
                INSERT OR REPLACE INTO health_scores
                (score_date, bp_check_score_dollars, daily_total_dollars, running_balance_dollars)
                VALUES (?, ?, ?, ?)
            """, (today, score, score, new_balance))
            conn.commit()

            response = (
                f"✅ BP {action}: {systolic}/{diastolic}\n\n"
                f"+$10 for daily BP check 💰\n"
                f"Running balance: ${new_balance:.0f}"
            )
            self.bot.send_message(chat_id, response)

            # Log audit
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_bp", "success", f"{action} {systolic}/{diastolic}")
            )
            conn.commit()

        except Exception as e:
            self.bot.send_message(chat_id, f"❌ Error logging BP: {str(e)}")
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_bp", "error", str(e))
            )
            conn.commit()
        finally:
            conn.close()

    def _log_steps(self, chat_id: int, steps: int):
        """Log steps count"""
        today = date.today().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if today already has entry
            cursor.execute(
                "SELECT id FROM health_metrics WHERE metric_date = ?",
                (today,)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing
                cursor.execute(
                    "UPDATE health_metrics SET steps = ?, steps_source = 'telegram', collected_at = CURRENT_TIMESTAMP WHERE metric_date = ?",
                    (steps, today)
                )
                action = "updated"
            else:
                # Insert new
                cursor.execute(
                    "INSERT INTO health_metrics (metric_date, steps, steps_source) VALUES (?, ?, 'telegram')",
                    (today, steps)
                )
                action = "logged"

            conn.commit()

            # Calculate score (+$20 if ≥6k, -$20 if <6k)
            if steps >= 6000:
                score = 20
                emoji = "🎯"
                message = "Hit 6k steps goal!"
            else:
                score = -20
                emoji = "📉"
                message = f"Below 6k goal ({6000 - steps} short)"

            # Get current running balance
            cursor.execute("""
                SELECT running_balance_dollars FROM health_scores
                ORDER BY score_date DESC
                LIMIT 1
            """)
            balance_result = cursor.fetchone()
            current_balance = balance_result[0] if balance_result else 0
            new_balance = current_balance + score

            # Insert/update score record
            cursor.execute("""
                INSERT OR REPLACE INTO health_scores
                (score_date, steps_score_dollars, daily_total_dollars, running_balance_dollars)
                VALUES (?, ?, ?, ?)
            """, (today, score, score, new_balance))
            conn.commit()

            response = (
                f"✅ Steps {action}: {steps:,}\n\n"
                f"{emoji} {message}\n"
                f"{score:+.0f} dollars\n"
                f"Running balance: ${new_balance:.0f}"
            )
            self.bot.send_message(chat_id, response)

            # Log audit
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_steps", "success", f"{action} {steps} steps")
            )
            conn.commit()

        except Exception as e:
            self.bot.send_message(chat_id, f"❌ Error logging steps: {str(e)}")
            cursor.execute(
                "INSERT INTO audit_log (operation, status, details) VALUES (?, ?, ?)",
                ("log_steps", "error", str(e))
            )
            conn.commit()
        finally:
            conn.close()

    def _send_status(self, chat_id: int):
        """Send current health status and score"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get today's data
            today = date.today().isoformat()
            cursor.execute("""
                SELECT weight_lbs, bp_systolic, bp_diastolic, steps
                FROM health_metrics
                WHERE metric_date = ?
            """, (today,))
            today_data = cursor.fetchone()

            # Get running balance
            cursor.execute("""
                SELECT running_balance_dollars
                FROM health_scores
                ORDER BY score_date DESC
                LIMIT 1
            """)
            balance_result = cursor.fetchone()
            balance = balance_result[0] if balance_result else 0

            # Format status
            status = "📊 *Health Status*\n\n"

            if today_data:
                weight, bp_sys, bp_dia, steps = today_data
                if weight:
                    status += f"⚖️ Weight: {weight} lbs\n"
                if bp_sys and bp_dia:
                    status += f"💓 BP: {bp_sys}/{bp_dia}\n"
                if steps:
                    status += f"🚶 Steps: {steps:,}\n"
            else:
                status += "No data logged today\n"

            status += f"\n💰 Balance: ${balance:.0f}"

            # Calculate stock equivalent (assuming $500/share average)
            shares = balance / 500
            status += f"\n📈 ~{shares:.1f} AI/energy shares"

            self.bot.send_message(chat_id, status, parse_mode='Markdown')

        except Exception as e:
            self.bot.send_message(chat_id, f"❌ Error fetching status: {str(e)}")
        finally:
            conn.close()

    def _send_streak(self, chat_id: int):
        """Send current streaks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Count consecutive days with BP checks
            cursor.execute("""
                SELECT COUNT(*) as streak
                FROM (
                    SELECT metric_date,
                           julianday('now') - julianday(metric_date) as days_ago
                    FROM health_metrics
                    WHERE bp_systolic IS NOT NULL
                    ORDER BY metric_date DESC
                )
                WHERE days_ago = (SELECT COUNT(*) FROM health_metrics m2
                                 WHERE m2.metric_date > health_metrics.metric_date
                                 AND m2.bp_systolic IS NOT NULL)
            """)
            bp_streak = cursor.fetchone()[0] or 0

            response = f"🔥 *Streaks*\n\n💓 BP checks: {bp_streak} days"

            self.bot.send_message(chat_id, response, parse_mode='Markdown')

        except Exception as e:
            self.bot.send_message(chat_id, f"❌ Error fetching streaks: {str(e)}")
        finally:
            conn.close()

    def _send_help(self, chat_id: int):
        """Send help message"""
        help_text = """
🏥 *A-C-Gee Health Coach*

I help you track health data and stay accountable!

*How to log data:*
📝 Natural language:
• "weight 195"
• "BP 120/80"
• "steps 7000"

💬 Slash commands:
• /weight 195
• /bp 120/80
• /steps 7000

*View status:*
• /status - Current data & balance
• /streak - Current streaks
• /help - This message

*Scoring:*
• Weight: +/-$100 per lb lost/gained (Sundays)
• BP check: +$10 per day
• Steps: +$20 if ≥6k, -$20 if <6k

Balance funds AI/energy stock portfolio! 📈
        """
        self.bot.send_message(chat_id, help_text, parse_mode='Markdown')

    def start(self):
        """Start polling for messages"""
        print("🏥 Health bot started! Polling for messages...")
        print(f"📂 Database: {self.db_path}")
        self.bot.infinity_polling()


def test_connection(token: str):
    """Test bot connection"""
    try:
        bot = telebot.TeleBot(token)
        me = bot.get_me()
        print("✅ Health bot connection successful!")
        print(f"Bot username: @{me.username}")
        print(f"Bot name: {me.first_name}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A-C-Gee Health Bot")
    parser.add_argument("--test", action="store_true", help="Test bot connection")
    parser.add_argument("--token", help="Bot token (or set HEALTH_BOT_TOKEN env var)")
    args = parser.parse_args()

    # Get token
    token = args.token or os.environ.get("HEALTH_BOT_TOKEN")
    if not token:
        print("❌ No bot token provided!")
        print("Set HEALTH_BOT_TOKEN environment variable or use --token")
        sys.exit(1)

    if args.test:
        test_connection(token)
    else:
        handler = HealthBotHandler(token)
        handler.start()
