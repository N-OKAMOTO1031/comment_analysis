import pandas as pd
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import yaml
import sys
import concurrent.futures
import datetime
import time

sys.path.append('src')
import create_plot
sys.path.append('src/view')
import layouts
sys.path.append('src/get_comment')
import get_youtube_info


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

setting = layouts.setting_layout()
plot = layouts.plot_layout()

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(setting, width=3, className='bg-light'),
                dbc.Col(plot, width=9)
            ],
            style={"height": "100vh"}
        ),
        html.Div(id='interval_div')
    ],
    fluid=True
)

# ライブ状況を確認
@app.callback(
        dash.Output('live_status', 'children'),
        dash.Input('video_url', 'value')
)
def check_live(video_url):
    with open('config/api_config.yaml') as file:
            config = yaml.safe_load(file)
    if video_url == None:
        return
    
    try:
        chat_id, video_id = get_youtube_info.get_chat_id(video_url, config['youtube_api_key'])
    except:
        return 'This video is not live or you may have reached the daily comment acquisition limit.'

    if type(chat_id)==str and type(video_id) == str:
        live_status = 'Now Live'

    else:
        live_status = 'Not Live, please check url'
    
    return live_status

# 設定完了時の処理
@app.callback(
    dash.Output('button', 'children', allow_duplicate=True),
    dash.Input('setting_comp', 'n_clicks'),
    dash.State('video_url', 'value'),
    dash.State('refresh_comment', 'value'),
    dash.State('refresh_plot', 'value'),
    dash.State('except_part_of_speech_1', 'value'),
    dash.State('except_part_of_speech_2', 'value'),
    dash.State('except_word', 'value'),
    dash.State('button', 'children'),
    prevent_initial_call=True
)
def setting_complete(n_clicks, 
                     video_url,
                     refresh_rate_comment,
                     refresh_rate_plot, 
                     except_part_of_speech_1, 
                     except_part_of_speech_2, 
                     except_word, 
                     button_children):
    if n_clicks == 0:
        pass
        return button_children
    else:
        # 入力されてなかった場合用の処理
        if video_url == None:
            if len(button_children)>1:
                button_children = button_children[:1]
            button_children.append('URLを入力してください')
            return button_children
        
        elif (refresh_rate_comment == None) or (refresh_rate_plot == None):
            if len(button_children)>1:
                button_children = button_children[:1]
            button_children.append('再読み込みレートを設定してください')
            return button_children
        
        else:
            try:
                with open('config/api_config.yaml') as file:
                    config = yaml.safe_load(file)
                chat_id, video_id = get_youtube_info.get_chat_id(video_url, config['youtube_api_key'])
            except:
                if len(button_children)>1:
                    button_children = button_children[:1]
                button_children.append('この動画はライブ動画ではありません。URLを確認してください。')
                return button_children
            
            if type(chat_id)==str and type(video_id) == str:
                pass

            else:
                if len(button_children)>1:
                    button_children = button_children[:1]
                button_children.append('この動画は現在ライブ中ではないようです。URLを確認してください。')
                return button_children

        
        # 除外単語用の処理
        if except_word == None:
            except_word_list = []
        else:
            except_word = except_word.replace(' ', ',')
            except_word = except_word.replace('　', ',')
            except_word = except_word.replace('、', ',')
            except_word_list = except_word.split(',')

        
        with open('config/api_config.yaml') as file:
            config = yaml.safe_load(file)

        with open("config/load_config.yaml", "w") as yf:
            load_config = {}
            load_config['youtube_api_key'] = config['youtube_api_key']
            load_config['video_url'] = video_url
            load_config['refresh_rate_comment'] = refresh_rate_comment
            load_config['refresh_rate_plot'] = refresh_rate_plot
            load_config['except_part_of_speech_list'] = except_part_of_speech_1 + except_part_of_speech_2
            load_config['except_word_list'] = except_word_list
            
            yaml.dump(load_config, yf)
        ## 実行ボタンを配置
        execution_child = [dbc.Button("コメント解析を実行", id="execution",
                                    className="execution", n_clicks=0)]
        return execution_child
    
# コメント解析を実行時の処理
@app.callback(
    dash.Output('button', 'children', allow_duplicate=True),
    dash.Input('execution', 'n_clicks'),
    dash.State('button', 'children'),
    prevent_initial_call=True
)
def execution_get_comment(n_clicks, button_children):
        def excecution_get_comment():
            
            import get_comment
        
        if n_clicks == 0:
            pass
            return button_children
        else:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
            executor.submit(excecution_get_comment)
        
            ## 設定変更ボタンを設定
            new_child = [dbc.Button("設定変更（URLは途中変更できません）", id="change_setting", n_clicks=0)]
            return new_child
    


