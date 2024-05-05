import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import datetime
import asyncio

# TODO
# - /currentboard
# - priority indicators
# - add user custom streaks


from openai import OpenAI

### BOT STUFF
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())

def get_streak():
    with open("streak.json", "r") as f:
        
        return json.load(f)

def write_streak(task):
    # js = {task: num+1}
    streak[task] += 1
    out = json.dumps(streak, indent = 4)
    
    with open("streak.json", "w") as f:
        f.write(out)
        
def add_streak(task):
    write_streak(task)

streak = get_streak()

def make_streak_board():
    streak_board = discord.Embed(colour=0x00b0f4)
    streak_board.set_author(name="KEVIN'S STREAKS")
    streak_board.add_field(name="STUDY",
                    value = streak["study"],
                    inline=True)
    streak_board.add_field(name="WORKOUT",
                    value = streak["workout"],
                    inline=True)
    streak_board.add_field(name="PRACTICE",
                    value = streak["practice"],
                    inline=True)
    streak_board.add_field(name="MEDITATE",
                    value = streak["meditate"],
                    inline=True)
    streak_board.set_thumbnail(url="https://cdn.discordapp.com/attachments/1236334285636505693/1236423368463618088/IMG_4296.jpg?ex=6637f47e&is=6636a2fe&hm=c40a7f52b3f3adb0ab7a9aaf7a37748aeaa2cf1b294f91c75d00fe0b748b9fe0&")
    streak_board.set_footer(text="THIS IS THE FOOTER")
                    # icon_url="https://slate.dan.onl/slate.png")
    
    return streak_board



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

RED = 0xFF0000
GREEN = 0x00ff00
BLUE = 0x0000ff
YELLOW = 0xffff00
FUCHSIA = 0xff00ff
AQUA = 0x00ffff
WHITE = 0xffffff
BLACK = 0x000000

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
prio = ["", "HIGH", "MEDIUM", "LOW"]
NAME = 0
TODO = 1
DOING = 2
DONE = 3

BOARDS = [["UNTITLED BOARD", {}, {}, {}, 0x00ff00]]

EMBEDS = [None for i in range(1024)]

# testing command
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

### KANBAN COMMANDS
# displays current board
@bot.tree.command(name="kanban")
async def kanban(interaction: discord.Interaction):       
    embed = discord.Embed(colour=BOARDS[curr_board][4])
    embed.set_author(name=BOARDS[curr_board][NAME])
    embed.add_field(name=":pushpin: TODO",
                    value = "\n".join([f"{i}. {BOARDS[curr_board][TODO][i][0]} [{prio[BOARDS[curr_board][TODO][i][1]]}]" for i in range(1, len(BOARDS[curr_board][TODO]) + 1)]),
                    inline=True)
    embed.add_field(name=":person_running: DOING",
                    value="\n".join([f"{i}. {BOARDS[curr_board][DOING][i][0]} [{prio[BOARDS[curr_board][DOING][i][1]]}]" for i in range(1, len(BOARDS[curr_board][DOING]) + 1)]),
                    inline=True)
    embed.add_field(name=":white_check_mark: DONE",
                    value = "\n".join([f"{i}. {BOARDS[curr_board][DONE][i][0]} [{prio[BOARDS[curr_board][DONE][i][1]]}]" for i in range(1, len(BOARDS[curr_board][DONE]) + 1)]),
                    inline=True)
    EMBEDS[curr_board] = embed
    await interaction.response.send_message(embed=EMBEDS[curr_board])

# adds task to current board
@bot.tree.command(name="kanbanadd")
@app_commands.describe(task = "What is your task?")
@app_commands.choices(priority=[
        app_commands.Choice(name="HIGH", value=1),
        app_commands.Choice(name="MEDIUM", value=2),
        app_commands.Choice(name="LOW", value=3)
    ])
async def kanbanadd(interaction: discord.Interaction, task: str, priority: app_commands.Choice[int]):
    BOARDS[curr_board][TODO][len(BOARDS[curr_board][TODO])+1] = [task, HIGH]
    print(BOARDS[curr_board][TODO])
    await interaction.response.send_message(f"Added **{task}** with **{priority.name}** priority.")

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
    BOARDS[curr_board][DONE] = {}
    await interaction.response.send_message(f"Cleared DONE list from {BOARDS[curr_board][0]}.")

@bot.tree.command(name="kanbanremove")
@app_commands.choices(remove_from=[
        app_commands.Choice(name="TO-DO", value=1),
        app_commands.Choice(name="DOING", value=2),
        app_commands.Choice(name="DONE", value=3)
    ])
@app_commands.describe(task_number = "Task to remove?")
async def kanbanremove(interaction: discord.Interaction, remove_from: app_commands.Choice[int], task_number: int):
    name = BOARDS[curr_board][remove_from.value][task_number][0]
    del BOARDS[curr_board][remove_from.value][task_number]
    BOARDS[curr_board][remove_from.value] = reset(BOARDS[curr_board][remove_from.value])   
    await interaction.response.send_message(f"Removed {name} from {BOARDS[curr_board][0]}.")

# lists all boards
@bot.tree.command(name="kanbanlistboards")
async def kanbanlistboard(interaction: discord.Interaction):
    embed = discord.Embed(colour=0x00b0f4)
    embed.set_author(name="LIST OF BOARDS")
    for i in range(len(BOARDS)):
        embed.add_field(name=BOARDS[i][0],
                    value="Board Number/ID: " + str(i),
                    inline=False)
    await interaction.response.send_message(embed=embed)

