# comment_analysis
<!-- START doctoc -->
<!-- END doctoc -->
## 概要
Youtube Liveのコメントを、MeCabを使用して形態素解析を行い分かち書きしたうえでNlPlotを使用してリアルタイムに解析していくアプリです。  
Dashで作られたWebアプリケーションになっていますが、各個人のローカルで動かすことを想定して作っており、基本的にどこかのサーバーにデプロイして運用することは想定していません。

### 画面構成
画面の構成は以下の写真のようになっています。  
現状で表示されるグラフとしては以下の四つになります。  
 * 分かち書きしたうえで各単語の出現数、出現頻度
 * 共起ネットワークのネットワーク図
 * 共起ネットワークに関連したサンバーストチャート
 * ワードクラウド  
 
 ### 内部処理の概要
 ![処理フロー](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/4c18f820-3175-4043-a373-3025f0eae3a5)  
 全体の処理の構成としては、configを外出しし、Get_comment内でループが回るたびにロードすることによって設定値の変更に対応しています。  
 一方でcreate_plot等に関しても、呼び出すたびにconfigを読み込む形をとっているのだが、これに関しては作り始めたころと構想が変わり、その頃の処理の仕方が残ってしまっているがためです。

 ## 環境の構築
 こちらのアプリケーションはPythonで書いてあるため、Python環境が必須ですのでない場合は最初にPythonを導入してください。  
 以降の説明は、pythonの環境があることを前提として進めていきます
 ### MeCabのユーザー辞書（NEologd）の導入
 こちらのアプリは、MeCabを使用して形態素解析を行い分かち書きをしています。NEologdを導入しなくても、Mecab-Python3を使うだけでも問題なく動くものの、Youtubeのコメントではネット用語が多く使われるためNEologdを導入したほうが正確に形態素解析を行うことができます。導入手順を見たうえで、面倒くさいと思ったら無しで動かしてみて、やっぱり必要だなと思った段階でこちらに戻ってきて再度導入するでも多分大丈夫です。
 #### Windowsの場合
 1. MeCab辞書の変換のためにMeCabをダウンロードします。以下のリンクから最新のexeファイルをダウンロードしてきます。  
 https://github.com/ikegami-yukino/mecab/releases/tag/v0.996.2

 2. ダウンロードしてきたexeを実行してMeCabをインストールします。その際に、言語設定後に以下のように文字コードの設定が出てくるのでUTF-8にしておきましょう。  
 ![mecab_install_unicode](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/0d0ff46e-a908-45df-9ecd-af85cef0d5de)

 3. 続いてNEologdをダウンロードしてきます。以下のリンクからGithubに飛びダウンロードしてきてください。（git cloneでもOK）  
 https://github.com/neologd/mecab-ipadic-neologd  
 Git cloneがわからない場合は、以下の画像の箇所からDownload ZIPで持ってこれます。
 ![NEologd_download](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/b4e30f15-1d8d-4bed-b770-de1aa3dbb648)

 4. フォルダーを展開した後にmecab-ipadic-neologd-master/seed内にあるmecab-user-dict-seed.20200910.csv.xzを解凍します。この際に7-zipがあると便利。

 5. 続いて.csvをバイナリー辞書に変換します。MeCabがインストールされている箇所を探します。大体C:\Program Files (x86)\MeCabにあります。見つけたら、コマンドプロンプトを開き以下の手順でコマンドを実行していきます。  

    1. MeCabフォルダー内のbinフォルダーを右クリックして、パスをコピーした後にコマンドプロンプトで  
        ```
        > cd {コピーしたパスをペースト} 
        ```
        を入力してbinフォルダーに移動します。  

    2. 続いて、先ほど解凍したcsvファイルを右クリックでパスをコピーしたうえで、コマンドプロンプトで
        ```
        > mecab-dict-index -d "C:\Program Files (x86)\MeCab\dic\ipadic" -u {出力したいフォルダー先}\mecab-user-dict-seed.20200910.dic -f utf-8 -t utf-8 {コピーしたパス}
        ```
        を入力します。以下が表示されたら成功です。
        ![dic_binaly](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/0557b9b5-8d52-43ac-a34e-4a46ddc5416e)
        これで辞書の変換が完了しました。辞書ファイルの移動、およびパスの追記をする必要があるのですがこのアプリをダウンロードした後にする必要があるので、後ほど実行します。

 #### macの場合
 1. 