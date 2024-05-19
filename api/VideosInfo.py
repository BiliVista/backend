from fastapi import APIRouter
from .DataLoader import data_loader

api_videos = APIRouter()

def check_running(): # Check the dict isRunning to see if contain any True value
    for bvid in data_loader.isRunning:
        if data_loader.isRunning[bvid] == True:
            return True
    return False

def get_rank(key):
    ranks = [{"bvid": bvid, "count": data_loader.videos_infos[bvid][key], "title": data_loader.videos_infos[bvid]['title'], "author": data_loader.videos_infos[bvid]['author'], "pic": data_loader.videos_infos[bvid]['pic']} for bvid in data_loader.videos_infos]
    return sorted(ranks, key=lambda x: x['count'], reverse=True)

@api_videos.get("/infos/")
async def get_videos_infos():
    if check_running():
        return data_loader.videos_infos
    return data_loader.videos_infos

@api_videos.get("/counts/{type}/rank/")
async def get_rank_by_type(type: str):
    valid_types = ["comment", "view", "like", "favorite", "coin", "share"]
    if type in valid_types:
        return get_rank(type)
    return {"error": "Invalid type"}

@api_videos.get("/sentiment/rank/")
async def get_sentimentRank():
    sentimentRanks = []
    for bvid in data_loader.videos_infos or bvid in data_loader.videos_sentiment: 
        if bvid not in data_loader.videos_sentiment:
            data_loader.videos_sentiment[bvid] = -1
        if bvid not in data_loader.videos_infos:
            data_loader.videos_infos[bvid] = {"title": "Unknown", "author": "Unknown", "pic": "Unknown"}
        sentimentRanks.append({"bvid": bvid, "sentiment": data_loader.videos_sentiment[bvid], "title": data_loader.videos_infos[bvid]['title'], "author": data_loader.videos_infos[bvid]['author'], "pic": data_loader.videos_infos[bvid]['pic']})
    # Sort the videos by the sentiment 
    sentimentRanks = sorted(sentimentRanks, key=lambda x: x['sentiment'], reverse=True)    
    return sentimentRanks

@api_videos.get("/anyRunning/")
async def get_any_running():
    return {"status": "running" if check_running() else "finish"}


# while 1:
#     if(check_running()):
#         print(1)
#         break