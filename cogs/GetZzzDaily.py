import discord
from discord.ext import commands, tasks
import tweepy
import os
import asyncio
import re 
from core.classes import Cog_Extension 

TARGET_CHANNEL_ID = 1384623990781378720
ZZZ_X_USERNAME = "ZZZ_CHT" 
X_BEARER_TOKEN = os.environ.get('twitterApi') # <<== 修改这里

FETCH_INTERVAL_MINUTES = 16.0 # 每隔多久检查一次新的贴文 (分钟)
TWEETS_FETCH_LIMIT_PER_CALL = 5 # 每次调用 X API 获取的最近贴文数量 (最多100)
DISCORD_HISTORY_LOOKUP_LIMIT = 30 # 启动时读取 Discord 频道最近多少条消息来判断已发送贴文

POST_ID_PATTERN = re.compile(r'\(ID:\s*`(\d+)`\)')


class GetZzzDaily(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.target_channel_id = TARGET_CHANNEL_ID
        self.zzz_x_username = ZZZ_X_USERNAME
        self.x_bearer_token = X_BEARER_TOKEN

        self.sent_post_ids_in_memory = set() 

        # Tweepy Client 实例
        self.x_client = None
        self.zzz_user_id = None # 存储绝区零用户的ID，避免每次查找

    async def _load_sent_post_ids_from_discord_history(self):
        """从 Discord 频道历史中加载已发送的贴文 ID"""
        print(f"正在从 Discord 频道 {self.target_channel_id} 读取最近 {DISCORD_HISTORY_LOOKUP_LIMIT} 条消息...")
        channel = self.bot.get_channel(self.target_channel_id)
        if channel is None:
            print(f"!! 错误：未找到配置的频道 ID {self.target_channel_id}。无法加载历史记录。")
            return

        loaded_count = 0
        try:
            # history() 方法返回消息是按时间倒序 (最新的在前)
            async for message in channel.history(limit=DISCORD_HISTORY_LOOKUP_LIMIT):
                # 检查消息是否由机器人自己发送，并且包含特定的 ID 格式
                if message.author == self.bot.user:
                    match = POST_ID_PATTERN.search(message.content)
                    if match:
                        post_id = match.group(1) # 提取括号中的 ID
                        self.sent_post_ids_in_memory.add(post_id)
                        loaded_count += 1

            print(f"成功从 Discord 历史中加载 {loaded_count} 个已发送贴文 ID 到内存。")

        except discord.errors.NotFound:
            print(f"!! 错误：无法找到频道 ID {self.target_channel_id}。")
        except discord.errors.Forbidden:
            print(f"!! 错误：机器人没有读取频道 {self.target_channel_id} 历史的权限。")
        except Exception as e:
            print(f"!! 错误：加载 Discord 历史时发生未知错误: {e}")


    @commands.Cog.listener()
    async def on_ready(self):
        # 初始化 Tweepy Client 和获取用户ID
        if not self.x_bearer_token:
             print("!! 错误：X_BEARER_TOKEN 未配置。请在代码中或环境变量中设置你的 Bearer Token。")
             return
        try:
            self.x_client = tweepy.Client(self.x_bearer_token, wait_on_rate_limit=True)
            # 获取用户的ID，只需要做一次
            print(f"正在查找 X 用户 @{self.zzz_x_username} 的 ID...")
            # user_response = self.x_client.get_user(username=self.zzz_x_username) # 旧版 get_user
            user_response = self.x_client.get_user(username=self.zzz_x_username) # 新版 get_user 需要指定字段，但默认也行
            if user_response.data:
                self.zzz_user_id = user_response.data.id
                print(f"找到用户 @{self.zzz_x_username} 的 ID: {self.zzz_user_id}")
            else:
                print(f"!! 错误：未能找到用户 @{self.zzz_x_username}。请检查用户名是否正确。")
                self.x_client = None # 无法获取用户ID，禁用客户端
                return

        except tweepy.TweepyException as e:
            print(f"!! 错误：初始化 Tweepy 或获取用户ID失败: {e}")
            self.x_client = None # 初始化失败，禁用客户端
            return
        except Exception as e:
            print(f"!! 发生未知错误在初始化阶段: {e}")
            self.x_client = None
            return

        # --- 梦境核心：从 Discord 历史中重建已发送记录 ---
        await self._load_sent_post_ids_from_discord_history()

        # 启动定时任务
        self.fetch_zzz_posts_task.start()
        print(f"绝区零贴文获取任务已启动，每 {FETCH_INTERVAL_MINUTES} 分钟检查一次！")

    @tasks.loop(minutes=FETCH_INTERVAL_MINUTES)
    async def fetch_zzz_posts_task(self):
        if self.x_client is None or self.zzz_user_id is None:
            # print("Tweepy 客户端或用户 ID 未准备好，跳过任务。") # 频繁打印可能刷屏，按需开启
            return

        # print("正在执行绝区零贴文获取任务...") # 频繁打印可能刷屏，按需开启
        channel = self.bot.get_channel(self.target_channel_id)
        if channel is None:
            print(f"错误：未找到配置的频道 ID {self.target_channel_id}。请检查频道 ID 是否正确且机器人，或者机器人没有访问该频道的权限。")
            # 如果频道不存在，直接返回，等待下次循环
            return

        try:
            # --- 梦境投射：使用 Tweepy 从 X.com 获取数据 ---
            response = self.x_client.get_users_tweets(
                id=self.zzz_user_id,
                max_results=min(TWEETS_FETCH_LIMIT_PER_CALL, 100), # max_results 最大是 100
                tweet_fields=["created_at", "text", "attachments", "entities"],
                expansions=["attachments.media_keys"],
                media_fields=["url", "type", "preview_image_url"], # 添加 preview_image_url
                exclude=['retweets', 'replies'] # 通常我们只关心原贴文
            )
            print(f'正在获取绝区零贴文。') # 调试用
            latest_posts = []
            if response.data:
                media_dict = {}
                if response.includes and 'media' in response.includes:
                     media_dict = {media.media_key: media for media in response.includes['media']}

                for tweet in response.data:
                    post_id = str(tweet.id)
                    post_text = tweet.text

                    image_urls = []
                    if tweet.attachments and 'media_keys' in tweet.attachments:
                        for media_key in tweet.attachments['media_keys']:
                            if media_key in media_dict:
                                media = media_dict[media_key]
                                if media.type in ('photo', 'animated_gif'):
                                     if hasattr(media, 'url') and media.url:
                                         image_urls.append(media.url)
                                elif media.type == 'video':
                                     if hasattr(media, 'url') and media.url:
                                          # 如果有直接视频链接，优先使用
                                          image_urls.append(media.url)
                                     elif hasattr(media, 'preview_image_url') and media.preview_image_url:
                                         # 如果没有，使用预览图并标记
                                         image_urls.append(media.preview_image_url + " (视频预览)")
                                     # else: print(f"视频媒体 {media_key} 没有 url 或 preview_image_url") # 调试用


                    latest_posts.append({
                        'id': post_id,
                        'text': post_text,
                        'image_urls': image_urls # 包含图片/视频预览 URL
                    })

            # 如果没有获取到贴文，直接返回
            if not latest_posts:
                # print("未获取到任何贴文数据。") # 频繁打印可能刷屏，按需开启
                return

            # API 返回的已经是按时间倒序的，最新的在前面，反转列表以便按时间顺序处理（旧->新）
            latest_posts.reverse()
            # print(f"获取到 {len(latest_posts)} 条贴文，准备检查和发送。") # 调试用

            new_posts_sent_count = 0
            for post in latest_posts:
                post_id = post['id']
                post_text = post['text']
                image_urls = post['image_urls']

                # 检查这个贴文 ID 是否已经发送过 (在内存中的 set 里查找)
                # 这里的 set() 是通过读取 Discord 历史加载 + 当前运行期间发送的新 ID 构建的
                if post_id in self.sent_post_ids_in_memory:
                    # print(f"贴文 ID {post_id} 已发送过，跳过。") # 频繁打印可能刷屏，按需开启
                    continue # 已经处理过，跳过

                # --- 梦境投射：将新贴文发送到 Discord ---
                # 消息内容中包含 ID，以便下次启动时可以从 Discord 历史中识别
                message_content = f"**绝区零新贴文 (ID: `{post_id}`)**\n\n{post_text}"

                # 考虑文字内容可能很长，Discord 有字数限制 (2000字符)
                if len(message_content) > 2000:
                     message_content = message_content[:1997] + "..." # 截断并添加省略号

                try:
                    # 发送文字内容
                    print(f"正在发送新贴文 (ID: {post_id})...")
                    await channel.send(message_content)
                    await asyncio.sleep(1) # 短暂等待，避免发送过快或触发 Discord 速率限制

                    # 发送图片/视频链接
                    for media_url in image_urls:
                        try:
                            # Discord 可以直接嵌入图片/视频 URL
                            await channel.send(media_url)
                            await asyncio.sleep(1) # 短暂等待
                        except Exception as media_e:
                            print(f"!! 发送媒体 {media_url} 失败: {media_e}")
                            # 媒体发送失败不中断整个流程

                    # 添加到已发送 set (内存)
                    # 这是为了在当前运行期间避免重复发送，不是为了持久化
                    self.sent_post_ids_in_memory.add(post_id)

                    new_posts_sent_count += 1
                    print(f"成功发送新贴文 (ID: {post_id}) 到频道。")

                except Exception as send_e:
                    print(f"!! 发送贴文 ID {post_id} 到 Discord 失败: {send_e}")
                    # 发送失败不中断整个任务循环，继续尝试下一个贴文

            if new_posts_sent_count > 0:
                 print(f"本次任务共发送 {new_posts_sent_count} 条新贴文。")
            # else:
                 # print("本次任务没有发现新的未发送贴文。") # 频繁打印可能刷屏，按需开启


        except tweepy.TweepyException as e:
            print(f"!! Tweepy API 调用失败: {e}")
            # 通常 API 错误不应中断循环，让它下次重试。
            pass
        except Exception as e:
            print(f"!! 获取或处理绝区零贴文时发生未知错误: {e}")
            # 未知错误，也让任务继续运行，下次重试
            pass


async def setup(bot):
    """将 Cog 添加到机器人"""
    await bot.add_cog(GetZzzDaily(bot))