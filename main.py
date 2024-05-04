import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime

# BOT STUFF
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())

# KANBAN DATA
HIGH = 1
MEDIUM = 2
LOW = 3

TODO = {
    1: ["bio hw", LOW],
    2: ["do kevin", HIGH]
}
DOING = {
    1: ["kevin", HIGH]
}
DONE = {
    1: ["asdf", MEDIUM]
}

@bot.event
async def on_ready():
    print("online")

@bot.command()
async def ping(ctx):
    embed = discord.Embed(colour=0x00b0f4)

    embed.set_author(name="ISAAC'S BOARD")

    embed.add_field(name="TODO",
                    value="",
                    inline=True)
    embed.add_field(name="DOING",
                    value="1. doing\n2. thing",
                    inline=True)
    embed.add_field(name="DONE",
                    value="1. lol\n2. hehe\n3. hohooh",
                    inline=True)

    embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")

    embed.set_footer(text="Example Footer",
                    icon_url="https://slate.dan.onl/slate.png")

    await ctx.send(embed=embed)

bot.run(TOKEN)