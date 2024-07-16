import discord
from discord.ext import tasks,commands
from core.classes import Cog_Extension
from datetime import datetime, timedelta
from Globle import NowTime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class cubeServer(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
      self.UpdateSheet.start()

    @commands.command(brief='Show Booking', description='Show Booking')
    async def Sbook(self,ctx):
      await ctx.channel.send(ShowAll())

    #@tasks.loop(seconds=2.0)
    async def UpdateSheetSimple(self):
      sheet = ConnetToSheet()
      cell = sheet.get_all_values()

      if str(cell[1][0]).find(NowTime().strftime("%m-%d")) < 0:
        print('123')
      print('finish')
      
    @tasks.loop(seconds=1800.0)
    async def UpdateSheet(self):
      sheet = ConnetToSheet()
      cell = sheet.get_all_values()
      #print(NowTime().strftime("%m-%d"))
      #print(len(cell))
      if str(cell[1][0]).find(NowTime().strftime("%m-%d")) < 0:
        cell.pop(1)
        while cell[1][0] == '':
          cell.pop(1)
        emptyField = 0
        for i in range(1,len(cell)):
          if cell[i][0] == '':
            emptyField += 1
        print(len(cell) - 1- emptyField)
        for i in range(len(cell) - 1 - emptyField,36):
          time = NowTime() + timedelta(hours=24 * i)
          weekday = SwicthToWeekDay(time.strftime("%A")[:3])
          #print(time.strftime("%m-%d") + weekday)
          cell.append([time.strftime("%m-%d") + weekday,'','','',''])
          
        sheet.batch_update([{'range': 'A2','values': cell[1:]}])
        #print(cell)
      print('finish')

    @commands.command(brief='!book [date] [StartTime] [EndTime] [remark] [請勿打擾]', description='!book [date] [StartTime] [EndTime] [remark] [請勿打擾]') 
    async def book(self,ctx, date,STime,ETime,*arg):
      if int(STime) > 2400 or int(ETime) >2400:
        await ctx.channel.send('你輸入的時間有誤')
        return
        
      findDate = False
      date = date[:2] + '-' + date[2:]
      sheet = ConnetToSheet()
      cell = sheet.get_all_values()

      for index,i in enumerate(cell):
        if i[0].find(date) >= 0:
          findDate = True
          dontCome = '請勿打擾'
          remark = ''
          remark = arg[0] if len(arg) >= 1 else ''
          if len(arg) >= 2:
            dontCome = arg[1]
            
          if i[1] == '':  #檢查當天時間是否為空值
            i[1:] = (str(STime),str(ETime),remark,dontCome)
            #print(cell)
            sheet.batch_update([{'range': 'A2','values': cell[1:]}])
            await ctx.channel.send(f'已幫你預約{date}  {STime}至{ETime+"|"+ remark +"|" + dontCome} |0 w0+' )
          elif is_time_overlap(i[1],i[2],STime,ETime) == False:
            print(cell)
            cell.insert(index + 1,['',str(STime),str(ETime),remark,dontCome])
            print(cell)
            sheet.batch_update([{'range': 'A2','values': cell[1:]}])
            await ctx.channel.send(f'已幫你預約{date}  {STime}至{ETime+"|"+ remark +"|" + dontCome} |0 w0+' )
          else:
            await ctx.channel.send('someone has been booked')
          break
          
      if not findDate:
        await ctx.channel.send('超出預定日子(30天內)')
    
      await ctx.channel.send(ShowAll())
      
    @commands.command(brief='!bookingClear [date] [Stime]', description='!bookingClear [date] [Stime]') 
    async def bookingClear(self,ctx,date,Stime):
      print('so')
      sheet = ConnetToSheet()
      date = date[:2] + '-' + date[2:]
      if date == '':
        return
      findDate = False
      cell = sheet.get_all_values()
      cell.append(['','','','',''])
      for index,i in enumerate(cell):
        if i[0].find(date) >= 0:
          findDate = True
          findTime = False
          timeIndex = 0
          while not findTime:
            if cell[index + timeIndex][1] == Stime:
              print('findtime')
              if cell[index + timeIndex][0] != '':
                cell[index + timeIndex][1] = cell[index + timeIndex][2] = cell[index + timeIndex][3] = ''
                if cell[index + timeIndex + 1][0] == '' and cell[index + timeIndex + 1][1] != '':
                  cell[index + timeIndex][1] = cell[index + timeIndex + 1][1]
                  cell[index + timeIndex][2] = cell[index + timeIndex + 1][2]
                  cell[index + timeIndex][3] = cell[index + timeIndex + 1][3]
                  cell.pop(index + timeIndex + 1)
                print('reCover row')
              else:
                cell.pop(index + timeIndex)
                print('remove row')
              findTime = True
              
            elif cell[index + timeIndex + 1][0] == '' and cell[index + timeIndex + 1][1] != '':
              timeIndex += 1
            else:
              break
          #print(cell)
          if findTime:
            sheet.batch_update([{'range': 'A2','values': cell[1:]}])
            await ctx.channel.send(f'已幫你清除{date}的預約 0 w0b')
          else:
            await ctx.channel.send('找不到對應時間')
      if not findDate:
        await ctx.channel.send('找不到日期')
      await ctx.channel.send(ShowAll())


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

def ShowAll():
  msg = "```"
  sheet = ConnetToSheet()
  list = sheet.get_all_values()
  for index,i in enumerate(list[1:]):
    if i[1] != '':
      msg += f"{i[0] if i[0] != '' else '     　　　'} {i[1]}-{i[2]} {i[3]} {i[4]} \n"
  msg += "```"
  return(msg)

def is_time_overlap(start_time1, end_time1, start_time2, end_time2):
  if start_time1 >= end_time2 or start_time2 >= end_time1:
      return False
  return True
  
async def setup(bot):
    await bot.add_cog(cubeServer(bot))