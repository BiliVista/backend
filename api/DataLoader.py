import json

def load_json(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

videos_infos = load_json('data/videos_infos.json')
videos_comments = load_json('data/videos_comments_res.json')
videos_danmakus = load_json('data/videos_danmus.json')
videos_sentiment = load_json('data/videos_sentiment.json')