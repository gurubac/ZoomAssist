# LA HACKS 2021

<p align="center">
  <img src="https://raw.githubusercontent.com/gurubac/lahacks21/mahir/Transparent%20Logo.png" />
</p>

## ZoomAssist
A discord bot that integrates Zoom setup through the Discord chat interface
## Installation Guide
Create a .env file located in the same LAHACKS2021 Folder, and set the environmental variables. Then create an app on zoom, and add your JWT token. 
Due to lack of hosting, we cannot provide our discord token, so you may create your own bot application on discord and set that token as an environmental variable using our program.

Install python3 onto your computer. Navigate to LAHACKS2021 Folder, and run main.py.

To run, type `python3 main.py` in the terminal.
## Command List
`.setschedule` OR `.sets` OR `.changeschedule` OR `.changesched` OR `.setSchedule` OR `.setS` to set the schedule for zoom meetings

`!status` to view the status of the meeting 

`!zoomschedule` to view the current schedule 

`!zoomschedule` + Class name to view all meeting times of a specific class

`.setTime` to set the default time for the zoom meeting 

`!meeting` to create a new zoom meeting

`.help` + meeting OR setschedule OR schedule OR status to get help on how to use any of the commands in the topic

`.setTime` + time (in 00:00 format) to set the default time for meetings if user didn't specify what subject was scheduled in `!meeting` command

## Issues We Ran into
We originally started out with a goal of creating a chat sync bot where it would sync the zoom chat to the discord chat, and you could send messages to the chats by doing zoom to discord chat or discord to zoom chat. However, complications arose due to the fact that we did not have the proper authentication needed. We need oath2 to access chat channels and get messages through the zoom api, and this authentication is only provided if you submit an app to the zoom marketplace. This requires a manual approval process from zoom itself, and this would take time. This is similar to how you would submit an app to the Apple appstore. So we used JWT authentication instead, and found out that we were very limited in what we could do with the API with there being paid features or features that are locked to certain account types, so we settled on generating new meetings, and creating scheduling for said meetings.