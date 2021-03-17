from keep_alive import keep_alive
import discord
import json
import find
import grades
import rmp
import misc

client = discord.Client()

# open the key needed to run the bot
with open('key.txt') as f:
    key = f.readlines()[0]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# scan all messages sent


@client.event
async def on_message(message):
    if message.author == client.user:  # we don't want the bot to respond to itself
        return

    # if any message starts with $find, get professor information
    if message.content.startswith('$find'):
        await find.get_professor(message)

    if message.content.startswith('$grades'):
        await grades.get_grades(message)

    if message.content.startswith('$tags'):
        await rmp.get_tags(message)

    if message.content.startswith('$rmp'):
        await rmp.get_rating(message)

    if message.content.startswith('$help'):
        await misc.get_help(message)

keep_alive()

client.run(key)
