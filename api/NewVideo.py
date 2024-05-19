from .get_bilibili_data import get_video_data, get_video_comment, get_video_dm
from fastapi import APIRouter

api_new_video = APIRouter()

isRunning = {}

@api_new_video.get("/infos/") #/newvideo/infos/
async def get_new_video_info(bvid: str):
    isRunning[bvid] = True
    video_info = get_video_data(bvid)
    isRunning[bvid] = False
    return video_info

@api_new_video.get("/comments/")
async def get_new_video_comments(bvid: str):
    return get_video_comment(bvid)

@api_new_video.get("/danmu/")
async def get_new_video_danmakus(bvid: str):
    return get_video_dm(bvid)
