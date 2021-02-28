import requests
import json
import matplotlib.pyplot as plt
import misc
import discord


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
        sum_grades = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0,
                      'B': 0, 'B-': 0, 'C+': 0, 'C': 0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0, 'W': 0}
        term_string = {"20s": "Spring 2020", "19s": "Spring 2019",
                       "18s": "Spring 2018", "19f": "Fall 2019", "18f": "Fall 2018", "17f": "Fall 2017"}
        color_map = ['darkgreen', 'green',
                     'lime', 'greenyellow', 'yellowgreen', 'goldenrod', 'gold', 'orange', 'darkorange', 'orangered', 'red', 'firebrick',
                     'darkred', 'darkgray']
        response = requests.get(url)
        print(response.status_code)
        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        # misc.jprint(response_dict)
        data = response_dict["data"]
        for section in data:
            grade_dict = section["grades"]
            for grade in grade_dict.keys():
                sum_grades[grade] = sum_grades[grade] + grade_dict[grade]

        valid_class = False
        for num in sum_grades.values():
            if num != 0:
                valid_class = True
        if valid_class:
            keys = sum_grades.keys()
            values = sum_grades.values()
            plt.bar(keys, values, color=color_map)
            plt.title(f"{course.upper()} - {term_string[term]}")
            plt.savefig('img/plt.png')
            await message.channel.send(file=discord.File('img/plt.png'))
        else:
            await message.channel.send("The course or term could not be found.")

    # if this fails, return error message
    except (IndexError, RuntimeError, KeyError):
        await message.channel.send("The course or term could not be found.")
