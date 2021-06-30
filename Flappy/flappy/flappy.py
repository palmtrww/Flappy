import discord
import colorama
import sqlite3
import os
import random
from glob import glob
from sqlite3 import connect
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Flappy import __mainguild__
from Flappy import __mainchannel__
from Flappy import __version__
from discord.ext import commands
from ..db import db
from colorama import Fore, Style
from pytz import utc

# Grabing the custom prefix from each guild
def cus_pre(bot, message):
    # Selects the prefix from the db table and its from a certant guild
    prefix = db.field("SELECT Prefix FROM Guilds WHERE GuildID = ?", message.guild.id)
    # The prefix can now be used like: @Bot help or {prefix}help
    return commands.when_mentioned_or(prefix)(bot, message)

class Flappy(commands.Bot):
    def __init__(self):
        # Setting a scheduler for autosaving the database every minute and setting time of it to utc time
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        self.ready = False
        # Activity variable for super().__init__
        self._acticity = discord.Activity(type=discord.ActivityType.listening, name="@BattleTime help")
        
        db.autosave(self.scheduler)
        
        
        super().__init__(
            command_prefix=cus_pre, 
            case_sensitive=True,
            intents=discord.Intents.all(), 
            activity = discord.Activity(
                status = discord.Status.dnd,
                name=f"{self._acticity} - {__version__}"
            ),
        )
        
    def setup(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Running Setup")
        # Checks for every cog with the file extension as py and loading it so all the commands can be used!
        for exts in os.listdir("./Flappy/flappy/extensions"):
            if exts.endswith(".py"):
                self.load_extension(f"Flappy.flappy.extensions.{exts[:-3]}")
                print(Fore.GREEN + Style.BRIGHT + f"[EXT NOTIFICATION] Loaded {exts[-3]}")
            else:
                print(Fore.RED + Style.BRIGHT + f"[EXT NOTIFICATION] Couldn't load {exts[-3]}")
                
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Finished Setup")
    
 
                
    def run(self):
        self.setup()
        
        # Loading the bot token from a folder in the /data directory
        with open("./data/secrets/flappytoken.txt", mode="r", encoding="utf-8") as tf:
            self.token = tf.read()
            
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Running Bot!")
        # Runs the bot
        super().run(self.token, reconnect=True)
        
    async def on_connect(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"Bot has connected to discord servers, Latency: {round(self.latency * 1000)}ms")
        
        
    async def on_disconnect(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Bot has disconnected from discord servers")
        
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            
            # Starts the scheduler autosaving the database
            self.scheduler.start()
            
            #Explined in the parent __init__.py
            mc = self.get_channel(__mainchannel__)
            await mc.send(f"Now Online {random.randint(1, 10000000000000000000)}")
            
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Bot is ready for usage")
            
        else:
            # If the bot was already online but the servers got switched it will print this
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Bot has reconnected")