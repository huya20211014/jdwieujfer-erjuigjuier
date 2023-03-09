#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  : 2023/02/11 修改接口
-------------------------------------------------
'''
import logging
import re
import traceback

import requests
import json
import time
import os
import copy

from TikTokUtils import Utils
from TikTokUrls import Urls
from TikTokResult import Result


class TikTok(object):

    def __init__(self):
        self.urls = Urls()
        self.utils = Utils()
        self.result = Result()
        self.log = self.utils.getlogger()
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        #     'referer': 'https://www.douyin.com/',
        #     'Cookie': f"msToken={self.utils.generate_random_str(107)};odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9"
        # }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.douyin.com/',
            'Cookie': f"msToken={self.utils.generate_random_str(107)};odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9"
        }
        # s_v_web_id=verify_leq1wke9_nJlb0kQZ_sfg7_4PjJ_9vjr_cWNs0CQ8WYcd;
        cookies = {
            'sessionid_ss': '5a3a9c8563dbeccbb9014db8ce9a675e',
        }

        headers = {
            'authority': 'www.douyin.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bd-ticket-guard-client-cert': 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNGRENDQWJxZ0F3SUJBZ0lVSWVWdTdEelBLd043dEhSK0Z6T3N3b09vc2hvd0NnWUlLb1pJemowRUF3SXcKTVRFTE1Ba0dBMVVFQmhNQ1EwNHhJakFnQmdOVkJBTU1HWFJwWTJ0bGRGOW5kV0Z5WkY5allWOWxZMlJ6WVY4eQpOVFl3SGhjTk1qSXhNakkwTURneE56RTRXaGNOTXpJeE1qSTBNVFl4TnpFNFdqQW5NUXN3Q1FZRFZRUUdFd0pEClRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMEQKQVFjRFFnQUVReVQ3U0w1RkUyU0lJdmpYWWZRSzdvbzlzZlNzU0dEWFFtRURqVHg2SFoxYngrM3dUTTRHMnRmcApBYS8xTXdzVEV5dzdzMzhkeGhVaVBSRVJ0NDFyV0tPQnVUQ0J0akFPQmdOVkhROEJBZjhFQkFNQ0JhQXdNUVlEClZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXcKS1FZRFZSME9CQ0lFSUg0Z3hGZFRKd05TdHpZeC9jTk9CSVBQUG52N0dXRWpDR0ZJU3FhWFl0SjNNQ3NHQTFVZApJd1FrTUNLQUlES2xaK3FPWkVnU2pjeE9UVUI3Y3hTYlIyMVRlcVRSZ05kNWxKZDdJa2VETUJrR0ExVWRFUVFTCk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGdBTUVVQ0lRQ2tySDd3WWFsY0lLNjcKRUhYZGpya0xxa2Qrb1B6WjBsa1lsUHFBNU5vRmhnSWdJS3c0dGE5SFJTc0xFd1kzWkhUQm9GOVVTUTNGY29oMAppc3BBTFdDcGd6VT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=',
            'bd-ticket-guard-version': '2',
            # 'cookie': 'xgplayer_user_id=127433142266; d_ticket=687002b130aebc2c765d4d585ce9dccc34880; n_mh=2awS99UZxOYCYMo9gqgsAxEu-NVaJYeU5MIm8TrCZRY; passport_assist_user=CkEdZhs9Exqlbjr1x2FWd8xPTRi7MoKCHPO6-DbDnUohFD684OjDs1eqioZXY4AcVYZ1VtzKbnI96yqlwFWtx7_WGhpICjzs42VP7ulFaqVxKQxyCQuhl9VRumoBxk0Y8dUR9oMCt2F8dJmQZ9Q4tNscrcmGywpCu8G3WD5scPF0wCkQ4tikDRiJr9ZUIgED2pEOZw%3D%3D; sso_uid_tt=270676b34399fbff50c3fdaf033fc2c6; sso_uid_tt_ss=270676b34399fbff50c3fdaf033fc2c6; toutiao_sso_user=adec5c4429c05b858819ea01845c8725; toutiao_sso_user_ss=adec5c4429c05b858819ea01845c8725; uid_tt=3846eb60ac9d17a6165a6f764235b50e; uid_tt_ss=3846eb60ac9d17a6165a6f764235b50e; sid_tt=5a3a9c8563dbeccbb9014db8ce9a675e; sessionid=5a3a9c8563dbeccbb9014db8ce9a675e; sessionid_ss=5a3a9c8563dbeccbb9014db8ce9a675e; LOGIN_STATUS=1; sid_ucp_sso_v1=1.0.0-KDFlN2EyOGE0NDk3ZjJjMjUxN2UxZDZjNzNlOTdhZDc4ZGMyY2U1M2QKHwjcpbDY6vS3AhCZgI6fBhjvMSAMMJqBq_sFOAZA9AcaAmxmIiBhZGVjNWM0NDI5YzA1Yjg1ODgxOWVhMDE4NDVjODcyNQ; ssid_ucp_sso_v1=1.0.0-KDFlN2EyOGE0NDk3ZjJjMjUxN2UxZDZjNzNlOTdhZDc4ZGMyY2U1M2QKHwjcpbDY6vS3AhCZgI6fBhjvMSAMMJqBq_sFOAZA9AcaAmxmIiBhZGVjNWM0NDI5YzA1Yjg1ODgxOWVhMDE4NDVjODcyNQ; sid_guard=5a3a9c8563dbeccbb9014db8ce9a675e%7C1675853849%7C5184000%7CSun%2C+09-Apr-2023+10%3A57%3A29+GMT; sid_ucp_v1=1.0.0-KGUxZTdiNzNlZTUzMmQwNGI4MTc2Y2QxNTU1OGVlNWNiNDk1YjUxZjYKGQjcpbDY6vS3AhCZgI6fBhjvMSAMOAZA9AcaAmxmIiA1YTNhOWM4NTYzZGJlY2NiYjkwMTRkYjhjZTlhNjc1ZQ; ssid_ucp_v1=1.0.0-KGUxZTdiNzNlZTUzMmQwNGI4MTc2Y2QxNTU1OGVlNWNiNDk1YjUxZjYKGQjcpbDY6vS3AhCZgI6fBhjvMSAMOAZA9AcaAmxmIiA1YTNhOWM4NTYzZGJlY2NiYjkwMTRkYjhjZTlhNjc1ZQ; s_v_web_id=verify_ldwxus9u_gFxfkxiV_xHf5_4ZEE_BwjS_JbB1AEVkB1YT; store-region=cn-gs; store-region-src=uid; odin_tt=f9c595402159f59fc140bc32bc9d99cb1ef35d5bfd882a1429a4c002dd7e54c7c7f09d67f35cfb63f392a4b9d461d7967655d7d402c38402149016ad72f88910; ttwid=1%7Cv70bMg0H26eflXmeq7YexUhnTLwoWLJClBtqIYPqZE8%7C1676858408%7C71726a79d13e45bf6f9bdfbe3dc179d496f386b4fb80fe0a34ceb41997bf40a3; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jZXJ0IjoiLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tXG5NSUlDRkRDQ0FicWdBd0lCQWdJVUllVnU3RHpQS3dON3RIUitGek9zd29Pb3Nob3dDZ1lJS29aSXpqMEVBd0l3XG5NVEVMTUFrR0ExVUVCaE1DUTA0eElqQWdCZ05WQkFNTUdYUnBZMnRsZEY5bmRXRnlaRjlqWVY5bFkyUnpZVjh5XG5OVFl3SGhjTk1qSXhNakkwTURneE56RTRXaGNOTXpJeE1qSTBNVFl4TnpFNFdqQW5NUXN3Q1FZRFZRUUdFd0pEXG5UakVZTUJZR0ExVUVBd3dQWW1SZmRHbGphMlYwWDJkMVlYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEXG5BUWNEUWdBRVF5VDdTTDVGRTJTSUl2alhZZlFLN29vOXNmU3NTR0RYUW1FRGpUeDZIWjFieCszd1RNNEcydGZwXG5BYS8xTXdzVEV5dzdzMzhkeGhVaVBSRVJ0NDFyV0tPQnVUQ0J0akFPQmdOVkhROEJBZjhFQkFNQ0JhQXdNUVlEXG5WUjBsQkNvd0tBWUlLd1lCQlFVSEF3RUdDQ3NHQVFVRkJ3TUNCZ2dyQmdFRkJRY0RBd1lJS3dZQkJRVUhBd1F3XG5LUVlEVlIwT0JDSUVJSDRneEZkVEp3TlN0ell4L2NOT0JJUFBQbnY3R1dFakNHRklTcWFYWXRKM01Dc0dBMVVkXG5Jd1FrTUNLQUlES2xaK3FPWkVnU2pjeE9UVUI3Y3hTYlIyMVRlcVRSZ05kNWxKZDdJa2VETUJrR0ExVWRFUVFTXG5NQkNDRG5kM2R5NWtiM1Y1YVc0dVkyOXRNQW9HQ0NxR1NNNDlCQU1DQTBnQU1FVUNJUUNrckg3d1lhbGNJSzY3XG5FSFhkanJrTHFrZCtvUHpaMGxrWWxQcUE1Tm9GaGdJZ0lLdzR0YTlIUlNzTEV3WTNaSFRCb0Y5VVNRM0Zjb2gwXG5pc3BBTFdDcGd6VT1cbi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS1cbiJ9; passport_csrf_token=0e4bfb634d63725d327560a64da6e0e1; passport_csrf_token_default=0e4bfb634d63725d327560a64da6e0e1; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%223%2F20230227%22; csrf_session_id=6e62d5254fe5c137f6ba05d0cdcf9650; live_can_add_dy_2_desktop=%220%22; __ac_nonce=063fe5b1200d7e320f58c; __ac_signature=_02B4Z6wo00f018qggfAAAIDDSqJ7sAKCcW.KhIVAAJFfsoasZoZOjs-CNjbKzO8.WI120qfrMzNww2yCYJpU.uj.801SE963J62.nUanm3MZnq6lYnEdDAJ4Sctp8Esi5.79u.mjv4Mm6wJte6; strategyABtestKey=%221677613864.092%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAIpvieueUTPWlnUPC4BAnBlDORKstHlr4XgjX1hBFlgtwYNfiFDF3aDsIzLCbwanI%2F1677686400000%2F0%2F0%2F1677614614627%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAIpvieueUTPWlnUPC4BAnBlDORKstHlr4XgjX1hBFlgtwYNfiFDF3aDsIzLCbwanI%2F1677686400000%2F0%2F1677614014628%2F0%22; passport_fe_beating_status=true; msToken=SgMiW8kRDdy41uYmnphzTFKu0LqtFkHK-nFLqJXI419bIJhsRc6KGW2fnYXxyXNxa8ooHGoyQ9giqpiXIKcvq_HJ1Dj4t__71Bst9db7Hb-kA5-5oRMmgMdI1dtphRuY; msToken=hragVqPGcpzl6krng9-JDz9VfzWhb7fNmcBPR7lt5Mxz0l_UyM4oIuiG6V27aqqJaCyFf12d7ripca31QtUqvKE39aemAijPniOUjSXR4wt5-M0-wxgcFET88jf2W_hf; home_can_add_dy_2_desktop=%221%22; tt_scid=ejPdCqLYnC.Vv5QeBz-pCdG6G4SymyCOQWACMRSQ1hgRC5ys2qjzppr-5wf3x3aDfbe4',
            'dnt': '1',
            'referer': 'https://www.douyin.com/user/MS4wLjABAAAA6lBPnv8OehGLn_vgi4DamLybmXtJ2ARonH4xgIgP5Pg',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }

    # 从分享链接中提取网址
    def getShareLink(self, string):
        # findall() 查找匹配正则表达式的字符串
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)[0]

    # 得到 作品id 或者 用户id
    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    def getKey(self, url):
        key = None
        key_type = None

        try:
            r = requests.get(url=url, headers=self.headers, timeout=10)
        except Exception as e:
            # print('[  错误  ]:输入链接有误！\r')
            self.log.exception('[  错误  ]:输入链接有误！')
            return key_type, key

        # 抖音把图集更新为note
        # 作品 第一步解析出来的链接是share/video/{aweme_id}
        # https://www.iesdouyin.com/share/video/7037827546599263488/?region=CN&mid=6939809470193126152&u_code=j8a5173b&did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&titleType=title&schema_type=37&from_ssr=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 用户 第一步解析出来的链接是share/user/{sec_uid}
        # https://www.iesdouyin.com/share/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek?did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&sec_uid=MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek&from_ssr=1&u_code=j8a5173b&timestamp=1674540164&ecom_share_track_params=%7B%22is_ec_shopping%22%3A%221%22%2C%22secuid%22%3A%22MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw%22%2C%22enter_from%22%3A%22others_homepage%22%2C%22share_previous_page%22%3A%22others_homepage%22%7D&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 合集
        # https://www.douyin.com/collection/7093490319085307918
        urlstr = str(r.request.path_url)

        if "/share/user/" in urlstr:
            # 获取用户 sec_uid
            if '?' in r.request.path_url:
                for one in re.finditer(r'user\/([\d\D]*)([?])', str(r.request.path_url)):
                    key = one.group(1)
            else:
                for one in re.finditer(r'user\/([\d\D]*)', str(r.request.path_url)):
                    key = one.group(1)
            key_type = "user"
        elif "/share/video/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('video/(\d+)?', urlstr)[0]
            key_type = "aweme"
        elif "/collection/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('collection/(\d+)?', urlstr)[0]
            key_type = "mix"
        elif "live.douyin.com" in r.url:
            key = r.url.replace('https://live.douyin.com/', '')
            key_type = "live"

        if key is None or key_type is None:
            self.log.exception('[  错误  ]:输入链接有误！无法获取 id')
            # print('[  错误  ]:输入链接有误！无法获取 id\r')
            return key_type, key

        return key_type, key

    # 传入 aweme_id
    # 返回 数据 字典
    def getAwemeInfo(self, aweme_id):
        # print('[  提示  ]:正在请求的作品 id = %s\r' % aweme_id)
        self.log.info('[  提示  ]:正在请求的作品 id = %s\r' % aweme_id)
        if aweme_id is None:
            return None

        while True:
            # 接口不稳定, 有时服务器不返回数据, 需要重新获取
            try:
                Xbogus = self.utils.getXbogus(
                    url=f'aweme_id={aweme_id}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333')
                jx_url = self.urls.POST_DETAIL + Xbogus
                raw = requests.get(url=jx_url, headers=self.headers, timeout=10).text

                datadict = json.loads(raw)
                if datadict is not None and datadict['aweme_detail'] is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:

                self.log.exception("[  警告  ]:接口未返回数据, 正在重新请求!")
                # self.log.error('{}'.format(raw))
                # self.utils.sleep_dis(2)
                # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

        # 清空self.awemeDict
        self.result.clearDict(self.result.awemeDict)

        # 默认为视频
        awemeType = 0
        try:
            # datadict['aweme_detail']["images"] 不为 None 说明是图集
            if datadict['aweme_detail']["images"] is not None:
                awemeType = 1
        except Exception as e:
            self.log.exception("[  警告  ]:接口中未找到 images")
            # print("[  警告  ]:接口中未找到 images\r")

        # 转换成我们自己的格式
        self.result.dataConvert(awemeType, self.result.awemeDict, datadict['aweme_detail'])

        return self.result.awemeDict, datadict

    def getJustUserInfo(self, sec_uid, mode="post", count=35):
        self.log.info('[  提示  ]:正在获取信息的用户 id = %s' % sec_uid)
        # print('[  提示  ]:正在获取信息的用户 id = %s' % sec_uid)
        if sec_uid is None:
            return None

        max_cursor = 0
        awemeList = []
        self.log.info("[  提示  ]:正在获取作者信息请稍后...")
        # print("[  提示  ]:正在获取作者信息请稍后...")
        # print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            self.log.info("[  提示  ]:正在对 [作者信息] 进行第 " + str(times) + " 次请求...")

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = self.urls.USER_DETAIL + self.utils.getXbogus(
                        url=f'device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&source=channel_pc_web&sec_user_id={sec_uid}&pc_client_type=1&version_code=170400&version_name=17.4.0'
                    )
                    res = requests.get(url=url, headers=self.headers, timeout=10)
                    # print(res.text)
                    datadict = json.loads(res.text)
                    if datadict is not None and datadict["status_code"] == 0:
                        break



                except Exception as e:
                    self.log.error("[  警告  ]:接口未返回数据, 正在重新请求!")
                    # traceback.print_exc()
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")
            # print(datadict)

            user_info = {}
            aweme_list = datadict["user"]
            if 'special_state_info' in aweme_list:
                special_state_info = aweme_list['special_state_info']
                self.log.error('{}'.format(special_state_info))

                return -1
            # JSON.user.punish_remind_info.punish_title
            if 'punish_remind_info' in aweme_list:
                punish_remind_info = aweme_list['punish_remind_info']
                if 'punish_title' in punish_remind_info:
                    punish_title = punish_remind_info['punish_title']
                    if '封禁' in punish_title:
                        self.log.error('{}'.format(punish_title))
                        return -1
            # JSON.user.avatar_larger.url_list
            if len(aweme_list) == 0:
                self.log.error('{} 没有作品'.format(sec_uid))
                # print('{} 没有作品'.format(sec_uid))
            else:
                self.log.debug('short_id:{}\nunique_id:{}'.format(aweme_list['short_id'],aweme_list['unique_id']))
                unique_id = aweme_list['short_id']
                if '{}'.format(aweme_list['short_id']) == '0':
                    unique_id = aweme_list['unique_id']
                user_info['nickname'] = aweme_list['nickname']
                user_info['sec_uid'] = aweme_list['sec_uid']
                user_info['uid'] = aweme_list['uid']
                user_info['unique_id'] = unique_id
                user_info['aweme_count'] = aweme_list['aweme_count']
                user_info['total_favorited'] = aweme_list['total_favorited']
                user_info['follower_count'] = aweme_list['follower_count']
                user_info['following_count'] = aweme_list['following_count']
                user_info['total_favorited'] = aweme_list['total_favorited']
                user_info['avatar'] = aweme_list['avatar_larger']['url_list'][0]
                user_info['signature'] = aweme_list['signature']
            return user_info

    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    # mode : post | like 模式选择 like为用户点赞 post为用户发布
    def getUserInfo(self, sec_uid, mode="post", count=35, max_count=-1):
        self.log.info('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        # print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None

        max_cursor = 0
        awemeList = []
        self.log.info("[  提示  ]:正在获取所有作品数据请稍后...")
        self.log.info("[  提示  ]:会进行多次请求，等待时间较长...")
        # print("[  提示  ]:正在获取所有作品数据请稍后...\r")
        # print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:

            times = times + 1
            self.log.info("[  提示  ]:正在对 [主页] 进行第 " + str(times) + " 次请求...")

            trytime = 0
            trymax = 10
            url = self.urls.USER_POST + self.utils.getXbogus(
                url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}')
            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    trytime += 1
                    res = requests.get(url=url, headers=self.headers, timeout=10)
                    print(res.text)
                    datadict = json.loads(res.text)
                    self.log.info('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据')
                    self.log.info('[  提示  ]:开始对 ' + str(len(datadict["aweme_list"])) + ' 条数据请求作品详情')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    # print(res.text)
                    self.log.error("{}-{} [  警告  ]:接口未返回数据, 正在重新请求!".format(trytime, sec_uid))
                    # self.log.error('{}'.format(res.text))
                    # if trytime >= trymax:
                    #     return []
                    # self.utils.sleep_dis(2)
                    # traceback.print_exc()
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 获取 aweme_id
                aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                datanew, dataraw = self.getAwemeInfo(aweme_id)
                awemeList.append(copy.deepcopy(datanew))

            # 更新 max_cursor
            max_cursor = datadict["max_cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                self.log.info("[  提示  ]: [主页] 下所有作品数据获取完成...")
                # print("\r\n[  提示  ]: [主页] 下所有作品数据获取完成...\r\n")
                break
            elif max_count != -1 and len(awemeList) >= max_count:
                self.log.info("[  提示  ]: [主页] 下所有作品数据达到最大限制值 {} ...".format(max_count))
                break
            else:
                self.log.info("[  提示  ]:[主页] 第 " + str(times) + " 次请求成功...")
                # print("\r\n[  提示  ]:[主页] 第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getLiveInfo(self, web_rid: str):
        print('[  提示  ]:正在请求的直播间 id = %s\r\n' % web_rid)

        # web_rid = live_url.replace('https://live.douyin.com/', '')

        try:
            live_api = self.urls.LIVE + self.utils.getXbogus(
                url=f'aid=6383&device_platform=web&web_rid={web_rid}')
            response = requests.get(live_api, headers=self.headers, timeout=10)
            live_json = json.loads(response.text)
        except Exception as e:
            print("[  错误  ]:接口未返回数据, 请检查后重新运行!\r")
            return None

        if live_json == {} or live_json['status_code'] != 0:
            print("[  错误  ]:接口未返回信息\r")
            return None

        # 清空字典
        self.result.clearDict(self.result.liveDict)

        # 是否在播
        self.result.liveDict["status"] = live_json['data']['data'][0]['status']

        if self.result.liveDict["status"] == 4:
            print('[   📺   ]:当前直播已结束，正在退出')
            return self.result.liveDict

        # 直播标题
        self.result.liveDict["title"] = live_json['data']['data'][0]['title']

        # 观看人数
        self.result.liveDict["user_count"] = live_json['data']['data'][0]['user_count_str']

        # 昵称
        self.result.liveDict["nickname"] = live_json['data']['data'][0]['owner']['nickname']

        # sec_uid
        self.result.liveDict["sec_uid"] = live_json['data']['data'][0]['owner']['sec_uid']

        # 直播间观看状态
        self.result.liveDict["display_long"] = live_json['data']['data'][0]['room_view_stats']['display_long']

        # 推流
        self.result.liveDict["flv_pull_url"] = live_json['data']['data'][0]['stream_url']['flv_pull_url']

        try:
            # 分区
            self.result.liveDict["partition"] = live_json['data']['partition_road_map']['partition']['title']
            self.result.liveDict["sub_partition"] = \
                live_json['data']['partition_road_map']['sub_partition']['partition'][
                    'title']
        except Exception as e:
            self.result.liveDict["partition"] = '无'
            self.result.liveDict["sub_partition"] = '无'

        info = '[   💻   ]:直播间：%s  当前%s  主播：%s 分区：%s-%s\r' % (
            self.result.liveDict["title"], self.result.liveDict["display_long"], self.result.liveDict["nickname"],
            self.result.liveDict["partition"], self.result.liveDict["sub_partition"])
        print(info)

        flv = []
        print('[   🎦   ]:直播间清晰度')
        for i, f in enumerate(self.result.liveDict["flv_pull_url"].keys()):
            print('[   %s   ]: %s' % (i, f))
            flv.append(f)

        # rate = int(input('[   🎬   ]输入数字选择推流清晰度：'))
        rate = 0

        # 显示清晰度列表
        print('[   %s   ]:%s' % (flv[rate], self.result.liveDict["flv_pull_url"][flv[rate]]))

        print('[   📺   ]:复制链接使用下载工具下载')
        return self.result.liveDict

    def getMixInfo(self, mix_id: str, count=35):
        print('[  提示  ]:正在请求的合集 id = %s\r\n' % mix_id)
        if mix_id is None:
            return None

        cursor = 0
        awemeList = []

        print("[  提示  ]:正在获取合集下的所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [合集] 进行第 " + str(times) + " 次请求...\r")

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = 'https://www.douyin.com/aweme/v1/web/mix/aweme/?' + self.utils.getXbogus(
                        url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&mix_id={mix_id}&cursor={cursor}&count={count}')
                    res = requests.get(url=url, headers=self.headers, timeout=10)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据\r')
                    print('[  提示  ]:开始对 ' + str(len(datadict["aweme_list"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None:
                        break
                except Exception as e:
                    print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 获取 aweme_id
                aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                datanew, dataraw = self.getAwemeInfo(aweme_id)
                awemeList.append(copy.deepcopy(datanew))

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("\r\n[  提示  ]:[合集] 下所有作品数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[合集] 第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getUserAllMixInfo(self, sec_uid, count=35):
        print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None

        cursor = 0
        mixIdNameDict = {}

        print("[  提示  ]:正在获取主页下所有合集 id 数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [合集列表] 进行第 " + str(times) + " 次请求...\r")

            # url = self.urls.USER_MIX_LIST + self.utils.getXbogus(
            #     url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&sec_user_id={sec_uid}&count={count}&cursor={cursor}')

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = self.urls.USER_MIX_LIST + self.utils.getXbogus(
                        url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&sec_user_id={sec_uid}&count={count}&cursor={cursor}')
                    res = requests.get(url=url, headers=self.headers, timeout=10)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["mix_infos"])) + ' 条数据\r')
                    print('[  提示  ]:开始对 ' + str(len(datadict["mix_infos"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for mix in datadict["mix_infos"]:
                mixIdNameDict[mix["mix_id"]] = mix["mix_name"]

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("[  提示  ]:[合集列表] 下所有合集 id 数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[合集列表] 第 " + str(times) + " 次请求成功...\r\n")

        return mixIdNameDict

    # 来自 https://blog.csdn.net/weixin_43347550/article/details/105248223
    def progressBarDownload(self, url, filepath):
        start = time.time()  # 下载开始时间
        response = requests.get(url, stream=True, headers=self.headers, timeout=10)
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                print('[开始下载]:文件大小:{size:.2f} MB'.format(
                    size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[下载进度]:%s%.2f%%' % (
                            '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
            end = time.time()  # 下载结束时间
            print('\n' + '[下载完成]:耗时: %.2f秒\n' % (
                    end - start))  # 输出下载用时时间
        except Exception as e:
            # 下载异常 删除原来下载的文件, 可能未下成功
            if os.path.exists(filepath):
                os.remove(filepath)
            print("[  错误  ]:下载出错\r")

    def awemeDownload(self, aweids: list, awemeDict: dict, music=True, cover=True, avatar=True, savePath=os.getcwd()):
        if awemeDict is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        try:
            # # 使用作品 创建时间+描述 当文件夹
            # file_name = self.utils.replaceStr(awemeDict["create_time"] + " " + awemeDict["desc"])
            # aweme_path = os.path.join(savePath, file_name)
            # if not os.path.exists(aweme_path):
            #     os.mkdir(aweme_path)
            #
            # # 保存获取到的字典信息
            # print("[  提示  ]:正在保存获取到的信息到 result.json\r\n")
            # with open(os.path.join(aweme_path, "result.json"), "w", encoding='utf-8') as f:
            #     f.write(json.dumps(awemeDict, ensure_ascii=False, indent=2))
            #     f.close()
            aweme_path = savePath
            # 下载  视频
            # print(awemeDict)
            if awemeDict["awemeType"] == 0:
                self.log.info("[  提示  ]:正在下载视频...")
                # print("[  提示  ]:正在下载视频...\r")
                # '2023_02_28_09_57_41_7205020034115144972_广汽本田潮州志诚店.mp4'
                create_time = self.utils.strtime2strtime(awemeDict["create_time"])
                aweme_id = awemeDict["aweme_id"]
                author_nickname = awemeDict["author"]["nickname"]
                author_nickname = self.utils.strfomat(author_nickname)
                mp4filename = '{}_{}_{}'.format(create_time, aweme_id, author_nickname)
                video_path = os.path.join(aweme_path, mp4filename + ".mp4")

                if os.path.exists(video_path) or aweme_id in aweids:
                    self.log.info("[  提示  ]:视频 {} 已存在为您跳过".format(video_path))
                    # print("[  提示  ]:视频已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["video"]["play_addr"]["url_list"]
                        if url != "":
                            self.progressBarDownload(url, video_path)
                    except Exception as e:
                        self.log.exception("[  错误  ]:无法获取到视频url")
                        # print("[  错误  ]:无法获取到视频url\r\n")

            # 下载 图集
            if awemeDict["awemeType"] == 1:
                self.log.info("[  提示  ]:正在下载图集...")
                # print("[  提示  ]:正在下载图集...\r")
                create_time = self.utils.strtime2strtime(awemeDict["create_time"])
                aweme_id = awemeDict["aweme_id"]
                author_nickname = awemeDict["author"]["nickname"]
                author_nickname = self.utils.strfomat(author_nickname)
                tujidir = '图集{}'.format(aweme_id)
                # mp4filename = '{}_{}_{}'.format(create_time, aweme_id, author_nickname)
                tujidir_abs = os.path.join(aweme_path, tujidir)
                tujidir_for = '{}_{}_{}'.format(create_time, aweme_id, author_nickname)
                tujidir_for_abs = os.path.join(aweme_path, tujidir_for)
                if aweme_id in aweids:
                    self.log.info("[  提示  ]:图集 {} 已存在为您跳过".format(tujidir_abs))
                    # print("[  提示  ]:图集已存在为您跳过...\r\n")
                    if os.path.exists(tujidir_abs):
                        self.log.info(
                            "[  提示  ]:图集命名不规范 重命名 {} -> {}\r\n".format(tujidir_abs, tujidir_for_abs))
                        # print("[  提示  ]:图集命名不规范 重命名 {} -> {}\r\n".format(tujidir_abs, tujidir_for_abs))
                        os.rename(tujidir_abs, tujidir_for_abs)

                else:
                    os.makedirs(tujidir_for_abs)

                    for ind, image in enumerate(awemeDict["images"]):
                        # image_path = os.path.join(aweme_path, "image" + str(ind) + ".jpeg")
                        image_path = os.path.join(tujidir_for_abs, str(ind) + ".jpg")
                        if os.path.exists(image_path):
                            self.log.info("[  提示  ]:图片 {} 已存在为您跳过".format(image_path))
                            # print("[  提示  ]:图片已存在为您跳过...\r\n")
                        else:
                            try:
                                url = image["url_list"][0]
                                if url != "":
                                    self.progressBarDownload(url, image_path)
                            except Exception as e:
                                self.log.exception("[  错误  ]:无法获取到图片url")
                                # print("[  错误  ]:无法获取到图片url\r\n")

            # 下载  音乐
            if music:
                print("[  提示  ]:正在下载音乐...\r")
                music_name = self.utils.replaceStr(awemeDict["music"]["title"])
                music_path = os.path.join(aweme_path, music_name + ".mp3")

                if os.path.exists(music_path):
                    print("[  提示  ]:音乐已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["music"]["play_url"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, music_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到音乐url\r\n")

            # 下载  cover
            if cover and awemeDict["awemeType"] == 0:
                print("[  提示  ]:正在下载视频cover图...\r")
                cover_path = os.path.join(aweme_path, "cover.jpeg")

                if os.path.exists(cover_path):
                    print("[  提示  ]:cover 已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["video"]["cover_original_scale"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, cover_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到cover url\r\n")

            # 下载  avatar
            if avatar:
                print("[  提示  ]:正在下载用户头像...\r")
                avatar_path = os.path.join(aweme_path, "avatar.jpeg")

                if os.path.exists(avatar_path):
                    print("[  提示  ]:avatar 已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["author"]["avatar"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, avatar_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到avatar url\r\n")
        except Exception as e:
            traceback.print_exc()
            print("[  错误  ]:请检查json信息是否正确\r\n")

    def getUserAllAweId(self, savePath):
        awefs = os.listdir(savePath)
        aweids = []
        for awef in awefs:
            if '.mp4' in awef or '_' in awef:
                # '2022_06_03_14_11_05_7104892363994172713_米奇小号.mp4'
                aweid = awef.split('_')[6]
            elif '图集' in awef:
                # 图集7137269018834079011
                aweid = awef.replace('图集', '')
            else:
                continue
            aweids.append(aweid)
        return aweids

    def userDownload(self, aweids: list, awemeList: list, music=True, cover=True, avatar=True, savePath=os.getcwd()):
        if awemeList is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        # aweids = self.getUserAllAweId(savePath=savePath)

        for ind, aweme in enumerate(awemeList):
            print("[  提示  ]:正在下载 [%s] 的作品 %s/%s\r\n"
                  % (aweme["author"]["nickname"], str(ind + 1), len(awemeList)))

            self.awemeDownload(aweids, aweme, music, cover, avatar, savePath)
            # time.sleep(0.5)


if __name__ == "__main__":
    pass
