# 蛋仔派对地图助手-QQ

基于ncatbot的qq机器人，提供“随机地图”地图推荐功能。
使用wy的api，仅供学习交流使用，api来自蛋仔派对官网网页，未进行逆向破解。

## 安装方法

1. 安装napcat CLI
   [NapcatQQ](https://github.com/NapNeko/NapCatQQ "Github")
   以及配置qq账号，登录账号等操作（main.py最下面换成机器人qq号）

2. 安装python库
   ```bash
   pip install -r requirements.txt
   ```

3. 运行python
   ```bash
   python main.py
   ```


## 使用方法
在包含机器人的群聊里发送“随机地图”即可
私信“你好”测试机器人在线


## 追加服务
通过“搜索地图 关键字”进行指定地图信息展示。该部分使用wx小程序蛋壳api，因此需要特殊凭证。
配置源代码LOGINID与LOGINTOKEN，即可使用功能（虽然除了抓包之外我找不到一般用户如何获取自己的这个凭证）
仍然是学习目的开发，无盈利，若有侵权联系删除。