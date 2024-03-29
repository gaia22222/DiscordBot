from tkinter import EventType
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import string
import random
import typing
import os

class Chat(Cog_Extension):
  '''
  @commands.Cog.listener()
  async def on_message(self,msg):
    if(msg.author == self.bot.user):
      return

    if not((msg.channel.id != 1079770157414625370) ^ (msg.channel.id != 540973843775488012)):
      return
    #ori
    #if (msg.channel.id != 1079770157414625370):
      #return
    #本bot
    #if (msg.channel.id != 540973843775488012):
      #return
    if(msg.content[0] == '!'):
      return
    config = {
      "session_token": os.getenv('Chat_Token')
    }
    chatbot = Chatbot(config,conversation_id=None)
    try:
        async with msg.channel.typing():
            prompt = msg.content
            for data in chatbot.ask(prompt):
              response = data["message"]
            await msg.channel.send(response)
            
    except Exception as e:
        await msg.channel.send("An error occurred during the request")
        print("Something went wrong")
        print(e)
      
  @commands.command()
  async def ask(ctx, *arg):
    config = {
      "session_token": os.getenv('Chat_Token')
    }
    chatbot = Chatbot(config,conversation_id=None)
    try:
        async with ctx.typing():
            prompt = ctx.message.content
            for data in chatbot.ask(prompt):
              response = data["message"]
              
            await ctx.send(response)
            
    except Exception as e:
        await ctx.send("An error occurred during the request")
        print("Something went wrong")
        print(e)
        '''

async def setup(bot):
    await bot.add_cog(Chat(bot))