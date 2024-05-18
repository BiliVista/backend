import requests
import qrcode
import re
from time import sleep
import xml.etree.ElementTree as ET
import pandas as pd
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'cookie':"buvid4=F945309E-15D7-20B9-E26B-AD693B6419B120027-022081210-V5ICQHqi6LAgNmQ2DE3bVg%3D%3D; header_theme_version=CLOSE; buvid3=DC77DCDC-CC49-D057-0CA7-86F7D5472C5D44733infoc; b_nut=1693380444; _uuid=64F3D312-BF2E-C1048-54E3-2CD5D107C33EF44395infoc; buvid_fp_plain=undefined; buvid_fp=4aa4d5ca784866ab23c5a0a167f0776a; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; rpdid=|(J~RYuku))k0J'u~uJJRmJY|; CURRENT_QUALITY=116; bp_t_offset_356652086=932057742045085766; fingerprint=636c04d6b54ef85dd030a7b5e6207f0b; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYxMTA3NDgsImlhdCI6MTcxNTg1MTQ4OCwicGx0IjotMX0.H-5h4IVV4fcxwwQOeSKewdn4-BuHJAZoW2qPsfkLzcs; bili_ticket_expires=1716110688; SESSDATA=98463e4c%2C1731403644%2Cf1734%2A51CjCIip3xJ2PJgIJc0wcPrhmkCQkbiPHlUfjUyYj3JUapt_Hj4BD1aNI_nbc21Eo4aGYSVklfTWsySDVPeTBRTE12WndleXpxWld1bi1waXpsbGJwYXhScFdORy1LMzdfYzJKYTFhU0ZUVjBKZU13dmg1Nl9NamVlMTQ2LVZ4VVJpcG5LYkNLTU9RIIEC; bili_jct=c869262e07000a7a2e4642a17ecf23fe; DedeUserID=375458937; DedeUserID__ckMd5=946b0c50e277d569; is-2022-channel=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; PVID=3; b_lsid=5B68F10F4_18F8CFED314; bsource=search_baidu; bp_t_offset_375458937=932945962801823797; home_feed_column=4; browser_resolution=1001-945",
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
        # Put the dict into a new dict
        # video_infos = {
        #     "标题": data['View']['title'],                # title	str	视频标题
        #     "视频图片": data['View']['pic'],               # pic	str	视频封面         
        #     "播放量": data['View']['stat']['view'],         # view num	播放数
        #     "弹幕量": data['View']['stat']['danmaku'],      # danmaku num	弹幕数
        #     "评论数": data['View']['stat']['reply'],        # repl num	评论数	
        #     "收藏人数": data['View']['stat']['favorite'],   # favorit num	收藏数	
        #     "投硬币枚数": data['View']['stat']['coin'],     # coin num	投币数	
        #     "分享数": data['View']['stat']['share'],       # share num	分享数	
        #     "获赞数": data['View']['stat']['like'],        # like	num	获赞数	
        #     "当前排名": data['View']['stat']['now_rank'],   # now_rank	num	当前排名
        #     "历史最高排行": data['View']['stat']['his_rank'], # his_rank	num	历史最高排行
        #     "视频作者": data['View']['owner']['name'],     # name	str	作者名
        #     "视频评分": data['View']['stat']['evaluation']  # evaluation	str	视频评分
        # }
        return video_info
    else:
        return None

def get_video_data(bvid):
    # Get the video information
    print("开始爬取视频信息")
    video_info = get_video_info(bvid)
    video_info = filter_video_info(video_info)
    # print(video_info)
    try: # Read the json file
        with open('videos_infos.json') as f:
            # Add the new video info to the dict
            videos_infos = json.load(f)
            videos_infos[bvid] = video_info
    except:
        videos_infos = {bvid: video_info}
    # Write the dict to the json file
    with open('videos_infos.json', 'w') as f:
        json.dump(videos_infos, f)
    print("视频信息爬取完毕")
    return video_info


def get_video_comment(bid):
    str = f"https://www.bilibili.com/video/{bid}"
    aid_ = f"https://api.bilibili.com/x/web-interface/view?bvid={bid}"
    tmp_data = requests.get(aid_, headers=HEADERS).json()
    # print(f"正在从{aid_}解析网址aid")
    aid = tmp_data['data']['aid']
    comment = []
    like = []
    pre_comment_length = 0
    i = 0
    while True:
        url = f"https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={i}" \
            f"&oid={aid}&plat=1&type=1"
        try:
            responses = requests.get(url=url.format(i), headers=HEADERS).json()
            # print(responses)
            i += 1
            for content in responses["data"]["replies"]:
                comment.append(content["content"]["message"])
                like.append(content['like'])
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
    # Combine the comment and like use dataframe
    comment_like = pd.DataFrame({"comment": comment, "like": like})
    # Export xlsx file
    comment_like.to_excel("comment.xlsx", index=False)
    # store the comment and like to json file which key is bvid
    try:
        with open('comment_like.json') as f:
            comment_like_dict = json.load(f)
            comment_like_dict[bid] = comment_like.to_dict(orient='records') # orient='records' means the dict is like [{column -> value}, ... , {column -> value}]
    except:
        comment_like_dict = {bid: comment_like.to_dict(orient='records')}
    with open('comment_like.json', 'w') as f:
        json.dump(comment_like_dict, f)
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
    #store the danmu to xml file
    # with open('danmu.xml', 'wb') as file:
    #     file.write(response.content)
    danmu=parse_xml(response.content)
    # store the danmu to json file which key is bvid
    try:
        with open('videos_danmus.json') as f:
            danmu_dict = json.load(f)
            danmu_dict[bvid] = danmu
    except:
        danmu_dict = {bvid: danmu}
    with open('videos_danmus.json', 'w') as f:
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
    return get_video_data(bvid),get_video_comment(bvid),get_video_dm(get_cid(bvid))
if __name__ == '__main__':
    bvid='BV1ct421u7gu'
    # HEADERS=update_headers_with_cookies(HEADERS)
    video_info,video_comment,video_danmu=get_data(bvid)
