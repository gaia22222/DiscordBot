import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time
import asyncio
from datetime import datetime, timedelta
from Globle import NowTime
import json
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# with open('setting.json', 'r',encoding='utf8') as jfile:
#     jdata = json.load(jfile)

class Mains(Cog_Extension):
    
    @commands.command()
    @commands.is_owner()
    async def exit(self,ctx):
        await ctx.send('下線中...')
        await self.bot.close()

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'你老母依加延遲 {round(self.bot.latency*1000,2)} ms呀')
    @commands.command()
    async def sleep(self,ctx):
        print(NowTime())
        username = str(ctx.author).split('#')[0]
        #晚上9點小於現在時間 and 明早9點大於現在時間
        if not(NowTime() > GetToday21_Oclock() or NowTime() < GetToday9_Oclock()):
            print(NowTime() > GetToday21_Oclock() , NowTime() < GetToday9_Oclock())
            print(GetToday21_Oclock() ,NowTime())
            await ctx.send(f'超出工作時間囉~ {username} 我現在要休息囉!')
            return
        
        timeNow = NowTime().strftime('%Y/%m/%d %H:%M:%S')
        if not(f'{ctx.author}' in jdata):
            jdata[f'{ctx.author}'] = [timeNow]
            SaveJson()
            await ctx.send(f'恭喜 {username} 成為新的乖寶寶!')
        else:
            RemoveTimeOutOfDate(jdata[f'{ctx.author}'])
            RemoveRepeatTimeInSameDay(jdata[f'{ctx.author}'])
            jdata[f'{ctx.author}'].append(timeNow)
            await ctx.send(f'{CheckMeetTarget()}')
            SaveJson()
        
        await ctx.send(f'乖寶寶  {username}  在 {timeNow[:-3]} 睡覺啦!!')
    @commands.command()
    async def c(self,ctx):
        #print(GetTargetTime())
        #asyncio.sleep(5)
        return
        await ctx.send(f'{CheckMeetTarget()}')

    @commands.command()
    async def clear(self,ctx,count : int):
        await ctx.channel.purge(limit = count +1)
        tmpmsg = await ctx.channel.send(f'已經幫你把 {count} 句垃圾清掉了0 w0b')
        await asyncio.sleep(2)
        await tmpmsg.delete()
    @commands.command()
    async def say(self,ctx):
        # if not(ctx.author == ctx.guild.owner):
        #     return
        content = ctx.message.content
        await ctx.channel.purge(limit = 1)
        await ctx.channel.send(content.replace('!say',''))
    @commands.command()
    async def ssay(self,ctx):
        # if not(ctx.author == ctx.guild.owner):
        #     return
        content = ctx.message.content
        await ctx.channel.purge(limit = 1)
        temp = await ctx.channel.send(content.replace('!ssay',''))
        await asyncio.sleep(10)
        await temp.delete()
    @commands.command()
    async def print(self,ctx):
      print(ctx.message.content)
    @commands.command()
    async def rp(self, ctx, *arg):
        with open('princessKey.json', 'r',encoding='utf8') as princessfile:
            princessData = json.load(princessfile)
        print(princessData[f'{random.randint(0,len(princessData))}'])
        await ctx.channel.send(file=discord.File('./img/PrincessIcon/'+princessData[f'{random.randint(0,len(princessData))}']))
    @commands.command()
    async def expend(self,ctx, *arg):
      if len(arg) < 3:
        return
      lastMsg = [message async for message in ctx.channel.history(limit=2)][1].content
      await ctx.channel.send(Expend(arg[0],arg[1],arg[2],lastMsg))
    
    #@tasks.loop(hours=24)
    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        print("shutdown")
        exit()

# def SaveJson():
#     with open('setting.json', 'w') as jfile:
#         json.dump(jdata, jfile)

def RemoveTimeOutOfDate(timeList):
    for time in timeList:
        tempTime = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
        if((NowTime() - tempTime).days > 7):
            timeList.remove(time)
    print(timeList)

def RemoveRepeatTimeInSameDay(timeList):
    for time in timeList:
        tempTime = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
        if(tempTime > GetToday21_Oclock() or tempTime > GetYesterday9_Oclock()):
            timeList.remove(time)

def GetYesterday9_Oclock():
    today = (NowTime()+ timedelta(days=-1)).strftime('%Y/%m/%d ') + '21:00:00'
    return datetime.strptime(today, '%Y/%m/%d %H:%M:%S')

def GetToday9_Oclock():
    today = NowTime().strftime('%Y/%m/%d ') + '09:00:00'
    return datetime.strptime(today, '%Y/%m/%d %H:%M:%S')

