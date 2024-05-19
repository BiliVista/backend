import requests
import qrcode
import re
from time import sleep
import xml.etree.ElementTree as ET
import pandas as pd
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'cookie':"buvid3=157B584A-E63D-0168-7DFA-767E9B9C54C862030infoc; b_nut=1708437762; i-wanna-go-back=-1; b_ut=7; _uuid=A9B5249B-DDF1-CC910-1E2B-E310C6D91A9CA62352infoc; buvid_fp=5acc377b1e17e95839e6c165bf8a1553; enable_web_push=DISABLE; buvid4=7386F889-F4FA-1E4B-F015-C0CACCBFDD1A63132-024022014-Uz5bLrdgm9Lr%2FbmDKGUepg%3D%3D; DedeUserID=74214360; DedeUserID__ckMd5=d0b23f38ca212bbd; rpdid=|(u))l|ml~um0J'u~|)RJ~)mu; header_theme_version=CLOSE; hit-dyn-v2=1; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; LIVE_BUVID=AUTO9117094820993473; is-2022-channel=1; CURRENT_BLACKGAP=0; bp_video_offset_74214360=924741733424562193; fingerprint=7c670eb0db7daf16c7a7ae0436cfe1d1; CURRENT_QUALITY=80; SESSDATA=88653f34%2C1731427373%2Cd3385%2A52CjCg17Wlhr7NpqkSuR_AdyWIMTtL8_AX4tRE8S5wxm0mpCkig-02OJhPiVyiSH1KmmcSVi1jLWI5N1lIell6ZzJaRkdUeHdJMVFSb2FzS2VkTUtsalI3d3RWMTlxSFVUdDZQNjNibjBaTXBzNFVHOW1CRkdMN2N1NFVmMzBrZzhoRTFjUFZmam1RIIEC; bili_jct=c7c54a35738c381536a94edf10a4b778; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; home_feed_column=5; browser_resolution=1512-823; sid=7pipgj59; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYyOTcyODYsImlhdCI6MTcxNjAzODAyNiwicGx0IjotMX0.JdlLe_dd_BnN8kO2j1gifMa6wcpM9dye_698PouxTH4; bili_ticket_expires=1716297226; bp_t_offset_74214360=932925385609314322; PVID=1; b_lsid=974D21043_18F8FEBB300; CURRENT_FNVAL=4048",
}

# Set up the API endpoint
# url = 'https://api.bilibili.com/x/web-interface/view'
url = 'https://api.bilibili.com/x/web-interface/view/detail'

# Define the parameters
params = {
    'bvid': 'BV117411r7R1'
}

def update_headers_with_cookies(HEADERS):
    print("准备扫码登录获取cookies")
    url="https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
    response = requests.get(url, headers=HEADERS)
    qrcode_key=response.json()['data']['qrcode_key']
    qr_url=response.json()['data']['url']
    img=qrcode.make(qr_url)
    img.show()
    pass_url="https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key="+qrcode_key
    response=requests.get(pass_url, headers=HEADERS)
    while response.json()['data']['message']=='未扫码':
        response = requests.get(pass_url, headers=HEADERS)
        print(response.json())
        sleep(3)
    img.close()
    res=response.json()['data']['url']
    match = re.search(r'SESSDATA(.+?)&', res)
    cookies=None
    if match:
        cookies=match.group()
        HEADERS['cookie']=cookies
        return HEADERS
    else:
        print("获取cookies失败")
        return None

def get_video_info(bvid):
    params['bvid'] = bvid
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def filter_video_info(video_info): # Filter the response to get the video informatin
    if video_info:
        data = video_info['data']
        video_info = {}
        video_info['title'] = data['View']['title']
        video_info['pic'] = data['View']['pic']
        video_info['view'] = data['View']['stat']['view']
        video_info['danmaku'] = data['View']['stat']['danmaku']
        video_info['reply'] = data['View']['stat']['reply']
        video_info['favorite'] = data['View']['stat']['favorite']
        video_info['coin'] = data['View']['stat']['coin']
        video_info['share'] = data['View']['stat']['share']
        video_info['like'] = data['View']['stat']['like']
        video_info['author'] = data['View']['owner']['name']
        return video_info
    else:
        return None

