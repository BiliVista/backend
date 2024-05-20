from fastapi import FastAPI
from api.NewVideo import api_new_video
from api.VideoInfo import api_video
from api.VideosInfo import api_videos 
from api.get_bilibili_data import get_video_data, get_video_comment, get_video_dm
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的源列表
    allow_credentials=True,  # 允许携带 cookies
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 请求头
)

app.include_router(api_video, prefix="/api/video", tags=["VideoInfo"])
app.include_router(api_videos, prefix="/api/videos", tags=["VideosInfo"])
app.include_router(api_new_video, prefix="/api/newvideo", tags=["NewVideo"])

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