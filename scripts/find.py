import requests
import json
import discord


async def get_professor(message):  # extract professor's name from the command

    try:

        command = message.content
        arr = command.strip().split()  # strip whitespace and split the message into an array
        first_name = arr[1]  # extract a first name
        last_name = arr[2]  # extract a last name
        # generate the full name of the professor
        formatted_name = first_name + "%20" + last_name
        url = "https://coursebook-api.herokuapp.com/v1/prof/" + \
            formatted_name  # use this to access the API of UTD Coursebook
        # output professor information
        await output_prof(message, first_name, last_name, url)

    # if this fails, return error message
    except (IndexError):
        await wrong_format(message)


async def output_prof(message, first_name, last_name, url):  # output professor information

    try:
        response = requests.get(url)
        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        data = response_dict["data"][0]  # extract dictionary from the list

        emoji = u"\U0001F9D1\U0000200D\U0001F3EB"
        embed = discord.Embed(
            title=f"{emoji} {data['name']}, {data['title']}",
            color=0x008542
        )
        embed.add_field(name="Email",
                        value=data['email'.lower(), inline=False)

        for key in data.keys():  # look through entire dictionary
            if key != "name" and key != 'title' and key != "email":  # add the contents of dictionary to the output
                embed.add_field(name=key.title(),
                                value=data[key], inline=True)

        await message.channel.send(embed=embed)

    # if this fails, return error message
    except (IndexError, RuntimeError):
        await prof_not_found(message)


async def prof_not_found(message):
    emoji = u"\U0001F50E"
    embed = discord.Embed(
        title=f"{emoji} Professor not found",
        description="The professor could not be found.",
        color=0xC75B12
    )
    await message.channel.send(embed=embed)


async def wrong_format(message):
    emoji = u"\U000026D4"
    embed = discord.Embed(
        title=f"{emoji} Incorrect formatting",
        description="Please blah blah blah",
        color=0xff0033
    )
    await message.channel.send(embed=embed)
