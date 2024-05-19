# Backend

## Base on FastAPI

### API

#### Get video info

api_video from VideoInfo.py

**API** Include

- Single Video's All information 单个视频的所有信息

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| infos    | 视频信息     | `/video/infos/?bvid=<bvid>`           |

- Single Video's Comment 单个视频的评论

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| comment    | 视频评论      | `/video/comment/?bvid=<bvid>`           |

- Single Video's danmakus 单个视频的弹幕

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| danmaku   | 视频评论      | `/video/danmu/?bvid=<bvid>`           |

- Whether the basic information of a single video is being crawled  单个视频的基本信息是否正在爬取

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| isRunning  | 视频评论      | `/video/isRunning/?bvid=<bvid>`           |

- Single Video's basic information 单个视频的基本信息

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| title     | 视频标题      | `/video/title/?bvid=<bvid>`           |
| pic       | 视频封面      | `/video/pic/?bvid=<bvid>`             |
| view      | 视频播放量    | `/video/view/?bvid=<bvid>`            |
| danmaku   | 视频弹幕量    | `/video/danmaku/?bvid=<bvid>`         |
| reply     | 视频评论量    | `/video/reply/?bvid=<bvid>`           |
| favorite  | 视频收藏量    | `/video/favorite/?bvid=<bvid>`        |
| coin      | 视频投币量    | `/video/coin/?bvid=<bvid>`            |
| share     | 视频转发量    | `/video/share/?bvid=<bvid>`           |
| like      | 视频点赞量    | `/video/like/?bvid=<bvid>`            |
| author    | 视频作者      | `/video/author/?bvid=<bvid>`         |

#### Get videos info

api_videos from VideosInfo.py

- All Videos' Basic Information 所有视频信息

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| videos infos |  所有视频信息     | `/videos/infos/?bvid=<bvid>`           |

- All Videos' `like`, `share`, `coin`, `view`, `favoriate` Counts Rank 点赞、投币、转发、收藏、播放量排行榜

|Property|Description|API|
| view      | 视频播放量排行榜  | `/videos/view/rank/`            |
| reply     | 视频评论量排行榜   | `/videos/reply/rank/`           |
| favorite  | 视频收藏量排行榜   | `/videos/favorite/rank/`        |
| coin      | 视频投币量排行榜   | `/videos/coin/rank/`            |
| share     | 视频转发量排行榜   | `/videos/share/rank/`           |
| like      | 视频点赞量排行榜   | `/videos/like/rank/`            |

- Videos' Sentiment Rank 好评率排行榜
|Property|Description|API|
| view      | 视频播放量排行榜  | `/videos/sentiment/rank/`            |

- Whether the basic information of videos are being crawled  是否存在一个视频的基本信息是否正在爬取

| Property  | Description   | API                                  |
|-----------|---------------|-------------------------------------|
| anyRunning  | 视频评论      | `/videos/anyRunning/`|

#### Add New Video to Analysis

api_new_video from NewVideo.py
