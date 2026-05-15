# Discord_YT-Alarm

# Japanese
## 概要
YouTubeチャンネルの更新情報（ライブ配信、動画、Shorts）を、公式のYouTube APIを使用せずにDiscordチャンネルへ通知するDiscord Botです。

## 使用技術
- 言語: Python 3.x
- ライブラリ/フレームワーク: discord.py, beautifulsoup4, feedparser, ndjson, python-dotenv, requests, scrapetube
- データベース: ndjson（ローカルファイルへのJSON保存）
- その他: なし

## 使い方
### 前提条件
- Python 3.x がインストールされていること
- Discord Botのトークンを取得済みであること
- 通知先のDiscordチャンネルでWebhook URLを取得済みであること

### インストール方法
以下の手順に従って、ご自身の環境にプロジェクトをセットアップしてください。

1. リポジトリをクローンします。
```bash
git clone https://github.com/ay2416/YT-Alarm.git
```

2. プロジェクトのディレクトリに移動します。
```bash
cd YT-Alarm
```

3. 必要なパッケージをインストールします。
```bash
pip install -r requirements.txt
```

### 基本的な使い方
```bash
python main.py
```

## 主な機能

- **`/youtube add [live/video/shorts]`**
  YouTubeの通知を送信するチャンネルを追加します。
  - `url` (必須): YouTubeチャンネルのURLを入力します。
  - `webhook_url` (必須): 通知先Discordチャンネルで事前に作成したWebhookのURLを入力します。
  - `normal_message` (任意): 動画・Shortsの更新時に表示されるメッセージを指定します（指定がない場合は「更新されました！」になります）。
  - `wait_message` (任意): 配信やプレミアム公開の待機所作成時に表示されるメッセージを指定します（指定がない場合は「待機所が作成されました！」になります）。
  - `premium_message` (任意): プレミアム公開の開始時に表示されるメッセージを指定します（指定がない場合は「プレミアム公開が始まりました！」になります）。
  - `mention` (任意): メンションするロールを指定します（指定がない場合はメンションなしで通知されます）。

- **`/youtube delete [live/video/shorts]`**
  YouTubeの通知を送信するチャンネルの登録を削除します。

- **`/youtube list [live/video/shorts]`**
  通知登録があるチャンネルの一覧を表示します。

- **`/help`**
  このBotのコマンドの簡単な使い方を表示します。
  ※`/help` 以外のコマンドはサーバー管理者のみ使用可能です。

## 設定
プロジェクトルートディレクトリに `.env` ファイルを作成し、以下の環境変数を設定してください。
- `token` : Discord Botのトークン

## ライセンス
MIT License

# English
## Overview
A Discord Bot that sends YouTube channel update notifications (live streams, videos, Shorts) to a Discord channel without using the official YouTube API.

## Technologies Used
- Language: Python 3.x
- Libraries/Frameworks: discord.py, beautifulsoup4, feedparser, ndjson, python-dotenv, requests, scrapetube
- Database: ndjson (JSON saved to local files)
- Other: None

## Usage
### Prerequisites
- Python 3.x is installed
- Discord Bot token is acquired
- Webhook URL is acquired for the destination Discord channel

### Installation
Follow the steps below to set up the project in your environment.

1. Clone the repository.
```bash
git clone https://github.com/ay2416/YT-Alarm.git
```

2. Move to the project directory.
```bash
cd YT-Alarm
```

3. Install the required packages.
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
python main.py
```

## Key Features

- **`/youtube add [live/video/shorts]`**
  Adds a YouTube channel for sending notifications.
  - `url` (Required): Enter the URL of the YouTube channel.
  - `webhook_url` (Required): Enter the Webhook URL created in the destination Discord channel.
  - `normal_message` (Optional): Specify the message displayed when a video/Shorts is updated (Default: "更新されました！").
  - `wait_message` (Optional): Specify the message displayed when a live stream or premiere waiting room is created (Default: "待機所が作成されました！").
  - `premium_message` (Optional): Specify the message displayed when a premiere starts (Default: "プレミアム公開が始まりました！").
  - `mention` (Optional): Specify the role to mention upon notification (Default: No mention).

- **`/youtube delete [live/video/shorts]`**
  Deletes a registered YouTube channel from notifications.

- **`/youtube list [live/video/shorts]`**
  Displays a list of currently registered channels for notifications.

- **`/help`**
  Displays simple usage instructions for the bot's commands.
  *Note: All commands except `/help` can only be used by server administrators.*

## Configuration
Create a `.env` file in the project root directory and configure the following environment variable.
- `token` : Discord Bot Token

## License
MIT License
