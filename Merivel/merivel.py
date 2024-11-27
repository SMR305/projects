import os
from twitchio.ext import commands

# Replace these with your own credentials (I suggest making a .env and setting them in there)
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
    if message.author.name.lower() == bot.nick.lower():
        return

    # Key phrase to trigger a ban
    key_phrases = ["cheap viewers", "best viewers on"]

    # Check if the key phrase is in the message content
    for key in key_phrases:
        if key in message.content.lower():
            # Ban the user
            await message.channel.send(f"/timeout {message.author.name} 60 Suspected Bot used {key}")
            return  # Stop processing further commands for this message

# Command: Responds with "Hello, {user}!" when "!hello" is typed in chat
@bot.command(name='Hello')
async def merivel_hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Command: Announces that the user is going to be lurking
@bot.command(name='Lurk')
async def merivel_lurk(ctx):
    await ctx.sent('Thanks for the support! Hope you enjoy the stream!')

#Command: Responds with the list of available commands
@bot.command(name='Merivel')
async def merivel_commands(ctx):
    commands_list = [
        "!Hello - Merivel says hello to you",
        "!Lurk - Lets me know you're here even if you're just lurking",
        "!Merivel - Gives you this list of commands",
    ]
    response = "Available commands: " + " | ".join(commands_list)
    
    await ctx.send(response)

@bot.command(name='Quit_Merivel')
async def merivel_quit(ctx):
    if ctx.author.name == TWITCH_CHANNEL_NAME:
        ctx.send("Bye Everyone!")
        exit()

# Run the bot
if __name__ == "__main__":
    bot.run()
