import pandas as pd
import time
import os 
import datetime
import sys
sys.path.append('src')
from get_comment import get_youtube_info

from pathlib import PurePath

chat_id, video_id = get_youtube_info.get_chat_id(os.getenv('video_url'), 
                                                 os.getenv('youtube_api_key'))

pageToken = None

comment_list = []

while True:
    try:
        comment_list = get_youtube_info.get_comment(
                                                    comment_list, 
                                                    chat_id, 
                                                    os.getenv('youtube_api_key'),
                                                    pageToken)
        os.makedirs('data', 
                    exist_ok=True)
        with open('data/comment_list.txt', 'w', encoding = 'utf-8') as f:
            f.write('\n'.join(comment_list))

        time.sleep(int(os.getenv('refresh_rate_comment')))
    except:
            break
os.makedirs('data/comment_archive', 
            exist_ok=True)
os.rename('data/comment_list.txt', 
          f'data/comment_archive/{datetime.datetime.now().strftime("%Y%m%d")}_{video_id}_comment_list.txt')

