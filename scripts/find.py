import requests
import json


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
        await message.channel.send("Invalid format. Please enter a name like 'John Smith'")


async def output_prof(message, first_name, last_name, url):  # output professor information

    try:
        response = requests.get(url)
        print(response.status_code)
        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        data = response_dict["data"][0]  # extract dictionary from the list

        output = "```"  # start creating output

        output += "Name: " + data["name"]  # add name to output, first!
        output += "\n"

        for key in data.keys():  # look through entire dictionary
            if key != "name":  # add the contents of dictionary to the output
                output += key.title() + ": " + data[key] + '\n'

        output += "```"  # end creating output
        await message.channel.send(output)

    # if this fails, return error message
    except (IndexError, RuntimeError):
        await message.channel.send(f"The professor '{first_name.title()} {last_name.title()}' could not be found.")
