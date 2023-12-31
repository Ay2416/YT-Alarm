# Discord bot import
import discord
import ndjson
import glob
import time
import os
import re
import requests
import datetime
import dateutil.parser
import asyncio
import scrapetube
import feedparser
from bs4 import BeautifulSoup

# My program import
from webhook import webhook_sender

# 変数
# 文字列にした時間を計算できる形式に変換する時に使用
time_format = '%Y-%m-%d %H:%M:%S.%f'

class Task:
    async def send_discord(self, bot):
        # webhookを使う準備
        webhook_send = webhook_sender()

        # guild_jsonのファイル一覧を取得
        files = glob.glob('./data/guild_json/*.ndjson')
        #print(files)
        
        # 1つのギルドごとに処理を開始
        for i in range(0, len(files)):
            # guildごとのndjsonファイルの読み込み
            with open(files[i]) as f:
                guild_data = ndjson.load(f)

            for j in range(0, len(guild_data)):
                # もし前回の更新から3分経っていたら
                update_time = datetime.datetime.strptime(guild_data[j]["latest_time"], time_format)
                if (datetime.datetime.now() - update_time).total_seconds() >= 180:
                    #print(os.path.split(files[i])[0])
                    #print(guild_data[j])
                    # 現在のdata_jsonの読込
                    with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson") as f:
                        old_data = ndjson.load(f)
                    # streamsの場合
                    if guild_data[j]["type"] == 'streams':
                        # 最新のデータを取ってくる
                        try:
                            channel_content = scrapetube.get_channel(channel_url='https://youtube.com/channel/' + guild_data[j]['add_id'], limit=10, sort_by="newest", content_type="streams")
                        except Exception as e:
                            print('scrapetubeデータ取得でエラーが発生しました。')
                            continue

                        # データをjson形式で変数に入れる
                        now_data = []

                        for stream in channel_content:
                            try:
                                StartTime = stream['upcomingEventData']['startTime']
                            except Exception as e:
                                StartTime = "no"
                            
                            content = {
                                "videoId" : stream['videoId'],
                                "style" : stream['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style'],
                                "StartTime" : StartTime,
                                "wait_nofication" : "no",
                                "premium_nofication" : "no"
                            }

                            now_data.append(content)

                        # nofication が yes の場合の引木継ぎ
                        for k in range(0, len(now_data)):
                                for l in range(0, len(old_data)):
                                    if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["wait_nofication"] == "yes":
                                        now_data[k]["wait_nofication"] = "yes"

                                    if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["premium_nofication"] == "yes":
                                        now_data[k]["premium_nofication"] = "yes"

                        for m in range(0, len(now_data)):
                            # upcomingのものがある場合は1時間前になった場合に通知を出す
                            if now_data[m]["style"] == "UPCOMING" and now_data[m]["StartTime"] != 'no' and now_data[m]["wait_nofication"] != "yes":
                                now = time.time()
                                if now - int(now_data[m]["StartTime"]) <= 3600:

                                    # メンションの設定はあるかの確認
                                    send_message = ""
                                    if guild_data[j]["mention"] != "Off":
                                        send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                    
                                    # 通知の送信
                                    send_message += '\n' + guild_data[j]["wait_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                    await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                    # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                    now_data[m]["wait_nofication"] = "yes"
                            
                            # liveのものがある場合は通知を出す
                            elif now_data[m]["style"] == "LIVE" and now_data[m]["premium_nofication"] != "yes":
                                
                                # メンションの設定はあるかの確認
                                send_message = ""
                                if guild_data[j]["mention"] != "Off":
                                        send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                
                                # 通知の送信
                                send_message += '\n' + guild_data[j]["normal_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                now_data[m]["premium_nofication"] = "yes"

                        # 更新されたデータをdata_jsonに保存していく
                        os.remove('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson")
                        
                        for n in range(0, len(now_data)):

                            with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson", 'a') as f:
                                writer = ndjson.writer(f)
                                writer.writerow(now_data[n])
                    
                    # videoの場合
                    elif guild_data[j]["type"] == 'videos':
                        # 最新のデータを取ってくる
                        try:
                            channel_content = scrapetube.get_channel(channel_url='https://youtube.com/channel/' + guild_data[j]['add_id'], limit=10, sort_by="newest", content_type="videos")
                        except Exception as e:
                            print('scrapetubeデータ取得でエラーが発生しました。')
                            continue

                        # データをjson形式で変数に入れる
                        now_data = []

                        for video in channel_content:
                            try:
                                StartTime = video['upcomingEventData']['startTime']
                            except Exception as e:
                                StartTime = "no"
                            
                            content = {
                                "videoId" : video['videoId'],
                                "style" : video['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style'],
                                "StartTime" : StartTime,
                                "normal_nofication" : "no",
                                "wait_nofication" : "no",
                                "premium_nofication" : "no"
                            }

                            now_data.append(content)

                        # nofication が yes の場合の引木継ぎ
                        for k in range(0, len(now_data)):
                                for l in range(0, len(old_data)):
                                    if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["normal_nofication"] == "yes":
                                        now_data[k]["normal_nofication"] = "yes"

                                    if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["wait_nofication"] == "yes":
                                        now_data[k]["wait_nofication"] = "yes"

                                    if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["premium_nofication"] == "yes":
                                        now_data[k]["premium_nofication"] = "yes"

                        for m in range(0, len(now_data)):
                            # upcomingのものがある場合は1時間前になった場合に通知を出す
                            if now_data[m]["style"] == "UPCOMING" and now_data[m]["StartTime"] != 'no' and now_data[m]["wait_nofication"] != "yes":
                                now = time.time()
                                if now - int(now_data[m]["StartTime"]) <= 3600:

                                    # メンションの設定はあるかの確認
                                    send_message = ""
                                    if guild_data[j]["mention"] != "Off":
                                        send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                    
                                    # 通知の送信
                                    send_message += '\n' + guild_data[j]["wait_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                    await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                    # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                    now_data[m]["wait_nofication"] = "yes"
                            
                            # liveのものがある場合は通知を出す
                            elif now_data[m]["style"] == "LIVE" and now_data[m]["premium_nofication"] != "yes":
                                
                                # メンションの設定はあるかの確認
                                send_message = ""
                                if guild_data[j]["mention"] != "Off":
                                    send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                
                                # 通知の送信
                                send_message += '\n' + guild_data[j]["premium_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                now_data[m]["premium_nofication"] = "yes"
                            
                            # defaultの者がある場合は通知を出す
                            elif now_data[m]["style"] == "DEFAULT":
                                # old_dataの中でdefalutの一番新しい情報を探す
                                for l in range(0, len(old_data)):
                                    if old_data[l]["style"] == "DEFAULT":
                                        hozon_videoId = old_data[l]["videoId"]
                                        break
                                
                                # new_dataとold_dataの１番上に来てるものよりも上にあるものを投稿されたものとして扱う
                                for n in range(0, len(now_data)):
                                    if now_data[n]["style"] == "DEFAULT" and now_data[n]["videoId"] == hozon_videoId:
                                        hozon_num = n

                                # 更新を行う
                                for o in range(hozon_num,-1,-1):
                                    if now_data[o]["style"] == "DEFAULT" and now_data[o]["normal_nofication"] != "yes":

                                        # メンションの設定はあるかの確認
                                        send_message = ""
                                        if guild_data[j]["mention"] != "Off":
                                            send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                        
                                        # 通知の送信
                                        send_message += '\n' + guild_data[j]["normal_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                        await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                        # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                        now_data[o]["normal_nofication"] = "yes"

                        # 更新されたデータをdata_jsonに保存していく
                        os.remove('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson")
                        
                        for n in range(0, len(now_data)):

                            with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson", 'a') as f:
                                writer = ndjson.writer(f)
                                writer.writerow(now_data[n])
                    # shortsの場合
                    elif guild_data[j]["type"] == 'shorts':
                        # 最新のデータを取ってくる
                        try:
                            channel_content = scrapetube.get_channel(channel_url='https://youtube.com/channel/' + guild_data[j]['add_id'], limit=10, sort_by="newest", content_type="shorts")
                        except Exception as e:
                            print('scrapetubeデータ取得でエラーが発生しました。')
                            continue

                        # データをjson形式で変数に入れる
                        now_data = []

                        for video in channel_content:
                            try:
                                StartTime = video['upcomingEventData']['startTime']
                            except Exception as e:
                                StartTime = "no"
                            
                            content = {
                                "videoId" : video['videoId'],
                                "StartTime" : StartTime,
                                "normal_nofication" : "no"
                            }

                            now_data.append(content)

                        # nofication が yes の場合の引木継ぎ
                        for k in range(0, len(now_data)):
                            for l in range(0, len(old_data)):
                                if now_data[k]["videoId"] == old_data[l]["videoId"] and old_data[l]["normal_nofication"] == "yes":
                                    now_data[k]["normal_nofication"] = "yes"
                        
                        for m in range(0, len(now_data)):
                            if now_data[m]["normal_nofication"] != "yes":
                                # old_dataの中でdefalutの一番新しい情報を探す
                                hozon_videoId = old_data[0]["videoId"]
                                
                                # new_dataとold_dataの１番上に来てるものよりも上にあるものを投稿されたものとして扱う
                                for n in range(0, len(now_data)):
                                    if now_data[n]["videoId"] == hozon_videoId:
                                        hozon_num = n

                                # 更新を行う
                                for o in range(hozon_num,-1,-1):

                                    # メンションの設定はあるかの確認
                                    send_message = ""
                                    if now_data[o]["normal_nofication"] != "yes":
                                        if guild_data[j]["mention"] != "Off":
                                            send_message = '<@&' + str(guild_data[j]["mention"]) + '>\n'
                                        
                                        # 通知の送信
                                        send_message += '\n' + guild_data[j]["normal_message"] + '\nhttps://youtu.be/' + now_data[m]['videoId']
                                        await webhook_send.webhook_send(guild_data[j]["webhook_url"], guild_data[j]["name"], guild_data[j]["picture_url"],send_message)

                                        # 通知を出したものはdata_jsonの「nofication」をyesに変更する
                                        now_data[o]["normal_nofication"] = "yes"

                        # 更新されたデータをdata_jsonに保存していく
                        os.remove('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson")
                        
                        for n in range(0, len(now_data)):

                            with open('./data/data_json/' + os.path.splitext(os.path.basename(files[i]))[0] + '/' + guild_data[j]["type"]  + '/' + guild_data[j]["add_id"] + ".ndjson", 'a') as f:
                                writer = ndjson.writer(f)
                                writer.writerow(now_data[n])
                    
                    # searchの場合
                    else:
                        print('未実装領域')
                    
                    # チャンネル名に更新を入れる
                    # チャンネル名を取得する
                    try:
                        feed_url = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=' + guild_data[j]["add_id"])

                        for entry in feed_url.entries:
                            yt_channel_name = entry.author
                            break
                        
                        guild_data[j]["name"] = yt_channel_name
                    except Exception as e:
                        print("チャンネル名取得でエラーが発生しました。")
                        pass

                    # チャンネルアイコンを更新する
                    try:
                        url = 'https://youtube.com/channel/' + guild_data[j]["add_id"]
                        res = requests.get(url)

                        soup = BeautifulSoup(res.text, "html.parser")
                        
                        elems = soup.find_all(rel=re.compile("image_src"))
                        yt_picture_url = elems[0].attrs['href']

                        guild_data[j]["picture_url"] = yt_picture_url
                    except Exception as e:
                        print("チャンネルアイコン取得でエラーが発生しました。")
                        pass
    
                    # 時間も更新する
                    guild_data[j]["latest_time"] = str(datetime.datetime.now())

                    # 処理が終わったことをprint
                    print(guild_data[j]["type"] + ":" + guild_data[j]["add_id"] + "の処理が終了しました。")

                    # エラー防止のための処理を止める時間
                    await asyncio.sleep(5)
    
            # guild_jsonの更新
            os.remove(files[i])
            for k in range(0, len(guild_data)):
                with open(files[i], 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(guild_data[k])
            
            # 処理が終了したprint
            print("* " + os.path.splitext(os.path.basename(files[i]))[0] + "の処理が終わりました。")
                

        #channel_sent = bot.get_channel(1090113806174273606)
        #await channel_sent.send('test')