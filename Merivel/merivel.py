from twitchio.ext import commands

# Replace these with your own credentials
BOT_TOKEN = 'your_oauth_token_here'
CLIENT_ID = 'your_client_id'
CHANNEL_NAME = 'target_channel_name'

# Initialize the bot
bot = commands.Bot(
    token=BOT_TOKEN,
    client_id=CLIENT_ID,
    nick='YourBotUsername',
    prefix='!',  # This is the prefix for bot commands (e.g., !hello)
    initial_channels=[CHANNEL_NAME]
)

# Event: Runs when the bot is ready
@bot.event
async def event_ready():
    print(f'Logged in as | {bot.nick}')
    print(f'Connected to channel | {CHANNEL_NAME}')

# Event: Runs every time a message is sent in chat
@bot.event
async def event_message(message):
    # Prevent the bot from responding to itself
    if message.author.name.lower() == bot.nick.lower():
        return
    
    # Process any commands
    await bot.handle_commands(message)

# Command: Responds with "Hello, {user}!" when "!hello" is typed in chat
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Run the bot
bot.run()