def GetToday21_Oclock():
    today = NowTime().strftime('%Y/%m/%d ') + '21:00:00'
    return datetime.strptime(today, '%Y/%m/%d %H:%M:%S')

def GetTargetTime():
    if(NowTime() > datetime.strptime(NowTime().strftime('%Y/%m/%d ') + '21:00:00', '%Y/%m/%d %H:%M:%S')):
        return (NowTime()+ timedelta(days=1)).strftime('%Y/%m/%d ') + jdata['targetTime']
    else:
        return NowTime().strftime('%Y/%m/%d ') + jdata['targetTime']

def CheckMeetTarget():
    print('sss')
    if(NowTime() < datetime.strptime(GetTargetTime(), '%Y/%m/%d %H:%M:%S')):
        #early
        timer = datetime.strptime(GetTargetTime(), '%Y/%m/%d %H:%M:%S') - NowTime()
        early = True
    else:
        #late
        timer = NowTime() - datetime.strptime(GetTargetTime(), '%Y/%m/%d %H:%M:%S')
        early = False
    print(early)

    if(early):
        return f'很棒呢,比預料目{GetTargetTime()}標早了 {round(timer.seconds/60)} 分鐘睡呢'
    else:
        return f'唉,比預料目標{GetTargetTime()}晚了 {round(timer.seconds/60)} 分鐘睡呢'

def NowTime():
    return datetime.now() + timedelta(hours=8)

def Expend(name,item,cost,lastMsg):
  if len(lastMsg.split('-=-')) > 1:
    lastMsg = lastMsg.split('-=-')[0]
  else:
    lastMsg = f'{name}| \n {item}| {0}|'
  print(len(lastMsg.split('-=-')))
  formatStr = 10
  clearMsg = lastMsg.replace(' ','')
  clearMsg = lastMsg.replace('`','')
  list = clearMsg.split('\n')
  table = []
  itemlist = []

  seclectName = -1
  seclectItem = -1
  print(clearMsg)
  for i in list:
    tempList = i.replace(' ','').split('|')
    if tempList[-1] == '':
      tempList.remove('')
    if len(tempList) != 0:
      table.append(tempList)
  print(table)
  
  if name in table[0]:
    print('can find Name')
    seclectName = table[0].index(name) + 1
  else:
    table[0].append(name)
    seclectName = len(table[0])
    for i in table[1:]:
        i.append(0)
  
  for i in table:
    itemlist.append(i[0])
  if item in itemlist:
    print('can find item')
    seclectItem = itemlist.index(item)
  else:
    itemlist.append(item)
    table.append([item])
    seclectItem = len(itemlist) - 1
    table[-1].extend([0]*(len(table[0])))

  print(seclectItem,seclectName)
  if seclectName >= 0 or seclectItem >= 0:
    tempCost =  round(float(eval(cost)), 2)
    table[seclectItem][seclectName] = float(table[seclectItem][seclectName]) + tempCost

  returnMsg = '``` ' + f"{'':>{formatStr}s}"
  for i in range(len(table)):
    for j in table[i]:
      returnMsg += f'{str(j):>{formatStr}s}|'
    returnMsg += '\n'
  returnMsg += '-=-' * int(((len(table[0]) + 1) * formatStr + len(table[0])) /3) + '\n '
  returnMsg += f"{'':>{formatStr}s}"
  totalCost = 0
  for i in range(len(table[0])):
    totalCost = 0
    for j in table[1:]:
      totalCost += float(j[i + 1])
    returnMsg += f'{str(totalCost):>{formatStr}s}|'
  
  
  returnMsg = returnMsg + '```'
  print(table)
  print(returnMsg)
  return returnMsg

def ConnetToSheet():
  scopes = ["https://spreadsheets.google.com/feeds"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
  client = gspread.authorize(credentials)
  sheets = client.open_by_key("12qOorzFHB_utm8YD6cPlJJ9xFTysAhm76uoCZtodv7s")
  sheet = sheets.worksheet("DCBuckup")
  return sheet

def SwicthToWeekDay(weekday):
  if weekday == 'Mon':
    return '星期一'
  elif weekday == 'Tue':
    return '星期二'
  elif weekday == 'Wed':
    return '星期三'
  elif weekday == 'Thu':
    return '星期四'
  elif weekday == 'Fri':
    return '星期五'
  elif weekday == 'Sat':
    return '星期六'
  elif weekday == 'Sun':
    return '星期日'
  else :
    return '0'
    
async def setup(bot):
    await bot.add_cog(Mains(bot))