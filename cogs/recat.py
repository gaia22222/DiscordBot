
import discord
from discord.ext import commands
from core.classes import Cog_Extension

class React(Cog_Extension):
    @commands.command
    async def on_ready(self):
        print('目前登入身份s：', self.bot.user)
    
async def setup(bot):
    await bot.add_cog(React(bot))