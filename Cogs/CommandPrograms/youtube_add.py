# Discord bot import
import discord
import ndjson
import glob
import datetime
import dateutil.parser
import re
import os
import requests
import scrapetube
import feedparser
from bs4 import BeautifulSoup

# My program import
from webhook import webhook_sender

class Add:
    async def add_info(self, interaction, mode, word, webhook_url, normal_message, wait_message, premium_message, mention):
        
        await interaction.response.defer()

        # webhookを使う準備
        webhook_send = webhook_sender()

        if mode == "live" or mode == "video" or mode == "shorts":
            
            # 処理に用にmodeを書き換える
            if mode == 'live':
                mode = 'streams'

            if mode == 'video':
                mode = 'videos'
            
            # webhook URLが正当なものかを確認
            try:
                await webhook_send.webhook_send(webhook_url, "Test Webhook", "no", "Test message")

            except Exception as e:
                embed=discord.Embed(title="エラー！", description=":x:入力した内容を確認してください。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return
            
            # チャンネルの正当性をライブラリを用いて確認
            try:
                streams = scrapetube.get_channel(channel_url=word, limit=2, sort_by="newest", content_type="streams")

                for stream in streams:
                    print(stream['videoId'])
            except Exception as e:
                embed=discord.Embed(title="エラー！", description=":x:入力した内容を確認してください。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return

            # チャンネルのidを取得する、チャンネルのアイコンを取得する
            url = word
            res = requests.get(url)

            soup = BeautifulSoup(res.text, "html.parser")

            elems = soup.find_all(itemprop=re.compile("identifier"))
            elems1 = soup.find_all(rel=re.compile("image_src"))

            yt_channel_id = elems[0].attrs['content']
            yt_picture_url = elems1[0].attrs['href']

            # チャンネル名を取得する
            feed_url = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=' + yt_channel_id)

            for entry in feed_url.entries:
                yt_channel_name = entry.author
                break

            # チャンネルの更新状況を取得
            
            channel_content = scrapetube.get_channel(channel_url=word, limit=10, sort_by="newest", content_type=mode)

            # ギルドのフォルダがあるかの確認
            judge = 0
            dir_data = os.listdir(path='./data/data_json')
            for i in range(0, len(dir_data)):
                if str(interaction.guild.id) == dir_data[i]:
                    judge = 1
                    break

            if judge != 1: # なければ作成する
                os.mkdir('./data/data_json/' + str(interaction.guild.id))
            
            # モードのファイルがあるかの確認
            judge = 0
            dir_data = os.listdir(path='./data/data_json/' + str(interaction.guild.id))
            for i in range(0, len(dir_data)):
                if mode == dir_data[i]:
                    judge = 1
                    break

            if judge != 1: # なければ作成する
                os.mkdir('./data/data_json/' + str(interaction.guild.id) + '/' + mode)
            

            # 指定のyoutubeチャンネルのndjsonファイルが存在しているかの確認
            files = glob.glob('./data/data_json/' + str(interaction.guild.id) + '/' + mode + '/*.ndjson')
            judge = 0

            for i in range(0, len(files)):
                print(os.path.split(files[i])[1])
                if(os.path.split(files[i])[1] == yt_channel_id + ".ndjson"):
                    #print("一致しました！")
                    judge = 1
                    break
            
            if judge != 1:
                # もし一致しなければ、チャンネルの更新状況を保存する
                if mode == "streams":
                    for stream in channel_content:
                        try:
                            StartTime = stream['upcomingEventData']['startTime']
                        except Exception as e:
                            StartTime = "no"
                        
                        content = {
                            "videoId" : stream['videoId'],
                            "style" : stream['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style'],
                            "StartTime" : StartTime,
                            "nofication" : "no"
                        }

                        with open('./data/data_json/' + str(interaction.guild.id) + '/' + mode  + '/' + yt_channel_id + ".ndjson", 'a') as f:
                            writer = ndjson.writer(f)
                            writer.writerow(content)
                elif mode == "videos":
                     for video in channel_content:
                        try:
                            StartTime = video['upcomingEventData']['startTime']
                        except Exception as e:
                            StartTime = "no"

                        content = {
                            "videoId" : video['videoId'],
                            "style" : video['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style'],
                            "StartTime" : StartTime,
                            "nofication" : "no"
                        }

                        with open('./data/data_json/' + str(interaction.guild.id) + '/' + mode  + '/' + yt_channel_id + ".ndjson", 'a') as f:
                            writer = ndjson.writer(f)
                            writer.writerow(content)
                elif mode == "shorts":
                    for short in channel_content:
                        content = {
                            "videoId" : short['videoId']
                        }

                        with open('./data/data_json/' + str(interaction.guild.id) + '/' + mode  + '/' + yt_channel_id + ".ndjson", 'a') as f:
                            writer = ndjson.writer(f)
                            writer.writerow(content)
            else:
                embed=discord.Embed(title="エラー！", description=":x:既に同じチャンネルの通知設定が登録されています。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return
            
            # メンションの指定がなければ
            if mention ==  None:
                mention_info = "Off"
            else:
                mention_info = mention.id
            
            # メッセージの指定がなければ
            if normal_message == None:
                normal_message = "更新されました！"
            
            # 待機場所のメッセージの指定がなければ
            if wait_message == None:
                wait_message = "待機所が作成されました！"
            
            # プレミアム公開のメッセージの指定がなければ
            if premium_message == None:
                premium_message = "プレミアム公開が始まりました！"

            # guild_jsonフォルダにサーバーidのフォルダを作成
            content = {
                    "type" : mode,
                    "name" : yt_channel_name,
                    "add_id" : yt_channel_id,
                    "picture_url" : yt_picture_url,
                    "latest_time": str(datetime.datetime.now()),
                    "webhook_url": webhook_url,
                    "mention": mention_info,
                    "normal_message": normal_message,
                    "wait_message": wait_message,
                    "premium_message": premium_message
            }

            with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(content)

            # 最後に表示させるように変えたmodeをもとに戻す
            if mode == "streams":
                mode = "live"
            
            if mode == 'videos':
                mode = 'video'
            
            print("登録しました!:" + word + "の入力されたチャンネルの通知を設定しました。")
            if mention == None:
                embed=discord.Embed(title="登録しました!", description=word + "\nこの入力されたチャンネルの通知を設定しました。\n\nタイプ：" + mode + "\nチャンネル名：" + yt_channel_name +"\nメンション：@" + mention_info + "\n 通常メッセージ：" + normal_message + "\n 待機場所メッセージ：" + wait_message + "\n プレミアム公開時メッセージ：" + premium_message, color=0x00ff7f) 
            else:
                embed=discord.Embed(title="登録しました!", description=word + "\nこの入力されたチャンネルの通知を設定しました。\n\nタイプ：" + mode + "\nチャンネル名：" + yt_channel_name + "\nメンション：@" + mention.name + "\n 通常メッセージ：" + normal_message + "\n 待機場所メッセージ：" + wait_message + "\n プレミアム公開時メッセージ：" + premium_message, color=0x00ff7f) 

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("まだ実装されていません！")