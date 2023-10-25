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


token = ""
bot.run(token)  # Starts the bot