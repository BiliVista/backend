from fastapi import APIRouter
from .DataLoader import data_loader

api_video = APIRouter()

@api_video.get("/infos/")
async def get_video_info(bvid: str):
    return data_loader.videos_infos.get(bvid, {"title": "Unknown", "author": "Unknown", "pic": "Unknown", "view": "Unknown", "danmaku": "Unknown", "reply": "Unknown", "favorite": "Unknown", "coin": "Unknown", "share": "Unknown", "like": "Unknown"})

@api_video.get("/attr/{attribute}/")
async def get_video_attribute(bvid: str, attribute: str):
    if attribute in data_loader.videos_infos.get(bvid, {}):
        return {attribute: data_loader.videos_infos[bvid][attribute]}
    return {attribute: "Unknown"}

@api_video.get("/danmu/")
async def get_danmaku(bvid: str):
    return {"danmaku": data_loader.videos_danmakus.get(bvid, "Unknown")}

@api_video.get("/comment/")
async def get_comment(bvid: str):
    if bvid in data_loader.videos_comments:
        data_loader.videos_comments[bvid] = sorted(data_loader.videos_comments[bvid], key=lambda x: x['like'], reverse=True)
        return {"comment": data_loader.videos_comments[bvid]}
    return {"comment": "Unknown"}

@api_video.get("/isRunning/")
async def get_is_running(bvid: str):
    if data_loader.isRunning.get(bvid,False)==True:
        return {"status": "running"}
    return {"status","finish"}