import RateMyProfessorPyAPI.ratemyprofessor as rate
import discord
import math

school = 1273


async def get_rating(message):
    try:
        arr = message.content.strip().split()
        first_name = arr[1]
        last_name = arr[2]
        name = first_name.title() + " " + last_name.title()
        school = "The University of Texas at Dallas"
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
