from fastapi import APIRouter
from .DataLoader import data_loader
from math import ceil

api_videos = APIRouter()

def check_running(): # Check the dict isRunning to see if contain any True value
    for bvid in data_loader.isRunning:
        if data_loader.isRunning[bvid] == True:
            return True
    return False

def get_rank(key):
    ranks = [{"bvid": bvid, "count": data_loader.videos_infos[bvid][key], "title": data_loader.videos_infos[bvid]['title'], "author": data_loader.videos_infos[bvid]['author'], "pic": data_loader.videos_infos[bvid]['pic']} for bvid in data_loader.videos_infos]
    return sorted(ranks, key=lambda x: x['count'], reverse=True)



# like/view ratio
@api_videos.get("/likeviewratio/")
async def get_like_view_ratio():
    like_view_ratio = []
    for bvid in data_loader.videos_infos:
        if data_loader.videos_infos[bvid]["view"] == 0:
            like_view_ratio.append({"bvid": bvid, "ratio": 0, "title": data_loader.videos_infos[bvid]['title'], "author": data_loader.videos_infos[bvid]['author'], "pic": data_loader.videos_infos[bvid]['pic']})
        else:
            like_view_ratio.append({"bvid": bvid, "ratio": data_loader.videos_infos[bvid]["like"]/data_loader.videos_infos[bvid]["view"], "title": data_loader.videos_infos[bvid]['title'], "author": data_loader.videos_infos[bvid]['author'], "pic": data_loader.videos_infos[bvid]['pic']})
    like_view_ratio = sorted(like_view_ratio, key=lambda x: x['ratio'], reverse=True)
    return like_view_ratio

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


# @api_videos.get("/topinfo/")
# async def get_top_info():
#     #  Retuen top view, bvid counts, top sentiment, comment counts
#     top_view= get_rank("view")[0] # Get the video with the most views
#     # Count comments number in each video add them together
#     all_comment_counts = sum([data_loader.videos_infos[bvid]["reply"] for bvid in data_loader.videos_infos])
#     # Count bvid number
#     bvid_counts = len(data_loader.videos_infos)
#     # Best sentiment
#     top_sentiment = get_rank("sentiment")[0]
#     return {"top_view": top_view, "all_comment_counts": all_comment_counts, "video_counts": bvid_counts, "top_sentiment": top_sentiment}



@api_videos.get("/counts/{type}/rank/")
async def get_rank_by_type(type: str,limit:int=5):
    valid_types = ["reply", "view", "like", "favorite", "coin", "share"]
    if type in valid_types:
        data=get_rank(type)[:limit]
        return {"code":20000,"data": data}
    return {"code":10000,"msg": "Invalid type"}


"""

下面是真正用到的API

"""



@api_videos.get("/count/3lian/")
async def get_3lian_counts():
    try:
        all_likes = sum([data_loader.videos_infos[bvid]["like"] for bvid in data_loader.videos_infos])
        all_favorite = sum([data_loader.videos_infos[bvid]["favorite"] for bvid in data_loader.videos_infos])
        all_coin = sum([data_loader.videos_infos[bvid]["coin"] for bvid in data_loader.videos_infos])
        return {"code":20000,"data":{"like": all_likes, "favorite": all_favorite, "coin": all_coin} }
    except Exception as e:
        return {"code":10000,"msg":e}


@api_videos.get("/rate/compare/")
async def get_sentimentRank():
    points = []
    for bvid in data_loader.videos_infos: 
        if bvid in data_loader.videos_sentiment.keys():
            y=data_loader.videos_sentiment[bvid]
            x=data_loader.videos_infos[bvid]["like"]/data_loader.videos_infos[bvid]["view"]
            points.append({"x":ceil(x*10000),"y":ceil(y*100)})
    points = sorted( points, key=lambda x: x['x'])    
    return  {"data":points,"code":20000}


@api_videos.get("/popular/list")
async def get_rank_by_type(type: str="likeRate",limit:int=10):
    if type=="likeRate":
        data = [{"key":bvid,"rate": ceil(data_loader.videos_infos[bvid]['like']/data_loader.videos_infos[bvid]['view']*10000), "title": data_loader.videos_infos[bvid]['title']} for bvid in data_loader.videos_infos]
        data=sorted(data, key=lambda x: x['rate'], reverse=True)[:limit]
        return {"code":20000,"data": data}
    elif type=="commentRate":
        data = [{"key":bvid,"rate": ceil(data_loader.videos_sentiment[bvid]*100), "title": data_loader.videos_infos[bvid]['title']} for bvid in data_loader.videos_infos if bvid in data_loader.videos_sentiment.keys()]
        data=sorted(data, key=lambda x: x['rate'], reverse=True)[:limit]
        return {"code":20000,"data": data}
    return {"code":10000,"msg": type}


@api_videos.get("/infos/")
async def get_videos_infos():
    data=[{"rate":data_loader.videos_sentiment.get(i,-1),"bvid":i,"author":data_loader.videos_infos[i]["author"],"title":data_loader.videos_infos[i]["title"],"like":data_loader.videos_infos[i]["like"],"share":data_loader.videos_infos[i]["share"],"img":data_loader.videos_infos[i]["pic"]} for i in data_loader.videos_infos.keys() ]
    return {"code":20000,"data": data}


@api_videos.get("/table/")
async def get_videos_infos(limit:int=1000):
    data=[]
    for i in data_loader.videos_comments.keys():
        for com in data_loader.videos_comments[i]:
            res=com
            res["bvid"]=i
            data.append(res)
            if len(data)>=limit: break
    return {"code":20000,"data": data}


@api_videos.get("/count/basic/")
async def get_basic_counts():
    # try:
    view=get_rank("view")[0]["count"]/10000
    video= len(data_loader.videos_infos)
    s=0
    for i in data_loader.videos_comments.values():
        s+=len(i)
    comment=s
    sentiment= max(data_loader.videos_sentiment.values())*100
    return {"code":20000,"data":{'view':view,'video':video,'comment':comment,'sentiment':sentiment } }
    # except Exception as e:
    #     return {"code":10000,"msg":e}