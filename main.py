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
        return json.load(f)["streak"]

def write_streak(n):
    js = {"streak": n}
    out = json.dunps(js, indent = 4)
    
    with open("streak.json", "w") as f:
        f.write(out)

streak = 0


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
    streak = get_streak()
    await interaction.response.send_message(f"Streak:{streak}")

@bot.tree.command(name="kanbanaddstreak")
async def kanbanaddstreak(interaction: discord.Interaction):
    streak = get_streak()
    streak += 1
    write_streak(streak)
    await interaction.response.send_message(f"Streak:{streak}")

bot.run(TOKEN)