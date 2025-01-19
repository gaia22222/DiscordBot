import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import google.generativeai as genai


class Chat(Cog_Extension):
  
    def __init__(self, bot):
        super().__init__(bot)
        genai.configure(api_key=os.environ.get('GeminiAI'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.conversation = self.model.start_chat()
        self.designated_channel_id = None
        self.chat__temperature = 0.3

    #@commands.hybrid_command(brief='/ask', description='Ask to AI')
    @commands.command()
    async def ask(self, ctx, *, message):
        if self.designated_channel_id != ctx.channel.id:
            old_channel = self.bot.get_channel(self.designated_channel_id)  # 获取之前的频道
            if old_channel: # 檢查舊頻道是否存在 (可能已被刪除)
                await old_channel.send(f'聊天機器人可能已在其他頻道啟動，現在的記憶記錄已清除。')

            self.designated_channel_id = ctx.channel.id
            self.conversation = self.model.start_chat()
            await ctx.send('正在此頻道啟動新的對話，之前的記憶記錄已清除。')
        try:
            async with ctx.channel.typing():
                response = self.conversation.send_message(message,
                  generation_config = genai.GenerationConfig(
                  max_output_tokens = 1000,
                  temperature = self.chat__temperature,
                ))
                # response = self.conversation.generate_content(
                #     generation_config=genai.GenerationConfig(
                #         max_output_tokens=3000,
                #         temperature=0.3,
                #     )
                # )
                await self.send_long_message(ctx, response.text)
        except Exception as e:
            await ctx.channel.send("An error occurred during the request")
            print("Something went wrong")
            await ctx.send(e)

    async def send_long_message(self, ctx, message):
        if len(message) <= 1000:
            await ctx.send(message)
        else:
            for i in range(0, len(message), 1000):
                await ctx.send(message[i:i+1000])

    @commands.command()
    @commands.is_owner()
    async def reset_chat(self, ctx):
        self.conversation = None
        self.designated_channel_id = None # 重置 designated_channel_id
        await ctx.send("現在頻道聊天記錄已重置。")

    @commands.command()
    @commands.is_owner()
    async def setchatT(self, ctx, *, temperature):
        try:
            temperature = float(temperature)
            if 0 <= temperature <= 1:
                self.chat_temperature = temperature
                await ctx.send(f"更新 Chat - Temperature 為 {temperature}")
            else:
                await ctx.send("Temperature 必須在 0 和 1 之間")
        except ValueError:
            await ctx.send("請提供一個有效的數字")
        


async def setup(bot):
    await bot.add_cog(Chat(bot))