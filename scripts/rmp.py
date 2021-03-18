import ratemyprofessor as rate
import discord
import logging as log
import sys
from bs4 import BeautifulSoup as bs
import math
import requests as requests
# for printing error messages for exceptions
log.basicConfig(stream=sys.stderr, 
                level=log.ERROR)

school = "The University of Texas at Dallas"

"""
Gets the ratings of professors from UTD from the RateMyProfessorAPI

:param message: The "$rmp <first> <last>"
:return: formatted message of the professor's RateMyProfessor information
"""

async def get_rating(message):
    try:
        # extracts content from message, removes white space
        arr = message.content.strip().split()
        first_name = arr[1]
        last_name = arr[2]
        name = first_name.title() + " " + last_name.title()

        # Grabs Professor object from RMPpy API
        professor = rate.get_professor_by_school_and_name(
            rate.get_school_by_name(school), name)

        # RMP Rating star field
        rating_stars = ""
        for value in range(math.floor(professor.rating)):
            rating_stars += "\u2605"
        while len(rating_stars) != 5:
            rating_stars += "\u2606"
        rating_stars += f" {professor.rating}"

        # RMP difficulty star field
        diff_stars = ""
        for num in range(math.floor(professor.difficulty)):
            diff_stars += "\u2605"
        while len(diff_stars) != 5:
            diff_stars += "\u2606"
        diff_stars += f" {professor.difficulty}"

        # RMP professor department field
        if (professor.department.lower() != "select department"):
            depart = f", {professor.department}"
        else:
            depart = ""

        # RMP would take again field
        if professor.would_take_again:
            take_again = f"{round(professor.would_take_again, 1)}%"
        else:
            take_again = "N/A"
        
        # Scrape top tags and most helpful rating from RMP website
        tags, helpful_rating = get_more_rmp_info(professor)
        
        # creates a discord embed object for the professor
        emoji = u"\U0001F9D1\U0000200D\U0001F3EB"
        embed = discord.Embed(
            title=f"{emoji} {name}{depart}",
            color=0x008542,
        )
        
        embed.add_field(name="Rating",
                        value=rating_stars, inline=False)
        embed.add_field(name="Difficulty",
                        value=diff_stars, inline=False)
        embed.add_field(name="Total Ratings",
                        value=professor.num_ratings, inline=False)
        embed.add_field(name="Would Take Again",
                        value=take_again, inline=False)
        embed.add_field(name="Top Tags",
                        value=tags, inline=False)
        embed.add_field(name="Most Helpful Rating",
                        value=helpful_rating, inline=False)

        await message.channel.send(embed=embed)
    except (RuntimeError, IndexError, AttributeError) as e:
        log.error(e)
        await prof_not_found(message)

"""
Basic webscraping function that retrieves a selected professor's top tags and most helpful rating

:param message, professor of type Professor
:return string, string either output or error message
"""

def get_more_rmp_info(professor : rate.Professor):
    # get the url of the professor's RMP page
    url = f"https://www.ratemyprofessors.com/ShowRatings.jsp?tid={professor.id}" 
    page = requests.get(url)
        
    # parse the html elements for the professor's tags and most helpful rating
    soup = bs(page.text, "html.parser")
    prof_tags = soup.find('div', 'TeacherTags__TagsContainer-sc-16vmh1y-0 dbxJaW')
    helpful_rating = soup.find("div", 'HelpfulRating__StyledRating-sc-4ngnti-0 jzbtsI')

    # join all the top tags together in a formatted manner ex : <tag>, <tag>, <tag>, until one index before the end
    if prof_tags != None:
        prof_tags = prof_tags.findAll("span", {"Tag-bs9vf4-0 hHOVKF"}, limit=5)
        tags_formatted = ''.join(tag.get_text().title() + ", " if index != len(prof_tags)-1 else tag.get_text().title() for index, tag in enumerate(prof_tags))

    # finds the most helpful rating text    
    if helpful_rating != None:
        helpful_rating = helpful_rating.find('div', 'Comments__StyledComments-dzzyvm-0 gRjWel').get_text()

    tags_error_message = f"{professor.name}'s tags could not be found."
    comment_error_message = f"{professor.name}'s most helpful rating could not be found."

    # when both elements in html can't be found exit with message
    if prof_tags == None or len(prof_tags) == 0 and helpful_rating == None:
        return tags_error_message, comment_error_message
    elif len(prof_tags) == 0 or prof_tags == None: # tags don't exist for professor
        return tags_error_message, helpful_rating
    elif helpful_rating == None: # helpful rating could not be found
        return tags_formatted, comment_error_message
    
    # otherwise output the tags and helpful rating in a formatted manner    

    return tags_formatted, helpful_rating

"""
 A function that return the an embed that the RMP page can't be found when an exception is thrown
 :param message: 
 :return An embed object
"""   

async def prof_not_found(message):
    emoji = u"\U0001F50E"
    embed = discord.Embed(
        title=f"{emoji} Ratings not found",
        description="The professor's RateMyProfessor page could not be found.",
        color=0xC75B12
    )
    await message.channel.send(embed=embed)
