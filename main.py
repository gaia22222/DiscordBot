import keep_alive
import os
import discord
from discord.ext import commands
#from Globle import NowTime
import asyncio
from Globle import NowTime
from datetime import datetime, timedelta

intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='!',owner_id = 334553910520053762, intents=intents)

@bot.event
async def on_ready():
    print('目前登入身份：', bot.user,flush=True)
    print('time.now = ', NowTime())
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game('維修中0u0'))


# @bot.event
# async def on_member_join(member):
#     print(F'{member} join!')


# @bot.command()
# async def load(ctx, extension):
#     await bot.load_extension(f"cogs.{extension}")
#     await ctx.send(f"Loaded {extension} done.")


# # 卸載指令檔案
# @bot.command()
# async def unload(ctx, extension):
#     await bot.unload_extension(f"cogs.{extension}")
#     await ctx.send(f"UnLoaded {extension} done.")


# # 重新載入程式檔案
# @bot.command()
# async def reload(ctx, extension):
#     await bot.reload_extension(f"cogs.{extension}")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(filename)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.environ.get('TOKEN'))


# 確定執行此py檔才會執行
if __name__ == "__main__":
    keep_alive.keep_alive()
    asyncio.run(main())