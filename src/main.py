from discord.ext import commands
import discord
import random

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


token = ""
bot.run(token)  # Starts the bot