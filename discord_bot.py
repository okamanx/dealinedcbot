import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No Discord bot token found. Please set DISCORD_BOT_TOKEN in your .env file.")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Constants
DATA_FILE = "tourney_data.json"

def load_data():
    """Load tournament data from JSON file or initialize if it doesn't exist."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in tourney_data.json. Initializing new data.")
            return {"slots": 0, "teams": [], "confirmed": []}
    else:
        return {"slots": 0, "teams": [], "confirmed": []}

def save_data(data):
    """Save tournament data to JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# Initialize tournament data
data = load_data()

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f"Bot logged in as {bot.user}")
    print(f"Bot is in {len(bot.guilds)} guilds")
    print("------")

@bot.command()
@commands.has_permissions(administrator=True)
async def setslots(ctx, number: int):
    """Set the number of available tournament slots."""
    if number < 0:
        await ctx.send("Please provide a positive number of slots.")
        return
    
    if number < len(data["teams"]):
        await ctx.send(f"Warning: Reducing slots to {number} will remove {len(data['teams']) - number} teams. Use !reset first if you want to start fresh.")
        return

    data["slots"] = number
    save_data(data)
    await ctx.send(f"Tournament slots set to {number}.")

@bot.command()
async def register(ctx, team_name: str, *players):
    """Register a team for the tournament."""
    # Check if slots are available
    if len(data["teams"]) >= data["slots"]:
        await ctx.send("All slots are full.")
        return

    # Check if team name is already taken
    for team in data["teams"]:
        if team_name.lower() == team["team_name"].lower():
            await ctx.send("This team name is already registered.")
            return

    # Validate number of players
    if len(players) < 1:
        await ctx.send("Please provide at least one player name.")
        return

    # Create and save team
    team = {
        "team_name": team_name,
        "players": list(players),
        "captain_id": ctx.author.id,
        "registered_at": str(ctx.message.created_at)
    }
    data["teams"].append(team)
    save_data(data)
    
    # Send confirmation message
    await ctx.send(
        f"Team '{team_name}' registered successfully!\n"
        f"Players: {', '.join(players)}\n"
        f"Captain: {ctx.author.mention}\n"
        f"Slots remaining: {data['slots'] - len(data['teams'])}"
    )

@bot.command()
async def confirm(ctx):
    """Confirm team registration."""
    for team in data["teams"]:
        if team["captain_id"] == ctx.author.id:
            if team["team_name"] in data["confirmed"]:
                await ctx.send("Your team is already confirmed.")
                return
            
            data["confirmed"].append(team["team_name"])
            save_data(data)
            await ctx.send(f"Team '{team['team_name']}' has been confirmed.")
            return
    
    await ctx.send("You don't have a registered team.")

@bot.command()
async def slots(ctx):
    """Show current tournament slot status."""
    filled = len(data["teams"])
    total = data["slots"]
    confirmed = len(data["confirmed"])
    
    await ctx.send(
        f"Tournament Status:\n"
        f"Slots: {filled}/{total} filled\n"
        f"Confirmed teams: {confirmed}/{filled}"
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def teams(ctx):
    """List all registered teams (admin only)."""
    if not data["teams"]:
        await ctx.send("No teams registered yet.")
        return

    # Create an embedded message for better formatting
    embed = discord.Embed(
        title="Registered Teams",
        color=discord.Color.blue()
    )
    
    for team in data["teams"]:
        status = "✅ Confirmed" if team["team_name"] in data["confirmed"] else "⏳ Pending"
        embed.add_field(
            name=f"{team['team_name']} {status}",
            value=f"Captain: <@{team['captain_id']}>\nPlayers: {', '.join(team['players'])}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx):
    """Reset all tournament data (admin only)."""
    global data
    data = {"slots": 0, "teams": [], "confirmed": []}
    save_data(data)
    await ctx.send("Tournament data has been reset.")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument provided.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN) 