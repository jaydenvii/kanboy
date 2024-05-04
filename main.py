import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import datetime

def sort(dict):
    new_dict = {}
    count = 1
    for val in dict.values():
        if val[1] == HIGH:
            new_dict[count] = val
            count += 1
    for val in dict.values():
        if val[1] == MEDIUM:
            new_dict[count] = val
            count += 1
    for val in dict.values():
        if val[1] == LOW:
            new_dict[count] = val
            count += 1

    return new_dict

# BOT STUFF
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())

# KANBAN DATA
HIGH = 1
MEDIUM = 2
LOW = 3

TODO = {
}
DOING = {
}
DONE = {
}

BOARDS = []

embed = discord.Embed(colour=0x00b0f4)
embed.set_author(name="ISAAC'S BOARD")
embed.add_field(name="TODO",
                value = "\n".join([f"{i}. {TODO[i][0]}" for i in range(1, len(TODO) + 1)]),
                # value=f"1.{TODO[1][0]} \n2.{TODO[2][0]}",
                # value=f"1. biohw\n2. do kevin",
                inline=True)
embed.add_field(name="DOING",
                value="\n".join([f"{i}. {DOING[i][0]}" for i in range(1, len(DOING) + 1)]),
                inline=True)
embed.add_field(name="DONE",
                value = "\n".join([f"{i}. {DONE[i][0]}" for i in range(1, len(DONE) + 1)]),
                # value="1. lol\n2. hehe\n3. hohooh",
                inline=True)
embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")
embed.set_footer(text="Example Footer",
                icon_url="https://slate.dan.onl/slate.png")

BOARDS.append(embed)

@bot.event
async def on_ready():
    print("online")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.command()
async def ping(ctx):

    await ctx.send(embed=BOARDS[0])

@bot.tree.command(name="kanban")
async def kanban(interaction: discord.Interaction):
    await interaction.response.send_message("this is where you see the kanban board")

@bot.tree.command(name="kanbanadd")
@app_commands.describe(task = "what is your task")
async def kanbanadd(interaction: discord.Interaction, task: str):
    await interaction.response.send_message(f"added {task}")

@bot.tree.command(name="kanbanmove")
@app_commands.describe(task = "what is your task")
async def kanbanmove(interaction: discord.Interaction, task: str):
    await interaction.response.send_message(f"moved {task}")

@bot.tree.command(name="kanbanclear")
async def kanbanclear(interaction: discord.Interaction):
    await interaction.response.send_message("cleared kanban board")

bot.run(TOKEN)