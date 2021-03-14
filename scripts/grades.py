import requests
import json
import matplotlib.pyplot as plt
import misc
import discord


sum_grades = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0,
              'B': 0, 'B-': 0, 'C+': 0, 'C': 0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0, 'W': 0}


async def get_grades(message):  # extract course and terms from the command

    try:
        command = message.content
        arr = command.strip().split()  # strip whitespace and split the message into an array
        course = arr[1]
        term = arr[2]
        url = f"https://coursebook-api.herokuapp.com/v1/grades//{term}//{course}"
        if len(arr) == 3:
            await plot_grades(message, course, term, url)
        elif len(arr) == 5:
            first_name = arr[3]
            last_name = arr[4]
            await plot_prof_grades(message, course, term, url, first_name, last_name)

    # if this fails, return error message
    except (IndexError):
        await message.channel.send("Invalid format. Please enter a term and course like 'cs1337 20s'")


async def output_graph(message, sum_grades, course, term, prof=None):
    color_map = ['darkgreen', 'green',
                 'lime', 'greenyellow', 'yellowgreen', 'goldenrod', 'gold', 'orange', 'darkorange', 'orangered', 'red', 'firebrick',
                 'darkred', 'darkgray']
    term_string = {"20s": "Spring 2020", "19s": "Spring 2019",
                   "18s": "Spring 2018", "19f": "Fall 2019", "18f": "Fall 2018", "17f": "Fall 2017"}
    valid_class = False
    for num in sum_grades.values():
        if num != 0:
            valid_class = True
    if valid_class:
        keys = sum_grades.keys()
        values = sum_grades.values()
        plt.clf()
        plt.bar(keys, values, color=color_map)
        if not prof:
            plt.title(f"{course.upper()} - {term_string[term]}")
        else:
            plt.title(f"{course.upper()} - {term_string[term]} - {prof}")
        plt.savefig('../img/plt.png')
        await message.channel.send(file=discord.File('../img/plt.png'))
    else:
        await message.channel.send("The course or term could not be found.")


async def plot_grades(message, course, term, url):
    try:
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
        misc.jprint(sum_grades)
        await output_graph(message, sum_grades, course, term)
    # if this fails, return error message
    except (IndexError, RuntimeError, KeyError):
        await message.channel.send("The course or term could not be found.")

# $grades cs1337 19f jason smith


async def plot_prof_grades(message, course, term, url, first_name, last_name):
    try:

        display_name = first_name.title() + " " + last_name.title()
        response = requests.get(url)
        print(response.status_code)
        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        data = response_dict["data"]
        for section in data:
            if (first_name.lower() in section["prof"].lower() and last_name.lower() in section["prof"].lower()):
                grade_dict = section["grades"]
                misc.jprint(section)
                for grade in grade_dict.keys():
                    sum_grades[grade] = sum_grades[grade] + grade_dict[grade]
        misc.jprint(sum_grades)
        await output_graph(message, sum_grades, course, term, prof=display_name)
    # if this fails, return error message
    except (IndexError, RuntimeError, KeyError):
        await message.channel.send("The course or term could not be found.")
