import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import datetime
from openai import OpenAI

### BOT STUFF
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("online")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

### OPENAI STUFF
OPENAI_KEY = os.getenv("OPENAI_KEY")

### KANBAN DATA

# helper for listing tasks
def reset(dict):
    new_dict = {}
    count = 1
    for val in dict.values():
        new_dict[count] = val
        count += 1

    return new_dict

# sorts tasks by priority
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

# sets current board
def set_curr_board(num):
    global curr_board
    curr_board = num

curr_board = 0

HIGH = 1
MEDIUM = 2
LOW = 3

NAME = 0
TODO = 1
DOING = 2
DONE = 3

BOARDS = [["UNTITLED BOARD", {}, {}, {}]]

EMBEDS = [None for i in range(1024)]

# testing command
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

### KANBAN COMMANDS
# displays current board
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

# adds task to current board
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

# moves task on current board
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

# clears "DONE" on current board
@bot.tree.command(name="kanbanclear")
async def kanbanclear(interaction: discord.Interaction):
    BOARDS[curr_board] = ["UNTITLED BOARD", {}, {}, {}]
    await interaction.response.send_message("Cleared kanban board.")

# lists all boards
@bot.tree.command(name="kanbanlistboards")
async def kanbanlistboard(interaction: discord.Interaction):
    embed = discord.Embed(colour=0x00b0f4)
    embed.set_author(name="LIST OF BOARDS")
    for i in range(len(BOARDS)):
        embed.add_field(name=BOARDS[i][0],
                    value = str(i),
                    inline=False)
    await interaction.response.send_message(embed=embed)

# renames board
@app_commands.describe(name = "New name for board?")
@app_commands.describe(name = "Board number? Run /kanbanlistboard for board numbers.")
@bot.tree.command(name="kanbanrenameboard")
async def kanbanrenameboard(interaction: discord.Interaction, name: str, board_number: int):
    BOARDS[board_number][0] = name
    await interaction.response.send_message(f"Renamed kanban board #{board_number} titled {name}.")

# adds new board
@app_commands.describe(name = "Name of new board?")
@bot.tree.command(name="kanbanaddboard")
async def kanbanaddboard(interaction: discord.Interaction, name: str):
    BOARDS.append([name, {}, {}, {}])
    await interaction.response.send_message(f"Added new kanban board titled {name}.")

# switches board
@app_commands.describe(name = "Number of board to switch to?")
@bot.tree.command(name="kanbanswitchboard")
async def kanbanswitchboard(interaction: discord.Interaction, name: int):
    set_curr_board(name)
    await interaction.response.send_message(f"Moved to board #{name}.")

### KANBOY COMMANDS
@bot.tree.command(name="kanboy")
async def kanboy(interaction: discord.Interaction, prompt: str):
    client = OpenAI(api_key=OPENAI_KEY)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a studying assistant, knowledgeable in many different fields of math, science, arts, and engineering."},
        {"role": "user", "content": prompt}
    ]
    )

    response = completion.choices[0].message.content
    await interaction.response.send_message(response)

bot.run(TOKEN)