import ratemyprofessor as rate
import discord
import math
import requests as requests
from bs4 import BeautifulSoup

school = "The University of Texas at Dallas"

"""
Gets the ratings of professors from UTD from the RateMyProfessorAPI

:param message: The "$rmp <first> <last>
:return: formatted message of the professor's RateMyProfessor information
"""
async def get_rating(message):
    try:
        arr = message.content.strip().split()
        first_name = arr[1]
        last_name = arr[2]
        name = first_name.title() + " " + last_name.title()
        professor = rate.get_professor_by_school_and_name(
            rate.get_school_by_name(school), name)
        rating_stars = ""
        for value in range(math.floor(professor.rating)):
            rating_stars += "\u2605"

        while len(rating_stars) != 5:
            rating_stars += "\u2606"

        diff_stars = ""
        for num in range(math.floor(professor.difficulty)):
            diff_stars += "\u2605"

        while len(diff_stars) != 5:
            diff_stars += "\u2606"

        output = f"```Name: {professor.name.title()}\n"
        if (professor.department.lower() != "select department"):
            output += f"Department: {professor.department}\n"
        else:
            output += "Department: Unknown\n"
        output += f"Rating: {rating_stars} ({professor.rating})\nDifficulty: {diff_stars} ({professor.difficulty})\nTotal Ratings: {professor.num_ratings}\n"
        if professor.would_take_again:
            output += f"Would Take Again: {round(professor.would_take_again, 1)}%```"
        else:
            output += f"Would Take Again: N/A```"

        await message.channel.send(output)
    except (RuntimeError, IndexError, AttributeError):
        await message.channel.send("The professor's ratings cannot be found.")

async def get_help():

    output = f"4 commands:\n```$rmp <first> <last>\n$grades <course> <term>\n$grades <course> <term> <first_name> <last_name>\n$find <first> <last>```\n"
    output += f"``$rmp`` fetches ratings from ratemyprofessor.com instantly.\n"
    output += f"``$grades`` displays a graph of student grades for selected course and term, with the option of adding a specific professor.\n"
    output += f"``$find`` displays a selected professor's contact information.\n"
    output += f"**Format**\n"
    output += f"``<term>``: <two-digit year><single letter semester> (ie. Spring 2020 is 20s, Fall 2019 is 19F)\n"
    output += f"``<course>``: <subject code><number> (ie. cs1337, CHEM1311)\n"
    output += f"``<first>`` and ``<last>``: Valid professor first and last names"

    await message.channel.send(output)
