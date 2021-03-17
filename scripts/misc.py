import json
import discord


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


async def get_help(message):

    output = f"4 commands:\n```$rmp <first> <last>\n$grades <course> <term>\n$grades <course> <term> <first_name> <last_name>\n$find <first> <last>```\n"
    output += f"``$rmp`` fetches ratings from ratemyprofessor.com instantly.\n"
    output += f"``$grades`` displays a graph of student grades for selected course and term, with the option of adding a specific professor.\n"
    output += f"``$find`` displays a selected professor's contact information.\n"
    output += f"**Format**\n"
    output += f"``<term>``: <two-digit year><single letter semester> (ie. Spring 2020 is 20s, Fall 2019 is 19F)\n"
    output += f"``<course>``: <subject code><number> (ie. cs1337, CHEM1311)\n"
    output += f"``<first>`` and ``<last>``: Valid professor first and last names"

    await message.channel.send(output)
