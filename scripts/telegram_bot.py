#!/usr/bin/env python3
"""
Telegram Bot Handler for Sage AI Civilization
Enables communication with the civilization via Telegram
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
import asyncio

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("Telegram library not installed. Run: pip install python-telegram-bot --break-system-packages")
    exit(1)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, config_path='config/telegram_config.json'):
        """Initialize Telegram bot with configuration"""
        self.config = self.load_config(config_path)
        self.app = Application.builder().token(self.config['bot_token']).build()
        self.setup_handlers()
        
    def load_config(self, config_path):
        """Load Telegram configuration"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Telegram config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def is_authorized(self, user_id):
        """Check if user is authorized"""
        allowed = self.config.get('allowed_chat_ids', [])
        admins = self.config.get('admin_chat_ids', [])
        return user_id in allowed or user_id in admins or len(allowed) == 0
    
    def is_admin(self, user_id):
        """Check if user is admin"""
        admins = self.config.get('admin_chat_ids', [])
        return user_id in admins
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("agents", self.cmd_agents))
        self.app.add_handler(CommandHandler("goals", self.cmd_goals))
        self.app.add_handler(CommandHandler("myid", self.cmd_myid))
        
        # Message handler for general chat
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text(
                "⚠️ You are not authorized to use this bot.\n"
                f"Your user ID is: {user_id}\n"
                "Please contact the administrator to get access."
            )
            return
        
        await update.message.reply_text(
            "🏛️ Welcome to Sage AI Civilization!\n\n"
            "I'm your interface to the AI agent civilization.\n\n"
            "Available commands:\n"
            "/status - Get system status\n"
            "/agents - List all agents\n"
            "/goals - View current goals\n"
            "/help - Show this help message\n"
            "/myid - Get your Telegram user ID"
        )
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.cmd_start(update, context)
    
    async def cmd_myid(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /myid command - shows user their Telegram ID"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "No username"
        
        await update.message.reply_text(
            f"👤 Your Telegram Information:\n\n"
            f"User ID: `{user_id}`\n"
            f"Username: @{username}\n\n"
            f"Use this ID in your telegram_config.json"
        )
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⚠️ Unauthorized")
            return
        
        status = self.get_system_status()
        
        message = (
            "📊 *Sage AI Civilization Status*\n\n"
            f"🤖 Active Agents: {status['agent_count']}\n"
            f"🏗️ Architecture: {status['architecture']}\n"
            f"📅 Last Update: {status['timestamp']}\n"
        )
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def cmd_agents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /agents command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⚠️ Unauthorized")
            return
        
        agents = self.get_agents()
        
        if not agents:
            await update.message.reply_text("No agents found.")
            return
        
        message = "🤖 *Active Agents:*\n\n"
        for name, data in agents.items():
            status_emoji = "✅" if data.get('status') == 'active' else "❌"
            message += f"{status_emoji} *{name}*\n"
            message += f"   Role: {data.get('role', 'Unknown')}\n"
            message += f"   Reputation: {data.get('reputation', 50)}\n\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def cmd_goals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /goals command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⚠️ Unauthorized")
            return
        
        goals = self.get_goals()
        
        await update.message.reply_text(
            f"🎯 *Current Goals:*\n\n{goals}",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        if not self.is_authorized(update.effective_user.id):
            return
        
        user_message = update.message.text
        user_id = update.effective_user.id
        
        # Log the message
        self.log_message(user_id, user_message, 'received')
        
        # Write to message bus for agents to process
        self.write_to_message_bus(user_id, user_message)
        
        await update.message.reply_text(
            "📬 Message received and forwarded to the civilization.\n"
            "An agent will process your request."
        )
    
    def get_system_status(self):
        """Get current system status"""
        status = {
            'agent_count': 0,
            'architecture': 'Unknown',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            with open('memories/agents/agent_registry.json', 'r') as f:
                agents = json.load(f)
                status['agent_count'] = len(agents)
        except:
            pass
        
        try:
            with open('memories/system/architectural_state.json', 'r') as f:
                arch = json.load(f)
                status['architecture'] = arch.get('topology', 'Unknown')
        except:
            pass
        
        return status
    
    def get_agents(self):
        """Get list of agents"""
        try:
            with open('memories/agents/agent_registry.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_goals(self):
        """Get current goals"""
        try:
            with open('memories/system/goals.md', 'r') as f:
                return f.read()
        except:
            return "No goals file found"
    
    def write_to_message_bus(self, user_id, message):
        """Write message to message bus for agents to process"""
        msg_dir = Path('memories/communication/message_bus/telegram')
        msg_dir.mkdir(parents=True, exist_ok=True)
        
        msg_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'telegram',
            'user_id': user_id,
            'message': message,
            'status': 'pending'
        }
        
        msg_file = msg_dir / f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(msg_file, 'w') as f:
            json.dump(msg_data, f, indent=2)
    
    def log_message(self, user_id, message, direction):
        """Log Telegram message"""
        log_dir = Path('memories/communication/telegram_logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'message': message,
            'direction': direction
        }
        
        log_file = log_dir / f"telegram_log_{datetime.now().strftime('%Y%m%d')}.json"
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    async def send_notification(self, message, chat_id=None):
        """Send notification to authorized users"""
        if chat_id:
            recipients = [chat_id]
        else:
            recipients = self.config.get('admin_chat_ids', [])
        
        for recipient in recipients:
            try:
                await self.app.bot.send_message(chat_id=recipient, text=message)
            except Exception as e:
                logger.error(f"Failed to send message to {recipient}: {e}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Sage AI Civilization Telegram Bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main entry point"""
    bot = TelegramBot()
    bot.run()

if __name__ == '__main__':
    main()
