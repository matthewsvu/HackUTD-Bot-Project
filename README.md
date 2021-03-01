## Inspiration
We wanted to create an easy way to compile information about grade distributions across classes and display it in a way that is easy to understand onto a discord bot.   
  
As students, we are constantly having discussions about what classes and professors to take, especially during registration. In a virtual environment, having these conversations can be a little disjunct, considering all the resources students use. Thus, having a discord bot compile common resources will give students an easy way to access and understand the information across all of UTD. 
## What CourseBot does

The bots works with 4 functionalities or commands:
```
$rmp <first> <last>
$grades <course> <term>
$grades <course> <term> <first_name> <last_name>
$find <first> <last>
```
With `$rmp`, users can get a summary of any professor's reviews from [ratemyprofessors](https://www.ratemyprofessors.com/) instantly.  
The `$grades` command displays a score distribution for courses and allows users to specify specific professors to display.
Using `$find`, students can easily access professor contact information.
## How we built CourseBot
We created a Discord bot using Python, Flask, CourseBookAPI, and RateMyProfessorPyAPI. Our Flask web server is deployed on Heroku for 24/7 hosting.  
__Backend__: Our bot utilizes common Python libraries such as discord.py and matplotlib to generate graphs and output messages.  
__Deployment:__ Our bot is deployed on Heroku using a Flask web server.
## Challenges we ran into
The challenges we ran into are the use of the CourseBookAPI and RateMyProfessorPyAPI. These were non-professionally maintained APIs that sometimes had features/functionalities broken about them. This caused several headaches when deploying our bot onto Heroku as it could never find the modules for these APIs.
## Accomplishments that we're proud of
For many of us, this was our first time interacting with APIs and requesting data with them. Our team found a lot of enjoyment in the hacking process, especially when first deploying our web server on Heroku. Many small accomplishments such as getting our graph data displayed correctly and getting the bot to respond encouraged us to keep pushing to the final stretch. 
## What we learned
Despite the limited amount of functionality we currently have, I think all of us could take away a lot of technical knowledge from this hackathon. We learned a lot about creating a project with a limited amount of knowledge in deploying software onto the web, writing a discord bot, and collaborating together as a team. All in all, we're much stronger developers that have an application that we're proud of.
## What's next for Temoc Course Bot
Potential next steps for Temoc Course Bot are scaling our software to multiple UTD Discord servers or making the bot a general bot that works for all universities.   
  
In this day and age, the way for students to communicate is by Discord. Scaling this bot up to handle multiple requests from dozens of users at a time by hosting it on cloud services like AWS, Azure, or GCP would be a potential pathway. In the end, our bot can hopefully help other students at UTD.
