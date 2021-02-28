import discord
import matplotlib
import requests
import json

client = discord.Client()

# open the key needed to run the bot
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

# scan all messages sent
@client.event
async def on_message(message):
    if message.author == client.user: # we don't want the bot to respond to itself
        return

    if message.content.startswith('$find'): # if any message starts with $find, get professor information
        await get_professor(message)

    if message.content.startswith('$grades'):
        await get_grades(message)


async def get_professor(message): # extract professor's name from the command

    try: 
        
        command = message.content
        arr = command.strip().split() # strip whitespace and split the message into an array
        first_name = arr[1] # extract a first name
        last_name = arr[2] # extract a last name
        formatted_name = first_name + "%20" + last_name # generate the full name of the professor
        url = "https://coursebook-api.herokuapp.com/v1/prof/" + formatted_name # use this to access the API of UTD Coursebook
        await output_prof(message, first_name, last_name, url) # output professor information

    # if this fails, return error message
    except (IndexError): 
        await message.channel.send("Invalid format. Please enter a name like 'John Smith'")


async def output_prof(message, first_name, last_name, url): # output professor information

    try:
        response = requests.get(url) 
        print(response.status_code)
        response_dict = response.json() # set a list equal to the json list from the API of UTD Coursebook
        data = response_dict["data"][0] # extract dictionary from the list

        output = "```" # start creating output

        output += "Name: " + data["name"] # add name to output, first!
        output += "\n"

        for key in data.keys(): # look through entire dictionary
            if key != "name": # add the contents of dictionary to the output
                output += key.title() + ": " + data[key] + '\n' # 

        output += "```" # end creating output
        await message.channel.send(output)

    # if this fails, return error message
    except (IndexError, RuntimeError):
        await message.channel.send(f"The professor '{first_name.title()} {last_name.title()}' could not be found.")


client.run(key)
