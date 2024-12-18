import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace these with your actual channel IDs
SOURCE_CHANNEL_ID = 1188420636406714368
ARCHIVE_CHANNEL_ID = 1319071742223978506
THREE_THUMBS_UP_CHANNEL_ID = 1286040119316451368
FOUR_THUMBS_UP_CHANNEL_ID = 1286040167550812330

@bot.event
async def on_reaction_add(reaction, user):
    print(f'Recognized on_reaction_add event...')
    if reaction.message.channel.id != SOURCE_CHANNEL_ID:
        return  # Ignore reactions from other channels
    
    if reaction.emoji == '👎':
        await move_message("Hey, a proposed game got a thumbs down and is moved to the archive:\n", reaction.message, ARCHIVE_CHANNEL_ID)

    if len(reaction.message.reactions) < 4:
        return  # Wait until there are at least 4 types of reactions

    # Check if the message has exactly 4 reactions (thumbs up, thumbs down, shrug)
    reactions = reaction.message.reactions
    thumbs_up = 0
    shrug = 0

    for react in reactions:
        if react.emoji == '👍':
            print(f'Recognized thumbs up...')
            thumbs_up = thumbs_up + 1
        elif react.emoji == '🤷':
            print(f'Recognized shrug...')
            shrug = shrug + 1

    total_voters = sum([reaction.count for reaction in reactions])
    if total_voters != 4:
        return  # Only process if exactly 4 voters have reacted

    if thumbs_up == 4:
        # Move to the thumbs-up channel
        await move_message("Hey, a new game is liked by everyone:\n", reaction.message, FOUR_THUMBS_UP_CHANNEL_ID)
    elif thumbs_up == 3:
        # Move to the three-thumbs-up channel
        for react in reactions:
            if react.emoji == '🤷':
                users = [user async for user in reaction.users()]
        await move_message(f"Hey, a new game is liked by everyone but one unimportant person, boooh:\n{users[0]}", reaction.message, THREE_THUMBS_UP_CHANNEL_ID)
    else:
        # Game is not interesting, move to archive channel
        await move_message("Hey, a proposed game got max 2 likes and is moved to the archive:\n", reaction.message, ARCHIVE_CHANNEL_ID)

async def move_message(message_addition, message, destination_channel_id):
    destination_channel = bot.get_channel(destination_channel_id)
    if destination_channel:
        # Send the message content to the new channel
        await destination_channel.send(f"{message_addition}{message.content}")
        # Optionally, delete the original message
        await message.delete()

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)  # Make sure the bot still processes commands

bot.run('key...')