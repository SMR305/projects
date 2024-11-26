import os
from twitchio.ext import commands

# Replace these with your own credentials
# TWITCH_BOT_TOKEN = 'your_oauth_token_here'
# TWITCH_CLIENT_ID = 'your_TWITCH_CLIENT_ID'
# TWITCH_CHANNEL_NAME = 'target_TWITCH_CHANNEL_NAME'
TWITCH_BOT_TOKEN = os.environ['TWITCH_BOT_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']
TWITCH_CHANNEL_NAME = os.environ['TWITCH_CHANNEL_NAME']

# print(TWITCH_BOT_TOKEN)
# print(TWITCH_CLIENT_ID)
# print(TWITCH_CHANNEL_NAME)

# Initialize the bot
bot = commands.Bot(
    token=TWITCH_BOT_TOKEN,
    client_id=TWITCH_CLIENT_ID,
    nick='merivel_bot',
    prefix='!',  # This is the prefix for bot commands (e.g., !hello)
    initial_channels=[TWITCH_CHANNEL_NAME]
)

# Event: Runs when the bot is ready
@bot.event()
async def event_ready():
    print(f'Logged in as | {bot.nick}')
    print(f'Connected to channel | {TWITCH_CHANNEL_NAME}')

# Event: Runs every time a message is sent in chat
@bot.event()
async def event_message(message):
    # Prevent the bot from responding to its own messages
    print(message.content)
    if message.author.name.lower() == bot.nick.lower():
        return

    # Key phrase to trigger a ban
    key_phrase = "bananasoup"

    # Check if the key phrase is in the message content
    if key_phrase in message.content.lower():
        # Ban the user
        await message.channel.send(f"Hey, {message.author.name}!")
        return  # Stop processing further commands for this message

# Command: Responds with "Hello, {user}!" when "!hello" is typed in chat
@bot.command(name='Hello_Merivel')
async def hello_merivel(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command(name='Merivel_Commands')
async def merivel_commands(ctx):
    commands_list = [
        "!Hello_Merivel - Merivel says hello to you",
        "!Merivel_Commands - Gives you this list of commands",
    ]
    response = "Available commands: " + " | ".join(commands_list)
    
    await ctx.send(response)

# Run the bot
if __name__ == "__main__":
    bot.run()