# 設定変更時の動作
@app.callback(
    dash.Output('button', 'children'),
    dash.Input('change_setting', 'n_clicks'),
    dash.State('refresh_comment', 'value'),
    dash.State('refresh_plot', 'value'),
    dash.State('except_part_of_speech_1', 'value'),
    dash.State('except_part_of_speech_2', 'value'),
    dash.State('except_word', 'value'),
    dash.State('button', 'children'),
)
def change_setting(n_clicks, 
                   refresh_rate_comment,
                   refresh_rate_plot, 
                   except_part_of_speech_1, 
                   except_part_of_speech_2, 
                   except_word, 
                   button_children):
    if n_clicks == 0:
        pass
        return button_children
    else:
        # 除外単語用の処理
        if except_word == None:
            except_word_list = []
        else:
            except_word = except_word.replace(' ', ',')
            except_word = except_word.replace('　', ',')
            except_word = except_word.replace('、', ',')
            except_word_list = except_word.split(',')
        
        # 変更された設定値を保存
        with open('config/load_config.yaml') as file:
            last_config = yaml.safe_load(file)

        with open("config/load_config.yaml", "w") as yf:
            load_config = {}
            load_config['youtube_api_key'] = last_config['youtube_api_key']
            load_config['video_url'] = last_config['video_url']
            if refresh_rate_comment==None:
                load_config['refresh_rate_comment'] = last_config['refresh_rate_comment']
            else:
                load_config['refresh_rate_comment'] = refresh_rate_comment

            if refresh_rate_plot==None:
                load_config['refresh_rate_plot'] = last_config['refresh_rate_plot']
            else:
                load_config['refresh_rate_plot'] = refresh_rate_plot
            load_config['except_part_of_speech_list'] = except_part_of_speech_1 + except_part_of_speech_2
            load_config['except_word_list'] = except_word_list
            
            yaml.dump(load_config, yf)
        ## 変更時間を追記
        if len(button_children)==2:
            button_children[1] = f'{datetime.datetime.now().strftime("%X")}：設定を変更しました'
        else:
            button_children.append(f'{datetime.datetime.now().strftime("%X")}：設定を変更しました')
        return button_children

# plotの実行
@app.callback(
    [dash.Output('word_freq_plot_row', 'children', allow_duplicate=True),
     dash.Output('co_networks_plot_row', 'children', allow_duplicate=True),
     dash.Output('sunburst_plot_row', 'children', allow_duplicate=True),
     dash.Output('word_cloud_plot_row', 'children', allow_duplicate=True),
     dash.Output('interval_status', 'children', allow_duplicate=True)],
    dash.Input('execution', 'n_clicks'),
    dash.State('word_freq_type', 'value'),
    dash.State('display_word_num', 'value'),
    prevent_initial_call=True
)

@app.callback(
    [dash.Output('word_freq_plot_row', 'children'),
     dash.Output('co_networks_plot_row', 'children', allow_duplicate=True),
     dash.Output('sunburst_plot_row', 'children'),
     dash.Output('word_cloud_plot_row', 'children'),
     dash.Output('interval_status', 'children', allow_duplicate=True)],
    dash.Input('interval_not_plot', 'n_intervals'),
    dash.State('word_freq_type', 'value'),
    dash.State('display_word_num', 'value'),
    prevent_initial_call=True
)

def execution_plot(n_trials, 
                   word_freq_type, 
                   display_word_num
                   ):
    if n_trials == 0:
        pass
        return None, None, None, None, None
    else:
        with open('config/load_config.yaml') as file:
            config = yaml.safe_load(file)
        time.sleep(2)

        # データがなかった場合状況を確認して対応を返す
        try:
            comment_df_len = len(pd.read_csv('data/comment_df.csv'))
        except FileNotFoundError:
            try:
                chat_id, video_id = get_youtube_info.get_chat_id(config['video_url'], config['youtube_api_key'])
            except:
                interval_children = html.P('Youtube APIの一日のコメント取得数の制限に達した可能性があります。確認してください。',
                                           style={"fontSize": 30, 'textAlign': 'center', 'color':'red'})
                
                return None, None, None, None, interval_children
            
            if type(chat_id)==str and type(video_id) == str:
                interval_children = html.P('コメントを取得したデータが確認できません。コメント取得処理側で処理が終了している可能性があります。YoutubeAPIの一日の取得制限等をご確認ください。',
                                           style={"fontSize": 30, 'textAlign': 'center', 'color':'red'})
                
                return None, None, None, None, interval_children

            else:
                interval_children = html.P('動画がライブ状態ではない可能性があります。確認してください。',
                                           style={"fontSize": 30, 'textAlign': 'center', 'color':'red'})
                
                return None, None, None, None, interval_children

        if comment_df_len < 100:
            # intervalを設定
            interval_children = dcc.Interval(id='interval_not_plot', interval=config['refresh_rate_plot']*1000)
            return None, None, None, None, interval_children
        else:
            # 各plotを取得
            min_edge = 10
            min_edge, word_freq_fig, fig_co_network, fig_sunburst, fig_word_cloud = create_plot.main.plot_main(min_edge, word_freq_type, display_word_num)
            # 単語の頻度のプロットを配置
            if word_freq_fig == None:
                word_freq_children = None
            else:
                word_freq_children = [(dcc.Graph(id = 'word_freq_plot', figure = word_freq_fig))]

            # 共起ネットワークのプロットを配置
            if fig_co_network == None:
                co_networks_children = None
            else:
                co_networks_children = [(dcc.Graph(id = 'co_network_plot', figure = fig_co_network))]
            
            if fig_sunburst == None:
                sunburst_children = None
            else:
                sunburst_children = [(dcc.Graph(id = 'sunburst_plot', figure = fig_sunburst))]

            # word cloudのプロットを配置
            if fig_word_cloud == None:
                word_cloud_children = None
            else:  
                word_cloud_children = [(dcc.Graph(id = 'word_cloud_plot', figure = fig_word_cloud))]

            # min_edgeを保存
            with open("config/co_network_config.yaml", "w") as yf:
                co_network_config = {}
                co_network_config['min_edge'] = min_edge
                yaml.dump(co_network_config, yf)

            # intervalを設定、どれか一つでも返ってきてなかった場合はもう一度この関数を動かす
            with open('config/load_config.yaml') as file:
                config = yaml.safe_load(file)

            if (word_freq_fig == None) or (fig_co_network == None) or (fig_sunburst == None) or (fig_word_cloud == None):
                interval_children = dcc.Interval(id='interval_not_plot', interval=config['refresh_rate_plot']*1000)
            else:
                interval_children = dcc.Interval(id='interval_plot', interval=config['refresh_rate_plot']*1000)

        return  word_freq_children, co_networks_children, sunburst_children, word_cloud_children, interval_children


