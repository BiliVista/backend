from fastapi import APIRouter
from .DataLoader import videos_infos, videos_comments, videos_danmakus
api_video = APIRouter()

isRunning = {}

@api_video.get("/infos/")
async def get_video_info(bvid: str):
    return videos_infos.get(bvid, {"title": "Unknown", "author": "Unknown", "pic": "Unknown", "view": "Unknown", "danmaku": "Unknown", "reply": "Unknown", "favorite": "Unknown", "coin": "Unknown", "share": "Unknown", "like": "Unknown"})

@api_video.get("/{attribute}/")
async def get_video_attribute(bvid: str, attribute: str):
    if attribute in videos_infos.get(bvid, {}):
        return {attribute: videos_infos[bvid][attribute]}
    return {attribute: "Unknown"}

@api_video.get("/danmu/")
async def get_danmaku(bvid: str):
    return {"danmaku": videos_danmakus.get(bvid, "Unknown")}

@api_video.get("/comment/")
async def get_comment(bvid: str):
    if bvid in videos_comments:
        videos_comments[bvid] = sorted(videos_comments[bvid], key=lambda x: x['like'], reverse=True)
        return {"comment": videos_comments[bvid]}
    return {"comment": "Unknown"}

@api_video.get("/isRunning/")
async def get_is_running(bvid: str):
    return {"status": "running" if isRunning.get(bvid) else "finish"}