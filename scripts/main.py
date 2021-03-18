from keep_alive import keep_alive
import discord
import json
import find
import grades
import rmp
import misc

client = discord.Client()

with open('scripts/config.json') as f:
  data = json.load(f)
key = data['key']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# scan all messages sent
@client.event
async def on_message(message):
    if message.author == client.user:  # we don't want the bot to respond to itself
        return

    # if any message starts with $find, get a professor's contact information and details
    if message.content.startswith('$find'):
        await find.get_professor(message)
    # return a graph of the grades distribution for a class or a professor's section
    if message.content.startswith('$grades'):
        await grades.get_grades(message)
    # return the RateMyProfessor ratings for a specified professor
    if message.content.startswith('$rmp'):
        await rmp.get_rating(message)
    # return a list of commands and instructions
    if message.content.startswith('$help'):
        await misc.get_help(message)

keep_alive()

client.run(key)
