import ratemyprofessor as rate
import discord
from bs4 import BeautifulSoup as bs
import math
import requests as requests
# from bs4 import BeautifulSoup

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
        rating_stars += f" {professor.rating}"

        diff_stars = ""
        for num in range(math.floor(professor.difficulty)):
            diff_stars += "\u2605"
        while len(diff_stars) != 5:
            diff_stars += "\u2606"
        diff_stars += f" {professor.difficulty}"

        if (professor.department.lower() != "select department"):
            depart = f", {professor.department}"
        else:
            depart = ""

        if professor.would_take_again:
            take_again = f"{round(professor.would_take_again, 1)}%"
        else:
            take_again = "N/A"

        emoji = u"\U0001F9D1\U0000200D\U0001F3EB"
        embed = discord.Embed(
            title=f"{emoji} {name}{depart}",
            color=0x008542,
        )

        embed.add_field(name="Rating", value=rating_stars, inline=False)
        embed.add_field(name="Difficulty", value=diff_stars, inline=False)
        embed.add_field(name="Total Ratings",
                        value=professor.num_ratings, inline=False)
        embed.add_field(name="Would Take Again",
                        value=take_again, inline=False)

        await message.channel.send(embed=embed)
    except (RuntimeError, IndexError, AttributeError):
        await prof_not_found(message)

async def get_tags(message):
    try:
        arr = message.content.strip().split()
        first_name = arr[1]
        last_name = arr[2]
        professor_name = first_name.title() + " " + last_name.title()

        # get Professor object from API
        professor = rate.get_professor_by_school_and_name(
                rate.get_school_by_name(school),
                professor_name)
        
        # get the url of the professor's RMP page
        url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor.id
        page = requests.get(url)
        
        # parse the html elements for the professor's tags
        soup = bs(page.text, "html.parser")
        prof_tags = soup.find('div', 'TeacherTags__TagsContainer-sc-16vmh1y-0 dbxJaW').findAll("span", {"Tag-bs9vf4-0 hHOVKF"}, limit=5)
    
        if(len(prof_tags) == 0):
            await message.channel.send("Professor's tags could not be found.")
            return
        
        # output the tags in a formatted manner
        output = ''.join(tag.get_text() + "\n" if i != len(prof_tags)-1 else tag.get_text() for i, tag in enumerate(prof_tags))
        output_format = f"```{professor_name}'s top tags are:\n{output}```"
        await message.channel.send(output_format)
    except(RuntimeError, IndexError, AttributeError):
        await prof_not_found(message)


async def prof_not_found(message):
    emoji = u"\U0001F50E"
    embed = discord.Embed(
        title=f"{emoji} Ratings not found",
        description="The professor's RateMyProfessor page could not be found.",
        color=0xC75B12
    )
    await message.channel.send(embed=embed)
