import requests
import qrcode
import re
from time import sleep
import xml.etree.ElementTree as ET

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'cookie':"buvid3=157B584A-E63D-0168-7DFA-767E9B9C54C862030infoc; b_nut=1708437762; i-wanna-go-back=-1; b_ut=7; _uuid=A9B5249B-DDF1-CC910-1E2B-E310C6D91A9CA62352infoc; buvid_fp=5acc377b1e17e95839e6c165bf8a1553; enable_web_push=DISABLE; buvid4=7386F889-F4FA-1E4B-F015-C0CACCBFDD1A63132-024022014-Uz5bLrdgm9Lr%2FbmDKGUepg%3D%3D; DedeUserID=74214360; DedeUserID__ckMd5=d0b23f38ca212bbd; rpdid=|(u))l|ml~um0J'u~|)RJ~)mu; header_theme_version=CLOSE; hit-dyn-v2=1; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; LIVE_BUVID=AUTO9117094820993473; home_feed_column=5; is-2022-channel=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; bp_video_offset_74214360=924741733424562193; fingerprint=7c670eb0db7daf16c7a7ae0436cfe1d1; browser_resolution=1512-823; CURRENT_QUALITY=80; SESSDATA=1a7fa502%2C1731167233%2C4cae8%2A52CjCTNN-vaEjTnK05NyZZkobNWv_us8W0xKj-7zSPS8nd4pNuZOmpprPNgyGYcum1BJwSVjJ3aVdfVXBDZldLWVZOZzl1OVRUc0VxbnhHZUQwWklSX21IY0Q3Y2VzZ1lTV01OUmx5S1FhWjFtcTZ3WVRsUk9pMENlX1FKYnZCYi1weTVGR3duVllRIIEC; bili_jct=10152f9f167ba3a986cd75523232a176; sid=4p1842mc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYwMzczNzIsImlhdCI6MTcxNTc3ODExMiwicGx0IjotMX0.5Eyk7aO3FxqroW5EQ6LQ0FIDx-OTCU8UAcvK83zkECU; bili_ticket_expires=1716037312; PVID=2; bp_t_offset_74214360=931793198082162743; b_lsid=CBF1083DB_18F7D4EC04A"
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

    # 扫码成功后关闭弹窗
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

# Filter the response to get the video information
def filter_video_info(video_info):
    if video_info:
        data = video_info['data']
        video_infos = {
            "标题": data['View']['title'],                # title	str	视频标题
            "视频图片": data['View']['pic'],               # pic	str	视频封面         
            "播放量": data['View']['stat']['view'],         # view num	播放数
            "弹幕量": data['View']['stat']['danmaku'],      # danmaku num	弹幕数
            "评论数": data['View']['stat']['reply'],        # repl num	评论数	
            "收藏人数": data['View']['stat']['favorite'],   # favorit num	收藏数	
            "投硬币枚数": data['View']['stat']['coin'],     # coin num	投币数	
            "分享数": data['View']['stat']['share'],       # share num	分享数	
            "获赞数": data['View']['stat']['like'],        # like	num	获赞数	
            "当前排名": data['View']['stat']['now_rank'],   # now_rank	num	当前排名
            "历史最高排行": data['View']['stat']['his_rank'], # his_rank	num	历史最高排行
            "视频作者": data['View']['owner']['name'],     # name	str	作者名
            "视频评分": data['View']['stat']['evaluation']  # evaluation	str	视频评分
        }
        return video_infos
    else:
        return None 

def get_video_data(bvid):
    # Get the video information
    print("开始爬取视频信息")
    video_info = get_video_info(bvid)
    video_infos = filter_video_info(video_info)
    print("视频信息爬取完毕")
    # export the video information to a file
    with open("video_info.txt", "w", encoding="utf-8") as fp:
        for key, value in video_infos.items():
            fp.write(key + ": " + str(value) + "\n")
    return video_infos


def get_video_comment(bid):
    str = f"https://www.bilibili.com/video/{bid}"
    aid_ = f"https://api.bilibili.com/x/web-interface/view?bvid={bid}"
    tmp_data = requests.get(aid_, headers=HEADERS).json()
    # print(f"正在从{aid_}解析网址aid")
    aid = tmp_data['data']['aid']
    comment = []
    pre_comment_length = 0
    i=0
    print("开始爬取评论")
    while True:
        url = f"https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={i}" \
            f"&oid={aid}&plat=1&type=1"
        try:
            responses = requests.get(url=url.format(i), headers=HEADERS).json()
            i+=1
            for content in responses["data"]["replies"]:
                comment.append(content["content"]["message"])
            print("搜集到%d条评论" % (len(comment)))
            # 调整爬虫策略，从必须每20条评论调整成上一次评论数和这一次评论数进行比较，如果有改变说明有新数据，如果没改变说明数据全部搜集完毕，爬虫停止
            if len(comment) == pre_comment_length:
                print("爬虫退出！！！")
                break
            else:
                pre_comment_length = len(comment)
        except Exception as e:
            print(e)
            break
    with open("comment.txt", "w", encoding="utf-8") as fp:
        for c in comment:
            fp.write(c + "\n")
    print("评论爬取完毕")
    return comment

def get_cid(bvid):
    url="https://api.bilibili.com/x/player/pagelist?bvid="+bvid
    response = requests.get(url, headers=HEADERS)
    return response.json()['data'][0]['cid']

def get_video_dm(cid):
    print("开始爬取弹幕")
    cid = str(cid)
    dm_url = f"https://comment.bilibili.com/{cid}.xml"
    response = requests.get(dm_url, headers=HEADERS)
    danmu=parse_xml(response.content)
    print("弹幕爬取完毕")
    return danmu 

def parse_xml(xml_text):
    root = ET.fromstring(xml_text)
    danmu=[]
    with open('danmu.txt', 'w', encoding='utf-8') as file:
        for d in root.findall('d'):
            file.write(d.text + '\n')
            danmu.append(d.text)
    return danmu

def get_data(bvid):
    return get_video_data(bvid),get_video_comment(bvid),get_video_dm(get_cid(bvid))

if __name__ == '__main__':
    # bvid = 'BV1Jh411Y7f6'
    bvid = 'BV117411r7R1'
    video_info,video_comment,video_danmu=get_data(bvid)