# intervalの設定
@app.callback(
    [dash.Output('word_freq_plot', 'figure'),
     dash.Output('co_networks_plot_row', 'children'),
     dash.Output('sunburst_plot', 'figure'),
     dash.Output('word_cloud_plot', 'figure'),
     dash.Output('interval_status', 'children')],
    dash.Input('interval_plot', 'n_intervals'),
    dash.State('word_freq_plot', 'figure'),
    dash.State('co_networks_plot_row', 'children'),
    dash.State('sunburst_plot', 'figure'),
    dash.State('word_cloud_plot', 'figure'),
    dash.State('word_freq_type', 'value'),
    dash.State('display_word_num', 'value'),
)
def execution_plot(n_intervals,
                   word_freq_fig_old,
                   co_networks_children_old,
                   fig_sunburst_old,
                   fig_word_cloud_old,
                   word_freq_type, 
                   display_word_num,
                   ):
    with open('config/co_network_config.yaml') as file:
        co_network_config = yaml.safe_load(file)

    with open('config/load_config.yaml') as file:
        config = yaml.safe_load(file)
    # 各plotを取得
    try:
        min_edge, word_freq_fig, fig_co_network, fig_sunburst, fig_word_cloud = create_plot.main.plot_main(co_network_config['min_edge'], word_freq_type, display_word_num)
    except FileNotFoundError:
        # エラーが発生した場合はライブ状況を確認して状況に応じて対応を返す
        try:
            chat_id, video_id = get_youtube_info.get_chat_id(config['video_url'], config['youtube_api_key'])
        except:
            interval_children = html.P('Youtube APIの一日のコメント取得数の制限に達した可能性があります。確認してください。',
                                        style={"fontSize": 30, 'textAlign': 'center', 'color':'red'})
            
            return word_freq_fig_old, co_networks_children_old, fig_sunburst_old, fig_word_cloud_old, interval_children
        
        if type(chat_id)==str and type(video_id) == str:
            interval_children = html.P('コメントを取得したデータが確認できません。コメント取得処理側で処理が終了している可能性があります。YoutubeAPIの一日の取得制限等をご確認ください。',
                                        style={"fontSize": 30, 'textAlign': 'center', 'color':'red'})
            
            return word_freq_fig_old, co_networks_children_old, fig_sunburst_old, fig_word_cloud_old, interval_children

        else:
            interval_children = html.P('Youtube Liveが終了しました。処理を終了します。',
                                        style={"fontSize": 30, 'textAlign': 'center'})
            
            return word_freq_fig_old, co_networks_children_old, fig_sunburst_old, fig_word_cloud_old, interval_children
    # 単語の頻度のプロットを配置
    if word_freq_fig == None:
        word_freq_fig = word_freq_fig_old
    else:
        pass

    # 共起ネットワークのプロットを配置
    if fig_co_network == None:
        co_networks_children = co_networks_children_old
    else:
        co_networks_children = [(dcc.Graph(id = 'co_network_plot', figure = fig_co_network))]
    
    if fig_sunburst == None:
        fig_sunburst = fig_sunburst_old
    else:
        pass

    # word cloudのプロットを配置
    if fig_word_cloud == None:
        fig_word_cloud = fig_word_cloud_old
    else:  
        pass

    # min_edgeを保存
    with open("config/co_network_config.yaml", "w") as yf:
        co_network_config = {}
        co_network_config['min_edge'] = min_edge
        yaml.dump(co_network_config, yf)
    
    # intervalを設定
    interval_children = dcc.Interval(id='interval_plot', interval=config['refresh_rate_plot']*1000)

    return  word_freq_fig, co_networks_children, fig_sunburst, fig_word_cloud, interval_children

app.run_server(host='127.0.0.1', port='8000')
