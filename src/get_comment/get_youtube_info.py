import requests

import pandas as pd

def get_chat_id(url, api_key):
    """
    動画urlからchat_idを取得
    
    Parameters:
    ---------------------------------
    url: str
        動画url

    api_key: str
        google_platformのyoutube data v3のapikey

    Return:
    ---------------------------------
    chat_id: str
        youtube liveのチャットid

    title: str
        動画タイトル

    """

    video_id = url.replace('https://www.youtube.com/watch?v=', '')

    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': api_key, 'id': video_id, 'part': 'liveStreamingDetails, snippet'}
    data   = requests.get(url, params=params).json()
    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        title = data['items'][0]['snippet']['title']
    else:
        title = None
        chat_id = None
    return chat_id, video_id

def get_comment(comment_list, chat_id, api_key, pageToken):
    """
    youtube liveからコメント一覧を取得してリストで返す
    
    Parameters:
    ---------------------------------
    comment_list: list of str or none
        コメントを格納したリスト

    chat_id: str
        対称のyoutube liveのchat id

    api_key: str
        google_platformのyoutube data v3のapikey

    spliter: mecab.tagger
        mecabのtaggerメソッド

    pageToken: str or None
        youtube liveのチャットのページトークン

    Return:
    ---------------------------------
    comment_list: list of str
        コメントを格納したリスト
    
    pageToken: str
        youtube liveのチャットの次のページトークン

    """
    request_url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': api_key, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    data = requests.get(request_url, params=params).json()
    pageToken = data['nextPageToken']


    add_comment_list = [i['snippet']['displayMessage'] for i in data['items']]

    comment_list = comment_list + add_comment_list
    
    return comment_list