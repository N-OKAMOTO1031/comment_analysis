import pandas as pd
import time

import os 
import datetime
import sys
sys.path.append('src')
from get_comment import get_youtube_info
import yaml

from pathlib import PurePath
with open('config/load_config.yaml') as file:
    config = yaml.safe_load(file)

chat_id, video_id = get_youtube_info.get_chat_id(config['video_url'], config['youtube_api_key'])

pageToken = None

comment_list = []

while True:
    try:
        # 途中で設定が変更される場合があるため毎回読み込む
        with open('config/load_config.yaml') as file:
            config = yaml.safe_load(file)
        
        comment_list = get_youtube_info.get_comment(
                                                    comment_list, 
                                                    chat_id, 
                                                    config['youtube_api_key'],
                                                    pageToken)
        comment_df = pd.DataFrame({'comment':comment_list})
        os.makedirs('data', exist_ok=True)
        comment_df.to_csv('data/comment_df.csv', index=False) 
        time.sleep(config['refresh_rate_comment'])
    except:
            break
os.makedirs('data/comment_archive', exist_ok=True)
os.rename('data/comment_df.csv', f'data/comment_archive/{datetime.datetime.now().strftime("%Y%m%d")}_{video_id}_comment_df.csv')

