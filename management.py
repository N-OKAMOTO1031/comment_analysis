import os
import yaml
import webbrowser

# 実行された段階で｀Youtube APIのkeyを環境変数に登録
with open('config/api_config.yaml') as file:
    config = yaml.safe_load(file)

os.environ['youtube_api_key'] = config['youtube_api_key']

webbrowser.open('http://127.0.0.1:8000')

from src import view




