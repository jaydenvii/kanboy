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
curr_board = 0

HIGH = 1
MEDIUM = 2
LOW = 3

NAME = 0
TODO = 1
DOING = 2
DONE = 3

BOARDS = [["MAIN BOARD", {}, {}, {}]]


default_embed = discord.Embed(colour=0x00b0f4)
default_embed.set_author(name="DEFAULT BOARD")
default_embed.add_field(name="TODO",
                value = "0",
                inline=True)
default_embed.add_field(name="DOING",
                value="0",
                inline=True)
default_embed.add_field(name="DONE",
                value = "0",
                inline=True)

EMBEDS = [default_embed]

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
    embed = discord.Embed(colour=0x00b0f4)
    embed.set_author(name=BOARDS[curr_board][NAME])
    embed.add_field(name="TODO",
                    value = "\n".join([f"{i}. {BOARDS[curr_board][TODO][i][0]}" for i in range(1, len(BOARDS[curr_board][TODO]) + 1)]),
                    inline=True)
    embed.add_field(name="DOING",
                    value="\n".join([f"{i}. {BOARDS[curr_board][DOING][i][0]}" for i in range(1, len(BOARDS[curr_board][DOING]) + 1)]),
                    inline=True)
    embed.add_field(name="DONE",
                    value = "\n".join([f"{i}. {BOARDS[curr_board][DONE][i][0]}" for i in range(1, len(BOARDS[curr_board][DONE]) + 1)]),
                    inline=True)
    EMBEDS[curr_board] = embed
    await interaction.response.send_message(embed=EMBEDS[curr_board])

@bot.tree.command(name="kanbanadd")
@app_commands.describe(task = "what is your task")
async def kanbanadd(interaction: discord.Interaction, task: str):
    BOARDS[curr_board][TODO][len(BOARDS[curr_board][TODO])+1] = [task, HIGH]
    print(BOARDS[curr_board][TODO])
    await interaction.response.send_message(f"added {task}")

@bot.tree.command(name="kanbanmove")
@app_commands.describe(task = "what is your task")
async def kanbanmove(interaction: discord.Interaction, task: int):
    await interaction.response.send_message(f"moved {task}")

@bot.tree.command(name="kanbanclear")
async def kanbanclear(interaction: discord.Interaction):
    await interaction.response.send_message("cleared kanban board")

bot.run(TOKEN)