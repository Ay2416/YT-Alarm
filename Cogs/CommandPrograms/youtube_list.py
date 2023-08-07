import discord
import ndjson
import glob
import os
import asyncio

class List:
    async def list_info(self, interaction, mode):
        
        await interaction.response.defer()

        # modeを処理用に中身を変える
        if mode == 'live':
            mode1 = 'streams'
        elif mode == 'video':
            mode1 = 'videos'
        else:
            mode1 = mode

        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge != 1:
                embed=discord.Embed(title="エラー！", description=":x:このサーバーのデータが存在していません。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return

        # サーバーのデータを表示させる処理
        if mode == "live" or mode == "video" or mode == "shorts":
            with open('./data/guild_json/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)
            
            search_num = 0
            for i in range(0, len(read_data)):
                if read_data[i]["type"] == mode1:
                    search_num += 1
            
            if search_num == 0:
                embed=discord.Embed(title="エラー！", description=":x:このサーバーの "+ mode +" のデータが存在していません。:x:", color=0xff0000)
                await interaction.followup.send(embed=embed)
                return

            embed=discord.Embed(title="登録されている通知（" + mode + "）", color=0x00ff7f)

            cut = 10
            count = 0
            for j in range(0, len(read_data)):
                # メンションの表示を指定
                mention_view = ' '
                if read_data[i]["mention"] == 'Off':
                    mention_view = read_data[i]["mention"]
                else:
                    mention_view = '<@&' + str(read_data[i]["mention"]) + '>'

                if read_data[j]["type"] == mode1:
                    embed.add_field(name=str(count+1) + '. ' + read_data[j]["name"], value="チャンネルURL：" + 'https://www.youtube.com/channel/' + read_data[j]["add_id"]
                                    +"\nメンション：" + mention_view + "\n通常メッセージ：" + read_data[j]["normal_message"] + "\n 待機場所メッセージ：" 
                                    + read_data[j]["wait_message"] + "\n プレミアム公開時メッセージ：" + read_data[j]["premium_message"], inline=False)

                    count += 1
                
                if j == len(read_data) - 1:
                    #表示させる
                    await interaction.followup.send(embed=embed)
                    return
                
                if count + 1 == cut:
                    cut = cut + 25
                    #表示させる
                    await interaction.followup.send(embed=embed)
                    embed=discord.Embed(title="")
                    
                    # DiscordのWebhook送信制限に引っかからないための対策　※効果があるかは不明
                    await asyncio.sleep(2)
                
        else:
            await interaction.followup.send("まだ実装されていません！")