import discord
import matplotlib
import requests
import json

client = discord.Client()

f = open("key.txt", "r")
key = f.read()
f.close()


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$find'):
        # start plotting the graph
        # output the graph
        await get_professor(message)


async def get_professor(message):
    try:
        command = message.content
        arr = command.strip().split()
        first_name = arr[1]
        last_name = arr[2]
        formatted_name = first_name + "%20" + last_name
        url = "https://coursebook-api.herokuapp.com/v1/prof/" + formatted_name
        output_prof(first_name, last_name, url)

    except (IndexError):
        await message.channel.send("Invalid format. Please enter a name like 'John Smith'")


async def output_prof(first_name, last_name, url)
     try:
        response = requests.get(url)
        print(response.status_code)
        response_dict = response.json()
        data = response_dict["data"][0]
        output = "```"
        output += "Name: " + data["name"]
        output += "\n"
        for key in data.keys():
            if key != "name":
                output += key.title() + ": " + data[key] + '\n'
        output += "```"
        await message.channel.send(output)

    except (IndexError, RuntimeError):
        await message.channel.send(f"The professor '{first_name.title()} {last_name.title()}' could not be found.")


client.run(key)
