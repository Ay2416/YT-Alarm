import feedparser

url = feedparser.parse('your_youtube_link')

for entry in url.entries:
    print(entry.author)
