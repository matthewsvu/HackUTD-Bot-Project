import requests
import json
import matplotlib.pyplot as plt
import misc
import discord
from io import BytesIO
from matplotlib.ticker import MaxNLocator


async def get_grades(message):  # extract course and terms from the command

    try:
        # splits the command into necessary parts
        command = message.content
        arr = command.strip().split()  # strip whitespace and split the message into an array
        course = arr[1]
        term = arr[2]

        url = f"https://coursebook-api.herokuapp.com/v1/grades//{term}//{course}"

        if len(arr) == 3:
            # calls the normal version of plot grades
            await plot_grades(message, course, term, url)
        elif len(arr) == 5:
            # calls the version of plot grades with an optional professor
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

    # checks that there is at least one grade in to output
    valid_class = False
    for num in sum_grades.values():
        if num != 0:
            valid_class = True

    if valid_class:
        # sets up the figure, making sure only integers are used for the y-axis
        keys = sum_grades.keys()
        values = sum_grades.values()
        plt.clf()
        fig, ax = plt.subplots()
        ax.bar(keys, values, color=color_map)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=14)

        if not prof:
            # stack of books emoji
            emoji = u'\U0001f4da'
            # formats output with course as title and term as description
            fig_name = f"{emoji} {course.upper()}"
            descr = term_string[term]
        else:
            # teacher emoji
            emoji = u"\U0001F9D1\U0000200D\U0001F3EB"
            # formats output with professor name as a title and course name/term as description
            fig_name = f"{emoji} {prof}"
            descr = f"{course.upper()} - {term_string[term]}"

        # initializes the output embed
        embed = discord.Embed(
            title=fig_name, description=descr, color=0xe87500
        )

        # writes the current figure's bytes to a variable and creates a new discord file with it
        fig_IObytes = BytesIO()
        plt.savefig(fig_IObytes, format="png", dpi=80)
        fig_IObytes.seek(0)
        chart = discord.File(fig_IObytes, filename="grades.png")

        # attaches the discord file to the embed
        embed.set_image(
            url="attachment://grades.png"
        )
        # send the embed into the channel
        await message.channel.send(embed=embed, file=chart)
    else:
        # send an error message to the channel
        await message.channel.send("The course or term could not be found.")


async def plot_grades(message, course, term, url):
    sum_grades = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0,
                  'B': 0, 'B-': 0, 'C+': 0, 'C': 0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0, 'W': 0}
    try:
        # calls the api, receiving grades per section
        response = requests.get(url)
        print(response.status_code)

        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        data = response_dict["data"]

        # loops through each course that matches and sums it
        for section in data:
            grade_dict = section["grades"]
            for grade in grade_dict.keys():
                sum_grades[grade] = sum_grades[grade] + grade_dict[grade]

        # misc.jprint(sum_grades)

        await output_graph(message, sum_grades, course, term)

    # if this fails, return error message
    except (IndexError, RuntimeError, KeyError):
        await message.channel.send("The course or term could not be found.")

# $grades cs1337 19f jason smith


async def plot_prof_grades(message, course, term, url, first_name, last_name):

    sum_grades = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0,
                  'B': 0, 'B-': 0, 'C+': 0, 'C': 0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0, 'W': 0}
    try:

        display_name = first_name.title() + " " + last_name.title()
        response = requests.get(url)
        # print(response.status_code)

        # set a list equal to the json list from the API of UTD Coursebook
        response_dict = response.json()
        data = response_dict["data"]

        # loops through each class section fetched from the API, adding scores only if the professor matches
        for section in data:
            if (first_name.lower() in section["prof"].lower() and last_name.lower() in section["prof"].lower()):
                grade_dict = section["grades"]
                misc.jprint(section)
                for grade in grade_dict.keys():
                    sum_grades[grade] = sum_grades[grade] + grade_dict[grade]

        # misc.jprint(sum_grades)

        await output_graph(message, sum_grades, course, term, prof=display_name)

    # if this fails, return error message
    except (IndexError, RuntimeError, KeyError):
        await message.channel.send("The course or term could not be found.")
