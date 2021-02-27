import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('ODE1MzQyOTQxNzY5MzAyMDM3.YDrBSQ.mMNv3sT-AjgSMmbcucz-6X_m7GY')

