# Discord Tournament Bot

A Discord bot for managing tournament registrations and team management.

## Features

- Tournament slot management
- Team registration
- Team confirmation
- Status checking
- Admin commands for management

## Commands

- `!setslots <number>` (Admin only): Set the number of tournament slots
- `!register <team_name> <player1> <player2> ...`: Register a team
- `!confirm`: Confirm your team's registration
- `!slots`: Check current slot status
- `!teams` (Admin only): List all registered teams
- `!reset` (Admin only): Reset all tournament data

## Deployment on Render

1. Create a Render account at https://render.com if you haven't already

2. Fork this repository to your GitHub account

3. In Render:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: discord-tournament-bot
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python discord_bot.py`
   - Add Environment Variable:
     - Key: `DISCORD_BOT_TOKEN`
     - Value: Your Discord bot token
   - Click "Create Web Service"

4. Wait for the deployment to complete

## Local Development

1. Clone the repository
2. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python discord_bot.py
   ```

## Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token (required)

## Security Notes

- Never commit your `.env` file or expose your bot token
- The bot token is stored securely in Render's environment variables
- Admin commands are restricted to users with administrator permissions 
