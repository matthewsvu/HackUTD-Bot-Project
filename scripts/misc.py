import json
import discord


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

"""
A help function that displays an embed of all the possible commands for the bot
:param message:
:return embed:
"""
async def get_help(message):
    emoji = u"\U00002139\U0000FE0F"
    embed = discord.Embed(
        title=f"{emoji} CourseBot Instructions",
        color=0x3399FF
    )
    command = "Use `$find` to display any professor's contact information\n"
    command += "Use `$grades` to display a graph of student grades for particular course or professor\n"
    command += "Use `$rmp` to fetch RateMyProfessor ratings for any professor"
    embed.add_field(
        name="Command Usage",
        value=command,
        inline=False
    )

    example = "`$find John Cole` - outputs John Cole's contact information\n\n"
    example += "`$grades MATH2414 20s` - outputs a graph of MATH2414 grades from Spring 2020\n\n"
    example += "`$grades CS3340 19f Richard Goodrum` - outputs a graph of all of Richard Goodrum's CS3340 grades from Fall 2019\n\n"
    example += "`$rmp Theresa Towner` - outputs a summary of Theresa Towner's ratings."
    embed.add_field(
        name="Example Commands",
        value=example,
        inline=False
    )

    data = "``Why is Fall 2020 not showing up?`` - There is no grades data from before Spring 2017 and after Spring 2020 currently."
    embed.add_field(
        name="FAQ",
        value=data,
        inline=False
    )
    await message.channel.send(embed=embed)
