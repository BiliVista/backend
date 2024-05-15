import requests
from bs4 import BeautifulSoup

# Set up the headers to mimic a browser request
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}

def get_video_details(bvid):
    url = f"https://www.bilibili.com/video/{bvid}/"
    respone = requests.get(url, headers=HEADERS)
    # Make the request
    html = respone.content
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Find the <meta> tags for 'description' and 'title'
    meta_description = soup.find("meta", {"name": "description"})
    meta_title = soup.find("meta", {"name": "title"})
    # Extract and print the video details and title
    if meta_description:
        description_content = meta_description['content']
        import re
        details = re.findall(r'\d+', description_content)
        video_details = {
            "播放量": details[0],
            "弹幕量": details[1],
            "点赞数": details[2],
            "投硬币枚数": details[3],
            "收藏人数": details[4],
            "转发人数": details[5],
            "视频作者": description_content.split(", 视频作者 ")[1].split(", ")[0]
        }
    else:
        print("Description meta tag not found")
    if meta_title:
        video_title = meta_title['content']
        # remove "_哔哩哔哩_bilibili"
        video_title = video_title.replace("_哔哩哔哩_bilibili", "")
        # Add the video title to the video details dictionary
        video_details["视频标题"] = video_title
    else:
        print("Title meta tag not found")
    return video_details


if __name__ == "__main__":
    bvid = "BV1SU411Z7xm"
    print(get_video_details(bvid))