import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import time
from Globle import NowTime  
from datetime import datetime, timedelta
from discord.ext import tasks, commands
with open('onlineRecord.json', 'r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
class KCmonitor(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(NowTime())
        self.GetKCStatus.start()
        self.RemoveTimeOutOfDate.start()
        #self.Test.start()
        # for guild in self.bot.guilds:
        #     for member in guild.members:
        #         print(member)
        #         print(member.status)
        #     print('-'*15)
    @tasks.loop(seconds=3.0)
    async def Test(self):
        getGuild = self.bot.get_guild(540935479894474753)
        sendChannel = self.bot.get_channel(976702879266144256)
        print((await sendChannel.history(limit=2).flatten())[0].content.split(' ')[0])
        print(str(NowTime())[:10])
        print((await sendChannel.history(limit=2).flatten())[0].content.split(' ')[0]==str(NowTime())[:10])

    @tasks.loop(seconds=30.0)
    async def GetKCStatus(self):
        getGuild = self.bot.get_guild(540935479894474753)
        sendChannel = self.bot.get_channel(976702879266144256)
        '''lastMsg = [message async for message in sendChannel.history(limit=1)]
        contents = []
        for message in lastMsg:
          contents.append(message.content)
        '''
        print('-' * 66)
        
        lastMsg = [message async for message in sendChannel.history(limit=1)][0].content
        
        for member in getGuild.members:
            if str(member.id) == '350328767119360001' and lastMsg.split(' ')[2] != str(member.status.value):
                if lastMsg.split(' ')[0] != str(NowTime())[:10]:
                  await sendChannel.send('-' * 66)
                #jdata['Record']['last Status'] = member.status.value
                #jdata['Record']['Status Change Record'].append([f'{member.status.value}',str(NowTime())[:-10]])
                sleep = ''
                if str(member.status.value) == 'offline':
                  sleep = 'Sleep'
                await sendChannel.send(str(NowTime())[:-10]+' '+member.status.value+ ' '+ sleep)
                

    @tasks.loop(hours=24)
    async def RemoveTimeOutOfDate(self):
        for time in jdata['Record']['Status Change Record']:
            tempTime = datetime.strptime(time[1], '%Y-%m-%d %H:%M')
            if((NowTime() - tempTime).seconds > 1):
                jdata['Record']['Status Change Record'].remove(time)
        SaveJson()

def SaveJson():
    with open('onlineRecord.json', 'w') as jfile:
        json.dump(jdata, jfile)

async def setup(bot):
    await bot.add_cog(KCmonitor(bot))