import requests, json


webhook_url  = 'discord_url'

main_content = {
                   'username': 'Test',
                   'avatar_url': 'picture_url',
                   'content': 'テスト',
               }
headers      = {'Content-Type': 'application/json'}

response     = requests.post(webhook_url, json.dumps(main_content), headers=headers)