def get_video_data(bvid):
    print("开始爬取视频信息") 
    video_info = get_video_info(bvid)
    video_info = filter_video_info(video_info) # Get the video information
    try: 
        with open('data/videos_infos.json') as f: # Read the json file
            videos_infos = json.load(f)
            videos_infos[bvid] = video_info # Add the new video info to the dict
    except:
        videos_infos = {bvid: video_info}
    with open('data/videos_infos.json', 'w') as f: # Write the dict to the json file
        json.dump(videos_infos, f)
    print("视频信息爬取完毕")
    return video_info

# Using thread to get the video comment
def get_video_comment(bid):
    str = f"https://www.bilibili.com/video/{bid}"
    aid_ = f"https://api.bilibili.com/x/web-interface/view?bvid={bid}"
    tmp_data = requests.get(aid_, headers=HEADERS).json()
    aid = tmp_data['data']['aid'] # print(f"正在从{aid_}解析网址aid")
    comment = []
    like = []
    sentiment=[]
    pre_comment_length = 0
    i = 0
    while True:
        url = f"https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={i}" \
            f"&oid={aid}&plat=1&type=1"
        try:
            responses = requests.get(url=url.format(i), headers=HEADERS).json()
            i += 1
            for content in responses["data"]["replies"]:
                comment.append(content["content"]["message"])
                like.append(content['like'])
                sentiment.append(0)
            print("搜集到%d条评论" % (len(comment)))
            if len(comment) == pre_comment_length:
                print("爬虫退出！！！")
                break
            else:
                pre_comment_length = len(comment)
        except Exception as e:
            print(e)
            break
    # Combine the comment and like use dataframe
    comment_like = pd.DataFrame({"comment": comment, "like": like, "sentiment": sentiment})
    try:
        with open('data/videos_comments_res.json') as f:
            comment_like_dict = json.load(f)
            comment_like_dict[bid] = comment_like.to_dict(orient='records') # orient='records' means the dict is like [{column -> value}, ... , {column -> value}]
    except:
        comment_like_dict = {bid: comment_like.to_dict(orient='records')}
    with open('data/videos_comments_res.json', 'w') as f:
        json.dump(comment_like_dict, f)
    print("评论爬取完毕")
    return comment

def get_cid(bvid):
    url="https://api.bilibili.com/x/player/pagelist?bvid="+bvid
    response = requests.get(url, headers=HEADERS)
    return response.json()['data'][0]['cid']

def get_video_dm(bvid):
    cid=get_cid(bvid)
    print("开始爬取弹幕")
    cid = str(cid)
    dm_url = f"https://comment.bilibili.com/{cid}.xml"
    response = requests.get(dm_url, headers=HEADERS)
    danmu=parse_xml(response.content)
    try: # store the danmu to json file which key is bvid
        with open('data/videos_danmus.json') as f:
            danmu_dict = json.load(f)
            danmu_dict[bvid] = danmu
    except:
        danmu_dict = {bvid: danmu}
    with open('data/videos_danmus.json', 'w') as f:
        json.dump(danmu_dict, f)
    print("弹幕爬取完毕")
    return danmu


def parse_xml(xml_text):
    # Parse the xml text and time stamp
    root = ET.fromstring(xml_text)
    danmaku_list = []
    for d in root.findall('d'):
        p_attr = d.get('p')
        text = d.text
        time, type_, font_size, color, timestamp, _, _, _, layer = p_attr.split(',')
        danmaku = {
            'time': float(time),
            'type': int(type_),
            'font_size': int(font_size),
            'color': int(color),
            'timestamp': int(timestamp),
            'layer': int(layer),
            'text': text
        }
        danmaku_list.append(danmaku)
    return danmaku_list

def get_data(bvid):
    return get_video_data(bvid),get_video_comment(bvid),get_video_dm(bvid)

if __name__ == '__main__':
    bvid='BV1ct421u7gu'
    # HEADERS=update_headers_with_cookies(HEADERS)
    video_info,video_comment,video_danmu=get_data(bvid)
