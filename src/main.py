import json
from discord.ext import commands
import discord
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

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send(f"Salut tout seul {message.author.mention}")

    await bot.process_commands(message)


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

token = 
bot.run(token)  # Starts the bot