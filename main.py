# ========= 导入必要模块 ==========
from ncatbot.core import BotClient, GroupMessage, PrivateMessage,Request,Text, At, Image,MessageChain
from ncatbot.utils import get_log

import uuid

import requests
import os
import json
import random
import time

# ========== 创建 BotClient ==========
bot = BotClient()
_log = get_log()



@bot.private_event()
async def on_test(msg: PrivateMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        await bot.api.post_private_msg(msg.user_id, text="NcatBot 测试成功")


mapintro_cd=False
@bot.group_event()
async def on_map(msg:GroupMessage):
    global mapintro_cd

    if msg.raw_message == "随机地图":
        if mapintro_cd:
            return
        mapintro_cd=True
        try:
            res=requests.get('https://s3.game.163.com/7f5ec8225c3ea603/user/mapList?sortType=1&pageNum='+str(random.randint(1,999))+'&pageSize=1')
            if res.status_code!=200:
                await bot.api.post_group_msg(group_id=msg.group_id,text='呃，请求错误：'+str(res.status_code))
                
                return
            info=res.json()
            map1=info['data']['gameMapInfoList'][0]

            response = requests.get(map1['imageUrl'], stream=True, timeout=10)
            filename=str(uuid.uuid4())+'.png'
            
            if response.status_code == 200:
                
                with open('static/'+filename, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

            text='地图名称：'+map1['name']+'\n'+'作者：'+map1['ownerName']+'\n'+'描述：'+map1['intro']+'\n'+'游玩：'+str(map1['playNum'])
            ms=MessageChain([
                Text('看看这个：'),
                Image(r"static/"+filename),
                Text(text)
            ])
            await bot.api.post_group_msg(group_id=msg.group_id,rtf=ms)

        except Exception as e:
            _log.info(str(e))
        finally:
            time.sleep(0.8)
            mapintro_cd=False


@bot.private_event()
async def on_hello(msg:PrivateMessage):
    if msg.raw_message == "你好":
        await bot.api.post_private_msg(msg.user_id, text="谢谢，我很好")


@bot.group_event()
async def on_search_map(msg:GroupMessage):
    command=msg.raw_message.split(' ')
    if len(command)>=2:
        if command[0]=="搜索地图":
            query=command[1]
            try:
                response=requests.get('https://u5pyq.webapp.163.com/apps/u5/web/search_multi?&range=10&page=0&tab=2&sort=0&login_id=143920078&login_token=8e7584ca384f4316bae60293c2b428f4',
                                      params={'keyword':query},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c37)XWEB/14185"}
                                        )
                if response.status_code!=200:
                    await bot.api.post_group_msg(group_id=msg.group_id,text='请求失败，HTTP'+str(response.status_code))
                    return
                data=json.loads(response.content.decode('utf-8'))
                map_code=data['data']['map']['data'][0]
                resp=requests.get('https://u5pyq.webapp.163.com/apps/u5/map/get_map_detail?map_ids='+map_code,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c37)XWEB/14185"},
                                  
                                            )
                if resp.status_code!=200:
                    await bot.api.post_group_msg(group_id=msg.group_id,text='请求失败，HTTP'+str(resp.status_code))
                    return
                data=json.loads(resp.content.decode('utf-8'))
                map1=data['data'][0]
                    
                response = requests.get(map1['image_url'], stream=True, timeout=10)
                filename=str(uuid.uuid4())+'.png'
                # 检查响应状态码
                if response.status_code == 200:
                    # 打开文件并写入内容
                    with open('static/'+filename, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)

                text='地图名称：'+map1['name']+'\n'+'作者：'+map1['owner_nickname']+'\n'+'描述：'+map1['intro']+'\n'+'游玩：'+str(map1['play_num'])+'\n'+'点赞：'+str(map1['like'])
                ms=MessageChain([
                    Text('我找到了：'),
                    Image(r"static/"+filename),
                    Text(text)
                ])
                await bot.api.post_group_msg(group_id=msg.group_id,rtf=ms)

            except Exception as e:
                _log.info(str(e))
            


# ========== 启动 BotClient==========
if __name__ == "__main__":
    
    bot.run(bt_uin="？") # 这里写 Bot 的 QQ 号