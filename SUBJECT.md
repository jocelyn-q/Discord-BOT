# SIGL-BOT 2023

## Pre-requisites

- Have discord installed on your laptop or access it through a web browser

## Useful References

- Discord API Documentation : https://discord.com/developers/docs/intro
- Discord.py Library Documentation : https://discordpy.readthedocs.io/en/stable/index.html
- Python Package Manager Documentation : https://pypi.org/project/pip/

## Setup

- Create a new discord server, this will be your test sandbox for testing your bot
- Go to https://discord.com/developers/applications and create a new application. Give it the name you want and add a cool profile picture for it
- Under the 'bot' tab, click on 'Add a bot', give it a username as well
- Reveal your bot private token and paste it in `main.py`
- Activate developpers feature :
  - Go to discord settings > App settings > Advanced
  - Activate developper mode
- Right click on your nickname in the right-side bar of your server and click on ' Copy ID'. Paste it in the `author_id` variable ìn `main.py`
- Add the bot to your server by clicking on the OAuth2 tab
  - Select the `bot` scope and `Administrator` permissions
  - A URL will then be generated. By clicking on it, you will have the opportunity to add your bot to one of the server you already joined

## Advices

- **Code quality** and **lisibility** as well as documentation on how you solved problems will be greatly appreciated/rewarded
- Be careful not to push your discord Bot token in your git as it will instantly disable the token
- Cheating is allowed, but **getting catched isn't**
- Your bot ability to produce **well-formatted answers** on the server is as important as solving the problem
- You are allowed to invite members to your server for test purposes
- Creation of new files is recommended. Clean architectures will be rewarded
- Extra-miles are challenges to go further with a particular usecase. Focus on the Todo-list then the extra miles items

## TODO LIST

### Warm-up

[X] When typing `!name` the bot should write back the name of the user typing the command

[X] When typing `!d6` the bot should answer with a value between 1 and 6

[X] When typing "Salut tout le monde" (without the command sign), the bot should say "Salut tout seul" and ping the original author of the message

### Administration

[X] When typing `!admin <A member nickname>`, your bot should create an Admin role (if it doesn't exists) on your server, allowing them to manage channels, kick and ban members, and give it to the member in parameter

[X] When typing `!ban <A member nickname> <ban reason?>`, your bot should ban that member from the server (**Test with caution**) displaying the input reason for the ban. If no ban reason is input, your bot should display a funny catchphrase picked at random in a given list

[X] The command `!flood` should activate (or deactivate) a moderation workflow. When activated, your bot should monitor the messages and display a warning to any user posting more than X messages in the last Y minutes. The (de)activation should be confirmed using a custom message

### It's all fun and games

[ ] When typing `!xkcd`, your post should post a random comic from https://xkcd.com

[ ] When typing `!poll <question>`, your bot should post a @here mention followed by a Yes/No question. The bost will then write the question again in another message and add one :thumbsup: and one :thumbsdown: emoji reaction to its message

- Example : `!poll "Should we get burgers ?"`
- Extra-mile : Define a time-limit for the poll. When the limit has been reached, bot will bot a message with the final result and delete the original poll message

[ ] Create a chat-GPT integration with the command `!prompt <prompt to be processed>`

### Bonus

If you reached this point, congratulations, you have a basic bot for your discord server. Check for the extra-mile content if you didn't already. Otherwise, try to think of some fun or useful features to add to your bot among which :

- Setting reminders for events
- Rewarding the most active members of your server
- Advanced role management (Directing new members to a #rules channel and giving them basic permissions after they agree, sky is the limit )
