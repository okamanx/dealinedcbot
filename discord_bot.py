import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import sys
import logging
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# Load environment variables from .env file
load_dotenv()

def validate_token(token):
    """Validate the Discord bot token format."""
    if not token:
        return False, "Token is empty"
    
    # Log token details (safely)
    logger.info(f"Token length: {len(token)}")
    logger.info(f"Token contains dots: {'.' in token}")
    logger.info(f"Token starts with: {token[:2]}")
    
    # Check for common issues
    if ' ' in token:
        return False, "Token contains spaces"
    if '\n' in token:
        return False, "Token contains newlines"
    if token.strip() != token:
        return False, "Token has leading/trailing whitespace"
    
    # More lenient token validation
    if not token.startswith(('MT', 'NT', 'OT')):
        return False, "Token doesn't start with expected prefix"
    
    if '.' not in token:
        return False, "Token doesn't contain required dots"
    
    if len(token) < 50 or len(token) > 70:
        return False, f"Token length ({len(token)}) is outside expected range (50-70)"
    
    return True, "Token format appears valid"

# Get the bot token from environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
logger.info("Checking Discord bot token...")

if not TOKEN:
    logger.error("DISCORD_BOT_TOKEN environment variable is not set!")
    logger.error("Please set your Discord bot token in Render's environment variables.")
    sys.exit(1)

# Log the raw token (first and last few characters only)
safe_token = f"{TOKEN[:4]}...{TOKEN[-4:]}" if len(TOKEN) > 8 else "***"
logger.info(f"Raw token (partial): {safe_token}")

# Validate token format
is_valid, message = validate_token(TOKEN)
if not is_valid:
    logger.error(f"Token validation failed: {message}")
    logger.error("Please check your token in Render's environment variables.")
    logger.error("Token should be obtained from Discord Developer Portal -> Your App -> Bot -> Reset Token")
    logger.error("Make sure to copy the entire token without any extra spaces")
    sys.exit(1)

logger.info("Token format validation passed")
logger.info("Attempting to connect to Discord...")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intents
bot = commands.Bot(command_prefix="!", intents=intents)

# ... rest of your existing code ...

# Run the bot with error handling
if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        logger.info("Make sure the bot is invited to your server with proper permissions")
        logger.info("You can get the invite link from Discord Developer Portal -> OAuth2 -> URL Generator")
        bot.run(TOKEN, log_handler=None)  # Disable discord.py's default logging
    except discord.LoginFailure as e:
        logger.error(f"Failed to login to Discord: {str(e)}")
        logger.error("This usually means the token is invalid or has been reset.")
        logger.error("Please:")
        logger.error("1. Go to Discord Developer Portal")
        logger.error("2. Select your application")
        logger.error("3. Go to Bot section")
        logger.error("4. Click 'Reset Token'")
        logger.error("5. Copy the new token")
        logger.error("6. Update the token in Render's environment variables")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error("Please check the logs for more details.")
        sys.exit(1)
// ... existing code ...
