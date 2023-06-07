import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

def setting_layout():
    setting = \
html.Div(
    [
        dbc.Row(
            [
                html.P('comment load setting')
            ],
            style={"height": "10vh", "fontSize": 30, 'textAlign': 'center'}
        ),
        dbc.Row(
            [
                dbc.Col([
                        html.Label('動画URLを入力：'),
                        ]),
                dbc.Col(id='live_status'),
                dbc.Input(id="video_url", size="sm",
                          placeholder="動画URL", type="text")
            ],
        ),
        dbc.Row(
            style={"height": "2vh"}
        ),
        dbc.Row(
            [
                html.Label('再読み込みレート（秒）'),
            ]),
        dbc.Row([
                dbc.Col([
                        html.Label('コメントロード間隔:'),
                        ]),
                dbc.Col([
                        dbc.Input(id="refresh_comment", value=5, size="sm", type='number', min=2),   
                        ]),

            ]),
        dbc.Row([
                dbc.Col([
                        html.Label('グラフ更新間隔:'),
                        ]),
                dbc.Col([
                        dbc.Input(id="refresh_plot", value=10, size="sm", type='number', min=5),   
                        ]),

            ]),
        dbc.Row(
            style={"height": "2vh"}
        ),
        dbc.Row(
            [
                html.Label('除外品詞を設定', style={
                           "height": "4vh", "fontSize": 20, 'textAlign': 'center'}),
                html.Label('全部除外設定してしまうと、グラフが表示されないor更新されなくなりますので注意してください。', style={"fontSize": 10, }),
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="except_part_of_speech_1",
                            options=[
                                {'label': '名詞', 'value': '名詞'},
                                {'label': '助詞', 'value': '助詞'},
                                {'label': '助動詞', 'value': '助動詞'},
                                {'label': '形容詞', 'value': '形容詞'},
                                {'label': '副詞', 'value': '副詞'},
                                {'label': '動詞', 'value': '動詞'},
                                {'label': 'フィラー', 'value': 'フィラー'},
                            ],
                            value=['助詞', '助動詞', '形容詞', '副詞', 'フィラー'],
                            style={"fontSize": 17, 'textAlign': 'left'}
                        )]),
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="except_part_of_speech_2",
                            options=[
                                {'label': '感動詞', 'value': '感動詞'},
                                {'label': '接頭詞', 'value': '接頭詞'},
                                {'label': '連体詞', 'value': '連体詞'},
                                {'label': '接続詞', 'value': '接続詞'},
                                {'label': '記号', 'value': '記号'},
                                {'label': 'その他', 'value': 'その他'}
                            ],
                            value=['感動詞', '接頭詞', '連体詞', '接続詞', '記号', 'その他'],
                            style={"fontSize": 17, 'textAlign': 'left'}
                        )])
            ],

        ),
        dbc.Row(
            style={"height": "2vh"}
        ),
        dbc.Row(
            [
                html.Label('除外単語指定', style={"fontSize": 20, 'textAlign': 'left'}),
                html.Label('除外する単語を設定する箇所です。', style={"fontSize": 10, }),
                html.Label('設定したい単語を半角のカンマ区切りで入力してください。',
                           style={"fontSize": 10, }),
                dbc.Input(id="except_word", size="sm",
                          placeholder='例）こんにちは,草,閉じる', type='txt')
            ],
        ),
        dbc.Row(
            style={"height": "5vh"}
        ),
        dbc.Row(id='button', children=[
                                        dbc.Button("設定完了", id="setting_comp",
                                                className="setting", n_clicks=0)
                                        ]
        ),
        dbc.Row(id='interval_status')
    ]
)
    return setting

def plot_layout():
    # 単語の出現頻度をプロットするタブ
    word_frequency_plot_tab = \
        dbc.Card(
                [
                    dbc.Row(
                            [
                                    dbc.Col(
                                    [   
                                        html.Label('プロット対象を選択'),
                                        dcc.Dropdown(id = 'word_freq_type',
                                                    options=[
                                                                {'label': '出現数', 'value': 'values'},
                                                                {'label': '出現割合', 'value': 'freq'}
                                                            ],
                                                            value='freq'
                                                        )
                                    ]
                                        ),
                                    dbc.Col(
                                    [
                                        html.Label('表示単語数を選択'),
                                        dbc.Input(id="display_word_num", size="sm",value=20, min=10, step=10, type="number")
                                    ]
                                ),
                            ]
                            ),
                    dbc.Row(id = 'word_freq_plot_row', children = [])
                ]
                )
    # 共起ネットワークをプロットするタブ
    co_networks_plot_tab = \
        dbc.Card(
                [
                    dbc.Row(id = 'co_networks_plot_row', children = []),
                    dbc.Row(id = 'sunburst_plot_row', children = []),
                ]
                )
    # ワードクラウドをプロットするタブ
    word_cloud_tab = \
        dbc.Card(
                [
                    dbc.Row(id = 'word_cloud_plot_row', children = [])
                ]
                    )
    plot = \
        html.Div(
            children=[
                dbc.Tabs([
                    dbc.Tab(id = 'word_frequency', children = [word_frequency_plot_tab], label="単語出現頻度"),
                    dbc.Tab(id = 'co_networks', children = [co_networks_plot_tab], label="共起ネットワーク"),
                    dbc.Tab(id = 'word_cloud', children = [word_cloud_tab], label='ワードクラウド'),
                ],
                
                    )
                    ]
                )
    return plot