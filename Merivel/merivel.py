import os
from twitchio.ext import commands
import pygame
import random
import time

# Set the current directory to the folder the program is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Replace these with your own credentials (I suggest making a .env and setting them in there)
# TWITCH_BOT_TOKEN = 'your_oauth_token_here'
# TWITCH_CLIENT_ID = 'your_TWITCH_CLIENT_ID'
# TWITCH_CHANNEL_NAME = 'target_TWITCH_CHANNEL_NAME'
TWITCH_BOT_TOKEN = os.environ['TWITCH_BOT_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']
TWITCH_CHANNEL_NAME = os.environ['TWITCH_CHANNEL_NAME']

# Initialize the mixer
pygame.mixer.init()

global start_time
start_time = time.time()

global downtime
downtime = 90

global cool
cool = False

# Initialize the bot
bot = commands.Bot(
    token=TWITCH_BOT_TOKEN,
    client_id=TWITCH_CLIENT_ID,
    nick='merivel_bot',
    prefix='!',
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
    if not message.author:
        return

    # Key phrase to trigger a ban
    key_phrases = ["cheap viewers", "best viewers on"]

    # Check if the key phrase is in the message content
    for key in key_phrases:
        if key in message.content.lower():
            # Timeout the user for 60 seconds
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

# Secret Command: Plays a random sound from the sounds directory
@bot.command(name='Prank')
async def merivel_prank(ctx):
    global start_time
    global cool
    if ((time.time() - start_time) < downtime) & cool:
        await ctx.send('Not so fast! You thought I was gonna let you spam this? Take a minute first!')
        return
    # Load and play the sound
    # Get a list of all files in the sounds directory
    sound_files = os.listdir('./sounds')

    # Choose a random file from the list
    random_sound = random.choice(sound_files)

    # Load and play the random sound
    pygame.mixer.music.load(os.path.join('./sounds', random_sound))
    pygame.mixer.music.play()
    print("Played sound: " + random_sound)
    start_time = time.time()
    cool = True

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

# Admin Command: Shuts Merivel Down
@bot.command(name='Quit_Merivel')
async def merivel_quit(ctx):
    if ctx.author.name == TWITCH_CHANNEL_NAME:
        ctx.send("Bye Everyone!")
        exit()

#Admin Command: Sets the downtime for the prank sound
@bot.command(name='Set_Downtime')
async def merivel_downtime(ctx):
    global downtime
    if ctx.author.name == TWITCH_CHANNEL_NAME:
        try:
            downtime = int(ctx.message.content.split(' ')[1])
            await ctx.send(f'New Cooldown {downtime} seconds.')
        except (ValueError, IndexError):
            await ctx.send('Invalid input. Please provide a valid number for downtime.')
    else:
        await ctx.send('Nice Try, but I saw that one coming.')

#Shows the status of the global variables
@bot.command(name='Prank-S')
async def merivel_status(ctx):
    message = f'Wait: {int(downtime - (time.time() - start_time))} seconds' if cool & (downtime - (time.time() - start_time) > 0) else 'Ready to go!'
    await ctx.send(message)
# Run the bot
if __name__ == "__main__":
    bot.run()
