from tkinter import EventType
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import string
import random

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self,msg):
        if(msg.author == self.bot.user):
            return
        if(msg.content[0] == '!'):
            return
        if(random.randrange(0,5000) < 20):
            await msg.channel.send(file = discord.File('./img/LuckyCat.png'))
        # if('好' in msg.content):
        #     await msg.channel.send(msg.content.replace("好", "都唔",1))

        # if('a' in msg.content):
        #     await msg.channel.send('have a')
        # if('b' in msg.content):
        #     await msg.channel.send('have b')
        # if('c' in msg.content):
        #     await msg.channel.send('have c')

async def setup(bot):
    await bot.add_cog(Event(bot))