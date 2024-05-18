from fastapi import FastAPI
import uvicorn
import json

app = FastAPI()

# Read the json file using the utf-8 encoding
with open('videos_infos.json') as f:
    videos_infos = json.load(f)

# Read the json file using the utf-8 encoding
with open('videos_comments_res.json') as f:
    videos_comments = json.load(f)

# Read the json file using the utf-8 encoding
with open('videos_danmakus.json') as f:
    videos_danmakus = json.load(f)

# Get all video information
@app.get("/videosinfos/")
async def get_videos_infos():
    return videos_infos

# Get the video information
@app.get("/videoinfo/")
async def get_video_info(bvid: str):
    if bvid in videos_infos:
        return videos_infos[bvid]
    else:
        return {"title": "Unknown", "author": "Unknown", "pic": "Unknown", "view": "Unknown", "danmaku": "Unknown", "reply": "Unknown", "favorite": "Unknown", "coin": "Unknown", "share": "Unknown", "like": "Unknown"}
    
# Get author name
@app.get("/author/")
async def get_author(bvid: str):
    if bvid in videos_infos:
        return {"author": videos_infos[bvid]['author']}
    else:
        return {"author": "Unknown"} 

# Get the video title
@app.get("/title/")
async def get_title(bvid: str):
    if bvid in videos_infos:
        return {"title": videos_infos[bvid]['title']}
    else:
        return {"title": "Unknown"}

# Get the video pic
@app.get("/pic/")
async def get_pic(bvid: str):
    if bvid in videos_infos:
        return {"pic": videos_infos[bvid]['pic']}
    else:
        return {"pic": "Unknown"}

# Get the video view
@app.get("/view/")
async def get_view(bvid: str):
    if bvid in videos_infos:
        return {"view": videos_infos[bvid]['view']}
    else:
        return {"view": "Unknown"}
    
# Get the video reply
@app.get("/reply/")
async def get_reply(bvid: str):
    if bvid in videos_infos:
        return {"reply": videos_infos[bvid]['reply']}
    else:
        return {"reply": "Unknown"}

# Get the video favorite
@app.get("/favorite/")
async def get_favorite(bvid: str):
    if bvid in videos_infos:
        return {"favorite": videos_infos[bvid]['favorite']}
    else:
        return {"favorite": "Unknown"}

# Get the video coin
@app.get("/coin/")
async def get_coin(bvid: str):
    if bvid in videos_infos:
        return {"coin": videos_infos[bvid]['coin']}
    else:
        return {"coin": "Unknown"}

# Get the video share
@app.get("/share/")
async def get_share(bvid: str):
    if bvid in videos_infos:
        return {"share": videos_infos[bvid]['share']}
    else:
        return {"share": "Unknown"}

# Get the video like
@app.get("/like/")
async def get_like(bvid: str):
    if bvid in videos_infos:
        return {"like": videos_infos[bvid]['like']}
    else:
        return {"like": "Unknown"}

# Get the video danmaku counts
@app.get("/danmuCounts/")
async def get_danmuCounts(bvid: str):
    if bvid in videos_infos:
        return {"danmuCounts": videos_infos[bvid]['danmaku']}
    else:
        return {"danmaCounts": "Unknown"}

# Get the video comment counts 
@app.get("/commentCounts/")
async def get_commentCounts(bvid: str):
    if bvid in videos_infos:
        return {"commentCounts": videos_infos[bvid]['reply']}
    else:
        return {"commentCounts": "Unknown"}
    

# Get the commentCounts and titles and authors and pics of all videos
@app.get("/commentRank/")
async def get_commentRank():
    commentRanks = []
    for bvid in videos_infos:
        commentRanks.append({"bvid": bvid, "commentCounts": videos_infos[bvid]['reply'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the comment counts 
    commentRanks = sorted(commentRanks, key=lambda x: x['commentCounts'], reverse=True)    
    return commentRanks

# Get the viewCounts and titles and authors and pics of all videos
@app.get("/viewRank/")
async def get_viewRank():
    viewRanks = []
    for bvid in videos_infos:
        viewRanks.append({"bvid": bvid, "viewCounts": videos_infos[bvid]['view'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the view counts 
    viewRanks = sorted(viewRanks, key=lambda x: x['viewCounts'], reverse=True)    
    return viewRanks

# Get the likeCounts and titles and authors and pics of all videos
@app.get("/likeRank/")
async def get_likeRank():
    likeRanks = []
    for bvid in videos_infos:
        likeRanks.append({"bvid": bvid, "likeCounts": videos_infos[bvid]['like'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the like counts 
    likeRanks = sorted(likeRanks, key=lambda x: x['likeCounts'], reverse=True)    
    return likeRanks

# Get the favoriteCounts and titles and authors and pics of all videos
@app.get("/favoriteRank/")
async def get_favoriteRank():
    favoriteRanks = []
    for bvid in videos_infos:
        favoriteRanks.append({"bvid": bvid, "favoriteCounts": videos_infos[bvid]['favorite'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the favorite counts 
    favoriteRanks = sorted(favoriteRanks, key=lambda x: x['favoriteCounts'], reverse=True)    
    return favoriteRanks

# Get the coinCounts and titles and authors and pics of all videos
@app.get("/coinRank/")
async def get_coinRank():
    coinRanks = []
    for bvid in videos_infos:
        coinRanks.append({"bvid": bvid, "coinCounts": videos_infos[bvid]['coin'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the coin counts 
    coinRanks = sorted(coinRanks, key=lambda x: x['coinCounts'], reverse=True)    
    return coinRanks

# Get the shareCounts and titles and authors and pics of all videos
@app.get("/shareRank/")
async def get_shareRank():
    shareRanks = []
    for bvid in videos_infos:
        shareRanks.append({"bvid": bvid, "shareCounts": videos_infos[bvid]['share'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the share counts 
    shareRanks = sorted(shareRanks, key=lambda x: x['shareCounts'], reverse=True)    
    return shareRanks

#Get the video_sentiment and the video title and author and pic of all videos
@app.get("/sentimentRank/")
async def get_sentimentRank():
    sentimentRanks = []
    for bvid in videos_infos:
        sentimentRanks.append({"bvid": bvid, "sentiment": videos_infos[bvid]['sentiment'], "title": videos_infos[bvid]['title'], "author": videos_infos[bvid]['author'], "pic": videos_infos[bvid]['pic']})
    # Sort the videos by the sentiment 
    sentimentRanks = sorted(sentimentRanks, key=lambda x: x['sentiment'], reverse=True)    
    return sentimentRanks

# Get the danmaku content
@app.get("/danmaku/")
async def get_danmaku(bvid: str):
    if bvid in videos_danmakus:
        return {"danmaku": videos_danmakus[bvid]}
    else:
        return {"danmaku": "Unknown"}

# Get the video comment content
@app.get("/comment/")
async def get_comment(bvid: str):
    if bvid in videos_comments:
        # Sort the comments by the like counts
        videos_comments[bvid] = sorted(videos_comments[bvid], key=lambda x: x['like'], reverse=True)
        return {"comment": videos_comments[bvid]}
    else:
        return {"comment": "Unknown"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__=="__main__":
    uvicorn.run(app)