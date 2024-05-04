import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json



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
    streak_board.set_author(name="BALLSACK'S STREAKS")
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

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def ching(ctx):
    await ctx.send("chong")

    
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

@bot.tree.command(name="kanbangetstreak")
async def kanbanstreak(interaction: discord.Interaction):

    await interaction.response.send_message(embed=make_streak_board())
        
    # streak = get_streak()
    # await interaction.response.send_message(f"Streak: {streak}")


@bot.tree.command(name="kanbanaddstreak")
# @app_commands.describe(task = "what u wnat?!/1!?")
@app_commands.choices(option = [
    app_commands.Choice(name="study", value = "study"),
    app_commands.Choice(name="workout", value = "workout"),
    app_commands.Choice(name="practice", value = "practice"),    
    app_commands.Choice(name="meditate", value = "meditate")
])
async def kanbanaddstreak(interaction: discord.Interaction, option: str):
    add_streak(option)
    # await interaction.response.send_message(f"Streak: {streak}")
    await interaction.response.send_message(embed=make_streak_board())

 
bot.run(TOKEN)