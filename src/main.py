from discord.ext import commands
import discord
import asyncio
import json
import random
import http.client

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 142316744176828416  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    user_name = ctx.author.name
    await ctx.send(user_name)


@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.command()
async def admin(ctx, member: discord.Member):
    # Check if the "Admin" role exists, and create it if it doesn't
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role is None:
        admin_role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())

    # Assign the "Admin" role to the specified member
    if admin_role in member.roles:
        await ctx.send(f'{member.mention} is already an Admin!')
    else:
        await member.add_roles(admin_role)
        await ctx.send(f'{member.mention} is now an Admin!')


catchphrases = [
    "Catch this ratio bozo!",
    "Condamné à pisser du code pour une ESN",
    "Ratio",
    "Ratioed",
]

@bot.command()
async def ban(ctx, member: discord.Member, reason=""):
    if member is None:
        await ctx.send("Please mention a valid member to ban.")
        return

    if member not in ctx.guild.members:
        await ctx.send(f'{member.display_name} is not a member of this server!')
        return

    if not reason:
        ban_message = random.choice(catchphrases)
    else:
        # Ban the member with the provided reason
        ban_message = f'{member.display_name} has been banned for the reason: {reason}'

    await member.ban(reason=reason)
    await ctx.send(ban_message)

flood_monitoring_active = False
flood_message_limit = 5
flood_time_period = 1
user_activity = {}	

@bot.command()
async def flood(ctx):
    global flood_monitoring_active
    flood_monitoring_active = not flood_monitoring_active

    if flood_monitoring_active:
        response = "Flood detection is now active."
    else:
        response = "Flood detection is now deactivated."

    await ctx.send(response)

@bot.event
async def on_message(message):
    # Salut tout le monde and Flood detection
    if message.content == "Salut tout le monde":
        await message.channel.send(f"Salut tout seul {message.author.mention}")

    if flood_monitoring_active and not message.author.bot:
        user_id = message.author.id
        current_time = message.created_at
        
        if user_id in user_activity:
            user_activity[user_id]['message_count'] += 1
            user_activity[user_id]['timestamps'].append(current_time)
        else:
            user_activity[user_id] = {'message_count': 1, 'timestamps': [current_time]}

        # Check for flooders
        if user_activity[user_id]['message_count'] >= flood_message_limit:
            last_message_time = user_activity[user_id]['timestamps'][-flood_message_limit]
            time_difference = (current_time - last_message_time).total_seconds() / 60
            if time_difference <= flood_time_period:
                # Send a warning message to the user
                warning_message = f"{message.author.mention}, you're posting too many messages in a short time."
                await message.channel.send(warning_message)

    await bot.process_commands(message)

@bot.command()
async def xkcd(ctx):
    xkcd_api_url = "xkcd.com"
    connection = http.client.HTTPSConnection(xkcd_api_url)
    
    connection.request("GET", f"/{random.randint(1, 2846)}/info.0.json")
    response = connection.getresponse()
    
    if response.status == 200:
        data = response.read()
        
        comic_data = json.loads(data.decode("utf-8"))
        comic_image_url = comic_data["img"]
        
        await ctx.send(comic_image_url)
    else:
        await ctx.send("Failed to fetch XKCD comic.")

@bot.command()
# Example : !poll "Should we get burgers ?" 5
# The poll will be active for 5 minutes

# Example : !poll "Should we get burgers ?"
# The poll will be active until the bot is stopped
async def poll(ctx, question, time_limit_minutes=-1):
    # Mention @here and post the poll question
    poll_message = f"@here {ctx.author.display_name} has a poll question:\n**{question}**\nReact with 👍 or 👎 to vote."
    poll_message = await ctx.send(poll_message)

    # Send question with reactions
    message = f"{question}"
    question_message = await ctx.send(message)

    await question_message.add_reaction("👍")
    await question_message.add_reaction("👎")

    if time_limit_minutes > 0:
        await asyncio.sleep(time_limit_minutes * 60)

        result_poll_message = await ctx.channel.fetch_message(question_message.id)

        thumbs_up = 0
        thumbs_down = 0
        for reaction in result_poll_message.reactions:
            if str(reaction.emoji) == "👍":
                thumbs_up = reaction.count - 1
            elif str(reaction.emoji) == "👎":
                thumbs_down = reaction.count - 1

        # Post the final result message
        result_message = f"The poll question was: **{question}**\n" \
                     f"👍 Yes: {thumbs_up}\n" \
                     f"👎 No: {thumbs_down}\n" \
                     f"Poll ended."

        await ctx.send(result_message)

        await poll_message.delete()
        await question_message.delete()


@bot.command()
async def mychatgpt(ctx, *, user_prompt):
    try:
        # Create an HTTP connection to the OpenAI API
        connection = http.client.HTTPSConnection("api.openai.com")
        
        # Define the request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        # Create the request payload
        payload = {
            "prompt": user_prompt,
            "max_tokens": 50  # Adjust this to control response length
        }

        # Convert the payload to a JSON string
        payload_json = json.dumps(payload)

        # Send a POST request to the OpenAI API
        connection.request("POST", "/v1/engines/davinci/completions", payload_json, headers)
        response = connection.getresponse()
        response_data = response.read()
        response_dict = json.loads(response_data)

        # Get the GPT-3 response
        bot_response = response_dict["choices"][0]["text"]

        # Send the GPT-3 response to the Discord channel
        await ctx.send(f"**User Prompt:** {user_prompt}\n**GPT-3 Response:** {bot_response}")
    except Exception as e:
        await ctx.send("An error occurred while processing the prompt.")


token = ""
bot.run(token)  # Starts the bot