import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import datetime
import asyncio
from discord.ui import Button, View

# TODO
# - /currentboard
# - priority indicators
# - add user custom streaks

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

### KANBAN STUFF

RED = 0xFF0000
GREEN = 0x00ff00
BLUE = 0x0000ff
YELLOW = 0xffff00
FUCHSIA = 0xff00ff
AQUA = 0x00ffff
WHITE = 0xffffff
BLACK = 0x000000
ORANGE = 0xFF8C00

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

curr_board = 1

HIGH = 1
MEDIUM = 2
LOW = 3
prio = ["", "HIGH", "MEDIUM", "LOW"]
NAME = 0
TODO = 1
DOING = 2
DONE = 3
COLOUR = 4
THUMBNAIL = 5

BOARDS = [[], ["UNTITLED BOARD", {}, {}, {}, BLUE, "https://cdn.discordapp.com/avatars/458004758796697621/2240e45905dff5ca72290c0f2beb4a8d.png?size=1024"]]

EMBEDS = [None for i in range(1024)]



# testing command
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

### KANBAN COMMANDS
# displays current board
@bot.tree.command(name="kanban")
async def kanban(interaction: discord.Interaction):
    PRIO_MAPPING = {"HIGH": ":red_square: ", "MEDIUM": ":yellow_square: ", "LOW": ":green_square: "}

    embed = discord.Embed(title=f":scroll: {BOARDS[curr_board][NAME]}", colour=BOARDS[curr_board][COLOUR])
    embed.set_thumbnail(url=BOARDS[curr_board][THUMBNAIL])
    
    embed.add_field(name=":pushpin: __TODO__",
                    value = "\n".join([f"{PRIO_MAPPING[prio[BOARDS[curr_board][TODO][i][1]]]} {i}. {BOARDS[curr_board][TODO][i][0]}" for i in range(1, len(BOARDS[curr_board][TODO]) + 1)]),
                    inline=True)
    embed.add_field(name=":person_running: __DOING__",
                    value="\n".join([f"{PRIO_MAPPING[prio[BOARDS[curr_board][DOING][i][1]]]} {i}. {BOARDS[curr_board][DOING][i][0]}" for i in range(1, len(BOARDS[curr_board][DOING]) + 1)]),
                    inline=True)
    embed.add_field(name=":white_check_mark: __DONE__",
                    value = "\n".join([f"{PRIO_MAPPING[prio[BOARDS[curr_board][DONE][i][1]]]} {i}. {BOARDS[curr_board][DONE][i][0]}" for i in range(1, len(BOARDS[curr_board][DONE]) + 1)]),
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
    BOARDS[curr_board][TODO][len(BOARDS[curr_board][TODO])+1] = [task, priority.value]
    print(BOARDS[curr_board][TODO])
    await interaction.response.send_message(f":pencil: Added **{task}** with **{priority.name}** priority.")

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
    await interaction.response.send_message(f":arrow_right: Moved **{move_from.name}**, task **{task_number}** to **{move_to.name}**")

# clears "DONE" on current board
@bot.tree.command(name="kanbanclear")
async def kanbanclear(interaction: discord.Interaction):
    BOARDS[curr_board][DONE] = {}
    await interaction.response.send_message(f":broom: Cleared DONE list from {BOARDS[curr_board][0]}.")

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
    await interaction.response.send_message(f":wastebasket: Removed {name} from {BOARDS[curr_board][0]}.")

# lists all boards
@bot.tree.command(name="kanbanlistboards")
async def kanbanlistboard(interaction: discord.Interaction):
    embed = discord.Embed(title=":scroll: LIST OF BOARDS", colour=0xD2691E)
    for i in range(1, len(BOARDS)):
        embed.add_field(name=BOARDS[i][0],
                    value="Board Number/ID: " + str(i),
                    inline=False)
    await interaction.response.send_message(embed=embed)

# renames board
@app_commands.describe(new_name = "New name for board?")
@app_commands.describe(board_number = "Board number? Run /kanbanlistboard for board numbers.")
@bot.tree.command(name="kanbanrenameboard")
async def kanbanrenameboard(interaction: discord.Interaction, board_number: int, new_name: str):
    BOARDS[board_number][0] = new_name
    await interaction.response.send_message(f":pencil: Renamed kanban board #{board_number} titled {new_name}.")

# recolours board
@app_commands.describe(board_number = "Board number? Run /kanbanlistboard for board numbers.")
@app_commands.choices(colour = [
    app_commands.Choice(name="RED", value = 0xFF0000),
    app_commands.Choice(name="GREEN", value = 0x00ff00),
    app_commands.Choice(name="BLUE", value = 0x0000ff),  
    app_commands.Choice(name="YELLOW", value = 0xffff00),
    app_commands.Choice(name="FUCHSIA", value = 0xff00ff),
    app_commands.Choice(name="AQUA", value = 0x00ffff),
    app_commands.Choice(name="ORANGE", value = 0xff8c00),
    app_commands.Choice(name="WHITE", value = 0xffffff),
    app_commands.Choice(name="BLACK", value = 0x000000)
])
@bot.tree.command(name="kanbanrecolourboard")
async def kanbanrecolourboard(interaction: discord.Interaction, board_number: int, colour: app_commands.Choice[int]):
    BOARDS[board_number][COLOUR] = colour.value
    await interaction.response.send_message(f":art: Recoloured kanban board #{board_number} coloured {colour.name}.")

# adds new board
@app_commands.describe(name = "Name of new board?")
@app_commands.describe(colour = "Colour of new board?")
@app_commands.choices(colour = [
    app_commands.Choice(name="RED", value = 0xFF0000),
    app_commands.Choice(name="GREEN", value = 0x00ff00),
    app_commands.Choice(name="BLUE", value = 0x0000ff),  
    app_commands.Choice(name="YELLOW", value = 0xffff00),
    app_commands.Choice(name="ORANGE", value = 0xff8c00),
    app_commands.Choice(name="FUCHSIA", value = 0xff00ff),
    app_commands.Choice(name="AQUA", value = 0x00ffff),
    app_commands.Choice(name="WHITE", value = 0xffffff),
    app_commands.Choice(name="BLACK", value = 0x000000)
])
@bot.tree.command(name="kanbanaddboard")
async def kanbanaddboard(interaction: discord.Interaction, name: str, colour: app_commands.Choice[int]):
    user_id = interaction.user.id
    user_avatar = interaction.user.avatar
    BOARDS.append([name, {}, {}, {}, colour.value, user_avatar])
    print(interaction.user.id, interaction.user.avatar)
    await interaction.response.send_message(f":pencil: Added new kanban board titled {name}.")

# switches board
@app_commands.describe(number = "Number of board to switch to?")
@bot.tree.command(name="kanbanswitchboard")
async def kanbanswitchboard(interaction: discord.Interaction, number: int):
    set_curr_board(number)
    await interaction.response.send_message(f":arrow_right_hook: Moved to board #**{number}**, titled **{BOARDS[curr_board][0]}**")



### STREAKS 🔥
def get_streak():
    with open("streak.json", "r") as f:
        
        return json.load(f)

def write_streak():
    # js = {task: num+1}
    out = json.dumps(streaks, indent = 4)
    
    with open("streak.json", "w") as f:
        f.write(out)
        
def add_streak(task):
    streaks[task] += 1 
    write_streak()

streaks = get_streak()

def make_streak_board():
    streak_board = discord.Embed(colour=ORANGE)
    streak_board.set_author(name="STREAKS")
    for key in streaks.keys():
        streak_board.add_field(name=key.upper(),
                    value = streaks[key],
                    inline=False)
    # streak_board.set_thumbnail(url="https://cdn.discordapp.com/attachments/1236334285636505693/1236423368463618088/IMG_4296.jpg?ex=6637f47e&is=6636a2fe&hm=c40a7f52b3f3adb0ab7a9aaf7a37748aeaa2cf1b294f91c75d00fe0b748b9fe0&")
    
    return streak_board
### STREAK COMMANDS
@bot.tree.command(name="getstreaks")
async def getstreaks(interaction: discord.Interaction):

    await interaction.response.send_message(embed=make_streak_board())
        

## increments a streak of choice
@bot.tree.command(name="streak")
# @app_commands.describe(task = "what u wnat?!/1!?")
@app_commands.choices(options = [app_commands.Choice(name=choice, value = choice) for choice in [key for key in streaks.keys()]])
async def streak(interaction: discord.Interaction, options: str):
    add_streak(options)
    # await interaction.response.send_message(f"Streak: {streak}")
    await interaction.response.send_message(embed=make_streak_board())

@bot.tree.command(name="addnewstreak")
async def addnewstreak(interaction: discord.Interaction, task: str):
    streaks[task] = 0
    write_streak()
    await interaction.response.send_message(embed=make_streak_board())

@bot.tree.command(name="removestreak")
@app_commands.choices(options = [app_commands.Choice(name=choice, value = choice) for choice in [key for key in streaks.keys()]])
async def removestreak(interaction: discord.Interaction, options: str):
    del streaks[options]
    write_streak()
    await interaction.response.send_message(embed=make_streak_board())


@bot.tree.command(name="clearstreak")
@app_commands.choices(options = [app_commands.Choice(name=choice, value = choice) for choice in [key for key in streaks.keys()]])
async def clearstreak(interaction: discord.Interaction, options: str):
    streaks[options] = 0
    write_streak()
    await interaction.response.send_message(embed=make_streak_board())
    
    
    
    
### POMODORO COMMANDS
def clock_embed_make(time):
    embed = discord.Embed(colour=RED)
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

@bot.tree.command(name="pomodoro")
@app_commands.choices(unit = [
    app_commands.Choice(name="minutes", value = "minutes"),
    app_commands.Choice(name="seconds", value = "seconds")
])

async def pomodoro(interaction: discord.Interaction, time: int, unit: str):
    
    channel = interaction.user.voice.channel
    await channel.connect()

    if unit == "minutes":
        time *= 60
    # await interaction.response.send_message(embed=clock_embed_make(time))
    
    message = await interaction.response.send_message(f"Pomodoro countdown: {time} seconds")
       
    message = await interaction.original_response()
    
    while time > 0:
        await asyncio.sleep(0.9) 
        time -= 1
        if time > 60:
            
            await message.edit(content=f"Pomodoro countdown: {time//60} minutes\n{time%60} seconds")
        await message.edit(content=f"Pomodoro countdown: {time} seconds")
        
        # await interaction.response.send_message(embed=clock_embed_make(time))
    # await interaction.response.send_message(embed=clock_embed_make(time))
    await message.edit(content="Pomodoro countdown finished!")
    await asyncio.sleep(1)

    break_time = 5

    if unit == "minutes":
        break_time *= 60
    # await interaction.response.send_message(embed=clock_embed_make(break_time))
    
    message = await message.edit(content=f"Break countdown: {break_time} seconds")
       
    message = await interaction.original_response()
    
    while break_time > 0:
        await asyncio.sleep(0.9)  
        break_time -= 1
        if break_time > 60:
            
            await message.edit(content=f"Break countdown: {break_time//60} minutes\n{break_time%60} seconds")
        await message.edit(content=f"Break countdown: {break_time} seconds")
        
        # await interaction.response.send_message(embed=clock_embed_make(break_time))
    # await interaction.response.send_message(embed=clock_embed_make(break_time))
    await message.edit(content="Break countdown finished!")
    await asyncio.sleep(1)

    # pomodoro complete embed
    embed = discord.Embed(title="Alert",
                      description="Pomodoro Complete!\n\nPoints have been added.",
                      colour=0x00b0f4)
    embed.set_author(name="KanBoy")
    embed.set_thumbnail(url="https://kanboy-website.vercel.app/assets/kanban.png")
    embed.set_footer(text="Pomodoro Timer",
                    icon_url="https://kanboy-website.vercel.app/assets/kanban.png")
    
    

    await message.edit(embed=embed)


@bot.command()
async def leave(ctx):
    print(ctx)
    # Check if the bot is connected to a voice channel in the guild
    if ctx.voice_client:
        # Disconnect from the voice channel
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not connected to a voice channel.")
 
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
    await interaction.response.send_message(f":robot: :{response}")
    
    
    
    


### LEADERBOARD
def load_scores():
    with open("score.json", "r") as f:
        return json.load(f)
@bot.command()
async def get_id(ctx):
    user_id = ctx.author.id
    await ctx.send(user_id)

@bot.command()
async def get_points(ctx):
    user_id = ctx.author.id
    with open("score.json", "r") as f:
        points = json.load(f)
    await ctx.send(points[str(user_id)])

scores = load_scores()

lb = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))



@bot.tree.command(name="leaderboard")
async def leaderboard(ctx):
    embed = discord.Embed(title="LEADERBOARD", colour=FUCHSIA)
    for key in lb.keys():
        embed.add_field(name=ctx.guild.get_member(int(key)).display_name,
                    value = lb[key],
                    inline=False)
    await ctx.send(embed=embed)
    
    
def add_points_to_leaderboard(user, points):
    lb[user] += points;
    
def write_score():
    out = json.dumps(streak, indent = 4)
    
    with open("score.json", "w") as f:
        f.write(out)


bot.run(TOKEN)