import scrapetube

streams = scrapetube.get_channel(channel_url="your_youtube_link", limit=5, sort_by="newest", content_type="streams")

for stream in streams:
    #print(stream['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style']) # 配信予定地か、配信しているか、デフォルトでいるか　shorts以外は動く
    #print("video id : " + stream['videoId'] + ", title : " + stream['title']['runs'][0]['text']) # titleとVideIdを取得する
    #print(stream['upcomingEventData']['startTime']) # upcomig状態の配信もしくは、動画で動く　#配信前の待機所または、プレミアム公開前の動画
    print(stream)