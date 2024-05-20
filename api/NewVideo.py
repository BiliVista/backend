from .get_bilibili_data import get_video_data, get_video_comment, get_video_dm
from .DataLoader import data_loader
from fastapi import APIRouter

api_new_video = APIRouter()

@api_new_video.get("/infos/")
async def get_new_video_info(bvid: str):
    # async with data_loader.lock:
        # data_loader.isRunning[bvid] = True
    video_info = get_video_data(bvid) #Use thread to get video data
    # async with data_loader.lock:
        # data_loader.isRunning[bvid] = False
    return video_info

@api_new_video.get("/comments/")
async def get_new_video_comments(bvid: str):
    return await get_video_comment(bvid)

@api_new_video.get("/danmu/")
async def get_new_video_danmakus(bvid: str):
    return await get_video_dm(bvid)