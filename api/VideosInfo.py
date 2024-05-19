from fastapi import APIRouter
from .DataLoader import videos_infos, videos_sentiment, load_json

api_videos = APIRouter()

isRunning = {}

def check_running():
    return any(isRunning.values())

# Generic function to get video ranks
def get_rank(key):
    ranks = [{"bvid": bvid, "count": videos_infos[bvid][key], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']} for bvid in videos_infos]
    return sorted(ranks, key=lambda x: x['count'], reverse=True)

@api_videos.get("/infos/")
async def get_videos_infos():
    print(check_running())
    if check_running():
        return load_json('videos_infos.json')
    return videos_infos

@api_videos.get("/counts/{type}/rank/")
async def get_rank_by_type(type: str):
    valid_types = ["reply", "view", "like", "favorite", "coin", "share","danmaku"]
    if type in valid_types:
        return get_rank(type)
    return {"error": "Invalid type"}

@api_videos.get("/sentiment/rank/")
async def get_sentimentRank():
    sentimentRanks = []
    for bvid in videos_infos or bvid in videos_sentiment: 
        if bvid not in videos_sentiment:
            videos_sentiment[bvid] = -1
        if bvid not in videos_infos:
            videos_infos[bvid] = {"title": "Unknown", "author": "Unknown", "pic": "Unknown"}
        sentimentRanks.append({"bvid": bvid, "sentiment": videos_sentiment[bvid], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the sentiment 
    sentimentRanks = sorted(sentimentRanks, key=lambda x: x['sentiment'], reverse=True)    
    return sentimentRanks

@api_videos.get("/anyRunning/")
async def get_any_running():
    return {"status": "running" if check_running() else "finish"}