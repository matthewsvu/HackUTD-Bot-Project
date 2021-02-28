from keep_alive import keep_alive
import discord
import find
import grades

client = discord.Client()

# open the key needed to run the bot
f = open("key.txt", "r")
key = f.read()
f.close()


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


keep_alive()

client.run(key)
