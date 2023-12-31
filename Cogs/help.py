# Discord bot import
import discord
from discord import app_commands
from discord.ext import commands

# My program import


#test_guild_id = your_guild_id

class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="コマンドについての簡単な使い方を出します。")
    #@app_commands.guilds(test_guild_id)
    #@app_commands.default_permissions(administrator=True)
    async def help_command(self, interaction: discord.Interaction):
        embed=discord.Embed(title="コマンドリスト")
        embed.add_field(name="このBotは/help以外はサーバー管理者しか使用することができません。", value="", inline=False)
        embed.add_field(name="/youtube add [live/video/shorts]", value="YouTubeの通知を送信するチャンネルを追加します。\n\n**__引数の説明（必須項目には「※必須」とつけています。）__**\n\n__url：（※必須）YouTubeチャンネルのURLを入力してください。__\n\n__webhook_url：（※必須）Discordのチャンネルで事前に作成したWebhookのURLを入力してください。__\n\n__normal_message：動画・Shortsの更新がされた時に表示されるメッセージを指定します。指定がなければ「更新されました！」になります。__\n\n__wait_message：配信やプレミアム公開の待機所が作成された時に表示されるメッセージを指定します。指定がなければ「待機所が作成されました！」になります。__\n\n__premium_message：プレミアム公開が開始された時に表示されるメッセージを指定します。指定がなければ、「プレミアム公開が始まりました！」になります。__\n\n__mention：メンションするロールを指定します。指定がなければ、メンションはしないで通知が表示されます。__", inline=False)
        embed.add_field(name="/youtube delete [live/video/shorts]", value="YouTubeの通知を送信するチャンネルを削除します。", inline=False)
        embed.add_field(name="/youtube list [live/video/shorts]", value="戦績を送信する登録があるプレイヤーの一覧を表示します。", inline=False)
        embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot))