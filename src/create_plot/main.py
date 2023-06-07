import nlplot
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os
import yaml
from create_plot import split_comment
import MeCab
import plotly.graph_objects as go
import plotly.express as px


def plot_main(min_edge, word_freq_type, display_word_num):
    # macとwindowsによってmecabのユーザー辞書の使い方が違うため分岐
    # ユーザー辞書を読み込めなかった場合は、デフォルトのmecabで実行
    # netスラングとうに対応できないことが多いためNEologd推奨
    try:
        # windows用のユーザー辞書設定
        if os.name =='nt':
            spliter = MeCab.Tagger(r'-d "C:/Program Files (x86)/MeCab/dic/ipadic" -u "data/mecab_dictionaly/mecab-user-dict-seed.20200910.dic"')

        # mac用のユーザー辞書設定
        elif os.name =='posix':
            spliter = MeCab.Tagger(r'-d "macのmecab-ipadic-neologdのフォルダーパスを記入"')
    except:
        tagger = MeCab.Tagger()

    with open('config/load_config.yaml') as file:
        config = yaml.safe_load(file)

    # 全部選択されている場合はNoneを返す
    if len(config['except_part_of_speech_list'])==13:
        return min_edge, None, None, None, None


    df = pd.read_csv('data/comment_df.csv')

    df['split_word'] = df['comment'].apply(lambda x:split_comment.get_specified_word(x,
                                                                                    spliter, 
                                                                                    config['except_part_of_speech_list'], 
                                                                                    config['except_word_list']))
    
    # 単語出現頻度をプロット
    try:
        word_freq_fig = plot_word_freq_plot(itertools.chain.from_iterable(df['split_word'].to_list()),
                                            word_freq_type, 
                                            display_word_num)
    except:
        word_freq_fig = None

    # nlplotの設定
    npt = nlplot.NLPlot(df, target_col='split_word')
    stopwords = npt.get_stopword(top_n=2, min_freq=0)

    # 共起ネットワークのプロットを作成
    try:
        min_edge, fig_co_network, fig_sunburst = plot_co_network(npt, min_edge, stopwords)
    except:
        fig_co_network, fig_sunburst = None, None
    
    # word cloudをプロット
    try:
        fig_word_cloud = plot_word_cloud(npt, stopwords)
    except:
        fig_word_cloud = None

    return min_edge, word_freq_fig, fig_co_network, fig_sunburst, fig_word_cloud

def plot_word_freq_plot(word_list, word_freq_type, display_word_num):
    """
    単語の出現頻度のグラフを描画
    
    Parameters:
    ---------------------------------
    word_list: list of str
        MeCabで分離した単語リスト

    word_freq_type: str
        プロットを割合にするか数にするか
    
    display_word_num: int
        表示する単語数

    Return:
    ---------------------------------
    fig: plotly graph object
        単語出現頻度のプロット結果

    """
    word_df = pd.DataFrame({'word':word_list, 'values':1})
    word_df = word_df.groupby('word', as_index=False).count()

    word_df['freq'] = (word_df['values']/word_df['values'].sum())*100

    word_df = word_df.sort_values('values', ascending=False).head(display_word_num)
    figures = []
    figures.append(
        go.Bar(x = word_df[word_freq_type],
            y=word_df['word'],
            orientation="h"
            )
    )
    if word_freq_type == 'values':
        hovertemplate='%{y}: %{x:0.0f}個'
        texttemplate='%{x:0.0f}個'
        xaxis_title = '出現頻度(個数)'
        
    elif word_freq_type == 'freq':
        hovertemplate='%{y}: %{x:0.2f}%'
        texttemplate='%{x:0.2f}%'
        xaxis_title = '出現頻度(%)'

    fig = go.Figure(data=figures)
    fig.update_traces(width=0.5,
                    hovertemplate=hovertemplate,
                    texttemplate=texttemplate,
                    textposition='outside')
    fig.update_layout(title = '単語出現頻度',
                    yaxis={'title':'単語',
                            'categoryorder':'total ascending'},
                    xaxis={'title':xaxis_title},
                    width=1000, 
                    height=display_word_num*30,)
    return fig



def plot_co_network(npt, min_edge, stopwords):
    """
    共起ネットワークを計算し計算結果を返す関数
    
    Parameters:
    ---------------------------------
    npt: NLPlot
        nlplotの結果を格納しているもの（だと思われる）

    min_edge: int
        node数を計算する際のmin_edge_frequencyの初期値

    stopword: list of str
        ストップワードを格納したリスト

    Return:
    ---------------------------------
    go.Figure(fig_co_network): plotly graph object
        共起ネットワークのプロット結果

    fig_sunburst: plotly graph object
        サンバーストのプロット結果

    """
    try:
        cal_node = True
        while cal_node:
            npt.build_graph(stopwords=stopwords, min_edge_frequency=min_edge)
            if len(npt.node_df)<=50:
                cal_node = False
            else:
                min_edge += 10
    except:
        min_edge = 10
        pass

    min_edge -= 9
    cal_node = True
    while cal_node:
        npt.build_graph(stopwords=stopwords, min_edge_frequency=min_edge)
        if len(npt.node_df)<=50:
            cal_node = False
        else:
            min_edge += 1
    try:
        fig_co_network = npt.co_network(
            title='共起ネットワーク',
            sizing=100,
            node_size='adjacency_frequency',
            color_palette='hls',
            width=800,
            height=700,
            save=False
        )
    except:
        fig_co_network = None

    try:
        fig_sunburst = npt.sunburst(
                                    title='sunburst chart',
                                    colorscale=True,
                                    color_continuous_scale='Oryel',
                                    width=800,
                                    height=800,
                                    save=False
                                    )
    except:
        fig_sunburst = None

    return min_edge, fig_co_network, fig_sunburst

def plot_word_cloud(npt, stopwords):
    """
    共起ネットワークを計算し計算結果を返す関数
    
    Parameters:
    ---------------------------------
    npt: NLPlot
        nlplotの結果を格納しているもの（だと思われる）

    stopword: list of str
        ストップワードを格納したリスト

    Return:
    ---------------------------------
    fig: plotしたword cloud

    """
    fig_wc = npt.wordcloud(
    width=1000,
    height=700,
    max_words=100,
    max_font_size=100,
    colormap='tab20_r',
    stopwords=stopwords,
    mask_file=None,
    save=False
    )
    fig = px.imshow(fig_wc)

    fig.update_layout(height=700, width=1000)
    return fig