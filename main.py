import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

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

bot.run(TOKEN)