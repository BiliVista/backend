from fastapi import FastAPI
from api.NewVideo import api_new_video
from api.VideoInfo import api_video
from api.VideosInfo import api_videos 
from api.get_bilibili_data import get_video_data, get_video_comment, get_video_dm
import uvicorn

# Create FastAPI instance
app = FastAPI()

app.include_router(api_video, prefix="/video", tags=["VideoInfo"])
app.include_router(api_videos, prefix="/videos", tags=["VideosInfo"])
app.include_router(api_new_video, prefix="/newvideo", tags=["NewVideo"])

# Router
@app.get("/")
async def root():
    return {"message": "Hello FastAPI World!"}

# Start server
if __name__ == "__main__":
    uvicorn.run(app)
    # bvid="BV18w4m1Q7GG"
    # get_video_data(bvid)
    # get_video_comment(bvid)
    # get_video_dm(bvid)