# renames board
@app_commands.describe(new_name = "New name for board?")
@app_commands.describe(board_number = "Board number? Run /kanbanlistboard for board numbers.")
@bot.tree.command(name="kanbanrenameboard")
async def kanbanrenameboard(interaction: discord.Interaction, new_name: str, board_number: int):
    BOARDS[board_number][0] = new_name
    await interaction.response.send_message(f"Renamed kanban board #{board_number} titled {new_name}.")

# recolours board
@app_commands.describe(board_number = "Board number? Run /kanbanlistboard for board numbers.")
@app_commands.choices(colour = [
    app_commands.Choice(name="RED", value = 0xFF0000),
    app_commands.Choice(name="GREEN", value = 0x00ff00),
    app_commands.Choice(name="BLUE", value = 0x0000ff),  
    app_commands.Choice(name="YELLOW", value = 0xffff00),
    app_commands.Choice(name="FUCHSIA", value = 0xff00ff),
    app_commands.Choice(name="AQUA", value = 0x00ffff),
    app_commands.Choice(name="WHITE", value = 0xffffff),
    app_commands.Choice(name="BLACK", value = 0x000000)
])
@bot.tree.command(name="kanbanrecolourboard")
async def kanbanrecolourboard(interaction: discord.Interaction, board_number: int, colour: app_commands.Choice[int]):
    BOARDS[board_number][4] = colour.value
    await interaction.response.send_message(f"Recoloured kanban board #{board_number} coloured {colour.name}.")

# adds new board
@app_commands.describe(name = "Name of new board?")
@app_commands.describe(colour = "Colour of new board?")
@app_commands.choices(colour = [
    app_commands.Choice(name="RED", value = 0xFF0000),
    app_commands.Choice(name="GREEN", value = 0x00ff00),
    app_commands.Choice(name="BLUE", value = 0x0000ff),  
    app_commands.Choice(name="YELLOW", value = 0xffff00),
    app_commands.Choice(name="FUCHSIA", value = 0xff00ff),
    app_commands.Choice(name="AQUA", value = 0x00ffff),
    app_commands.Choice(name="WHITE", value = 0xffffff),
    app_commands.Choice(name="BLACK", value = 0x000000)
])
@bot.tree.command(name="kanbanaddboard")
async def kanbanaddboard(interaction: discord.Interaction, name: str, colour: app_commands.Choice[int]):
    BOARDS.append([name, {}, {}, {}, colour.value])
    await interaction.response.send_message(f"Added new kanban board titled {name}.")

# switches board
@app_commands.describe(number = "Number of board to switch to?")
@bot.tree.command(name="kanbanswitchboard")
async def kanbanswitchboard(interaction: discord.Interaction, number: int):
    set_curr_board(number)
    await interaction.response.send_message(f"Moved to board #**{number}**, titled **{BOARDS[curr_board][0]}**")

@bot.tree.command(name="kanbangetstreak")
async def kanbanstreak(interaction: discord.Interaction):

    await interaction.response.send_message(embed=make_streak_board())
        
    # streak = get_streak()
    # await interaction.response.send_message(f"Streak: {streak}")


@bot.tree.command(name="kanbanaddstreak")
# @app_commands.describe(task = "what u wnat?!/1!?")
@app_commands.choices(priority = [
    app_commands.Choice(name="study", value = "study"),
    app_commands.Choice(name="workout", value = "workout"),
    app_commands.Choice(name="practice", value = "practice"),    
    app_commands.Choice(name="meditate", value = "meditate")
])
async def kanbanaddstreak(interaction: discord.Interaction, priority: str):
    add_streak(priority)
    # await interaction.response.send_message(f"Streak: {streak}")
    await interaction.response.send_message(embed=make_streak_board())

# CLOCK
def clock_embed_make(time):
    embed = discord.Embed(colour=0x00b0f4)
    if (time <= 0):
        embed.add_field(name="COUNTDOWN FINISHED", inline=True)
    else:
        if (time > 60):
            embed.add_field(name="COUNTDOWN", value=f"{time//60} minutes\n{time%60} seconds", inline=True)
        else:
            embed.add_field(name="COUNTDOWN", value=f"{time} seconds", inline=True)
    # embed=discord.Embed(title="COUNTDOWN", description="{placeholder}")
    # embed.add_field(name="{PLACEHOLDER}", value="", inline=True)
    
    return embed
    # await ctx.send(embed=embed)

@bot.tree.command(name="kanbancountdown")
@app_commands.choices(unit = [
    app_commands.Choice(name="minutes", value = "minutes"),
    app_commands.Choice(name="seconds", value = "seconds")
])
async def kanbancountdown(interaction: discord.Interaction, time: int, unit: str):
    
    if unit == "minutes":
        time *= 60
    await interaction.response.send_message(embed=clock_embed_make(time))
    
    # message = await interaction.response.send_message(f"Countdown: {time} seconds")
       
    # message = await interaction.original_response()
    
    while time > 0:
        await asyncio.sleep(0.7) 
        time -= 1
        # if time > 60:
            
        #     await message.edit(content=f"Countdown: {time//60} minutes\n{time%60} seconds")
        # await message.edit(content=f"Countdown: {time} seconds")
        
        await interaction.response.send_message(embed=clock_embed_make(time))
    await interaction.response.send_message(embed=clock_embed_make(time))
    # await message.edit(content="Countdown finished!")
    
    






 
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