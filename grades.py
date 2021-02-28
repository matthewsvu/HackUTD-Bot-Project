import requests
import json
import matplotlib as plt
import numpy as np
import misc


async def get_grades(message):  # extract course and terms from the command

    try:
        command = message.content
        arr = command.strip().split()  # strip whitespace and split the message into an array
        course = arr[1]
        term = arr[2]
        url = f"https://coursebook-api.herokuapp.com/v1/grades//{term}//{course}"
        await plot_grades(message, course, term, url)
    # if this fails, return error message
    except (IndexError):
        await message.channel.send("Invalid format. Please enter a term and course like 'cs1337 20s'")


async def plot_grades(message, course, term, url):
    try:
        response = requests.get(url)
        print(response.status_code)
        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        misc.jprint(response_dict)
        data = response_dict["data"]
    # if this fails, return error message
    except (IndexError, RuntimeError):
        await message.channel.send("The course or term could not be found.")


# async def display_graph():
