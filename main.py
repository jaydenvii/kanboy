import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import datetime

def reset(dict):
    new_dict = {}
    count = 1
    for val in dict.values():
        new_dict[count] = val
        count += 1

    return new_dict

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

BOARDS = [["UNTITLED BOARD", {}, {}, {}]]

EMBEDS = [None]

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

    await ctx.send("pong")

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
@app_commands.describe(task = "What is your task?")
@app_commands.choices(option=[
        app_commands.Choice(name="HIGH", value=1),
        app_commands.Choice(name="MEDIUM", value=2),
        app_commands.Choice(name="LOW", value=3)
    ])
async def kanbanadd(interaction: discord.Interaction, task: str, option: app_commands.Choice[int]):
    BOARDS[curr_board][TODO][len(BOARDS[curr_board][TODO])+1] = [task, HIGH]
    print(BOARDS[curr_board][TODO])
    await interaction.response.send_message(f"Added **{task}** with **{option.name}** priority.")

@bot.tree.command(name="kanbanmove")
@app_commands.choices(move_from=[
        app_commands.Choice(name="TO-DO", value=1),
        app_commands.Choice(name="DOING", value=2),
        app_commands.Choice(name="DONE", value=3)
    ])
@app_commands.describe(task_number = "Column to move task to?")
@app_commands.choices(move_to=[
        app_commands.Choice(name="TO-DO", value=1),
        app_commands.Choice(name="DOING", value=2),
        app_commands.Choice(name="DONE", value=3)
    ])
async def kanbanmove(interaction: discord.Interaction, move_from: app_commands.Choice[int], task_number: int, move_to: app_commands.Choice[int]):
    BOARDS[curr_board][move_to.value][len(BOARDS[curr_board][move_to.value])+1] = BOARDS[curr_board][move_from.value][task_number]
    del BOARDS[curr_board][move_from.value][task_number]
    BOARDS[curr_board][move_from.value] = reset(BOARDS[curr_board][move_from.value])
    await interaction.response.send_message(f"Moved **{move_from.name}**, task **{task_number}** to **{move_to.name}**")

@bot.tree.command(name="kanbanclear")
async def kanbanclear(interaction: discord.Interaction):
    BOARDS[curr_board] = ["UNTITLED BOARD", {}, {}, {}]
    await interaction.response.send_message("Cleared kanban board.")

bot.run(TOKEN)