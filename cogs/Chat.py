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
                  max_output_tokens=1000,
                  temperature=0.3,
                ))
                # response = self.conversation.generate_content(
                #     generation_config=genai.GenerationConfig(
                #         max_output_tokens=3000,
                #         temperature=0.3,
                #     )
                # )
                await ctx.channel.send(response.text)
        except Exception as e:
            await ctx.channel.send("An error occurred during the request")
            print("Something went wrong")
            print(e)

    @commands.command()
    @commands.is_owner()
    async def reset_chat(self, ctx):
        self.conversation = None
        self.designated_channel_id = None # 重置 designated_channel_id
        await ctx.send("現在頻道聊天記錄已重置。")

async def setup(bot):
    await bot.add_cog(Chat(bot))