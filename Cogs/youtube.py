# Discord bot import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.youtube_add import Add
from Cogs.CommandPrograms.youtube_delete import Delete
from Cogs.CommandPrograms.youtube_list import List

#test_guild_id = 842412412460072964

#@app_commands.guilds(test_guild_id)
@app_commands.default_permissions(administrator=True)
class Youtube(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot

    # /youtube add *
    youtube_add = app_commands.Group(name="add", description="指定されたYouTubeチャンネルやキーワードの更新の通知を送信する設定を行います。")
    
    @youtube_add.command(name="live", description="指定されたYouTubeチャンネルの配信の通知を送信する設定を行います。")
    @app_commands.describe(url="YouTubeチャンネルのURL")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    @app_commands.describe(normal_message="通常の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    @app_commands.describe(wait_message="配信待機場所の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")    
    #@app_commands.describe(channel="投稿先のチャンネル")
    @app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def youtube_live_add(self, interaction: discord.Interaction, url: str, webhook_url: str, normal_message: str = None, wait_message: str = None, mention: discord.Role = None):
        mode = 'live'
        premium_message = "no"

        yt_add = Add()
        await yt_add.add_info(interaction, mode, url, webhook_url, normal_message, wait_message, premium_message, mention)
    
    @youtube_add.command(name="video", description="指定されたYouTubeチャンネルの動画更新の通知を送信する設定を行います。")
    @app_commands.describe(url="YouTubeチャンネルのURL")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    @app_commands.describe(normal_message="通常の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    @app_commands.describe(wait_message="プレミアム公開待機場所の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    @app_commands.describe(premium_message="プレミアム公開の通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")   
    #@app_commands.describe(channel="投稿先のチャンネル")
    @app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def youtube_video_add(self, interaction: discord.Interaction, url: str, webhook_url:str, normal_message: str = None, wait_message: str = None, premium_message: str = None, mention: discord.Role = None):
        mode = 'video'

        yt_add = Add()
        await yt_add.add_info(interaction, mode, url, webhook_url, normal_message, wait_message, premium_message, mention)

    @youtube_add.command(name="shorts", description="指定されたYouTubeチャンネルのショート動画更新の通知を送信する設定を行います。")
    @app_commands.describe(url="YouTubeチャンネルのURL")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    @app_commands.describe(normal_message="通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    #@app_commands.describe(channel="投稿先のチャンネル")
    @app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def youtube_shorts_add(self, interaction: discord.Interaction, url: str, webhook_url:str,  normal_message: str = None, mention: discord.Role = None):
        mode = 'shorts'
        wait_message = "no"
        premium_message = "no"

        yt_add = Add()
        await yt_add.add_info(interaction, mode, url, webhook_url, normal_message, wait_message, premium_message, mention)

    @youtube_add.command(name="search", description="指定されたキーワードでの更新の通知を送信する設定を行います。")
    @app_commands.describe(keyword="検索キーワード")
    @app_commands.describe(webhook_url="Discordで作成したWebhookのURL")
    @app_commands.describe(normal_message="通知をする時に出すメッセージの指定（入力がない場合はデフォルトメッセージを出します。）")
    #@app_commands.describe(channel="投稿先のチャンネル")
    @app_commands.describe(mention="メンションを行うロール（入力がない場合はメンションない状態になります。）")
    async def youtube_search_add(self, interaction: discord.Interaction, keyword: str, webhook_url:str, normal_message: str = None, mention: discord.Role = None):
        mode = 'search'
        wait_message = "no"
        premium_message = "no"

        yt_add = Add()
        await yt_add.add_info(interaction, mode, keyword, webhook_url, normal_message, wait_message, premium_message, mention)
    
    # /youtube delete *
    youtube_delete = app_commands.Group(name="delete", description="指定されたYouTubeチャンネルの更新の通知を送信する設定を削除します。")

    @youtube_delete.command(name="live", description="指定されたYouTubeチャンネルの配信通知を送信する設定を削除します")
    async def youtube_live_delete(self, interaction: discord.Interaction):
        mode = "live"

        yt_delete = Delete()
        await yt_delete.delete_info(interaction, mode)

    @youtube_delete.command(name="video", description="指定されたYouTubeチャンネルの動画の更新の通知を送信する設定を削除します")
    async def youtube_video_delete(self, interaction: discord.Interaction):
        mode = "video"

        yt_delete = Delete()
        await yt_delete.delete_info(interaction, mode)

    @youtube_delete.command(name="shorts", description="指定されたYouTubeチャンネルのショート動画の更新の通知を送信する設定を削除します")
    async def youtube_shorts_delete(self, interaction: discord.Interaction):
        mode = "shorts"

        yt_delete = Delete()
        await yt_delete.delete_info(interaction, mode)

    @youtube_delete.command(name="search", description="指定されたキーワードでの更新の通知を送信する設定を削除します")
    async def youtube_search_delete(self, interaction: discord.Interaction):
        mode = "search"

        yt_delete = Delete()
        await yt_delete.delete_info(interaction, mode)

    # /youtube list *
    youtube_list = app_commands.Group(name="list", description="現在通知が設定されているYouTubeチャンネルやキーワードの一覧を表示します。")
    
    @youtube_list.command(name="live", description="配信の通知が設定されているYouTubeチャンネルの一覧を表示します")
    async def youtube_live_list(self, interaction: discord.Interaction):
        mode = "live"

        yt_list = List()
        await yt_list.list_info(interaction, mode)

    @youtube_list.command(name="video", description="動画の通知が設定されているYouTubeチャンネルの一覧を表示します")
    async def youtube_video_list(self, interaction: discord.Interaction):
        mode = "video"
        
        yt_list = List()
        await yt_list.list_info(interaction, mode)

    @youtube_list.command(name="shorts", description="ショート動画の通知が設定されているYouTubeチャンネルの一覧を表示します")
    async def youtube_shorts_list(self, interaction: discord.Interaction):
        mode = "shorts"
        
        yt_list = List()
        await yt_list.list_info(interaction, mode)

    @youtube_list.command(name="search", description="指定されたキーワードでの通知が設定されているキーワードの一覧を表示します")
    async def youtube_search_list(self, interaction: discord.Interaction):
        mode = "search"
        
        yt_list = List()
        await yt_list.list_info(interaction, mode)
    
async def setup(bot: commands.Bot):
    bot.tree.add_command(Youtube(bot, name="youtube"))