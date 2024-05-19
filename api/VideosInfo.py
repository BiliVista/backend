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


@api_videos.get("/topinfo/")
async def get_top_info():
    #  Retuen top view, bvid counts, top sentiment, comment counts
    top_view= get_rank("view")[0] # Get the video with the most views
    # Count comments number in each video add them together
    all_comment_counts = sum([data_loader.videos_infos[bvid]["comment"] for bvid in data_loader.videos_infos])
    # Count bvid number
    bvid_counts = len(data_loader.videos_infos)
    # Best sentiment
    top_sentiment = get_rank("sentiment")[0]
    return {"top_view": top_view, "all_comment_counts": all_comment_counts, "video_counts": bvid_counts, "top_sentiment": top_sentiment}

@api_videos.get("/3lianCounts/")
async def get_3lian_counts():
    all_likes = sum([data_loader.videos_infos[bvid]["like"] for bvid in data_loader.videos_infos])
    all_favorite = sum([data_loader.videos_infos[bvid]["favorite"] for bvid in data_loader.videos_infos])
    all_coin = sum([data_loader.videos_infos[bvid]["coin"] for bvid in data_loader.videos_infos])
    return {"like": all_likes, "favorite": all_favorite, "coin": all_coin}