import json
import asyncio

def load_json(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

class DataLoader:
    def __init__(self):
        self.isRunning = {}
        self.videos_infos = load_json('data/videos_infos.json')
        self.videos_comments = load_json('data/videos_comments_res.json')
        self.videos_danmakus = load_json('data/videos_danmus.json')
        self.videos_sentiment = load_json('data/videos_sentiment.json')
        self.lock = asyncio.Lock()

data_loader = DataLoader()