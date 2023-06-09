# comment_analysis
<!-- START doctoc -->
<!-- END doctoc -->
## 概要
Youtube Liveのコメントを、MeCabを使用して形態素解析を行い分かち書きしたうえでNlPlotを使用してリアルタイムに解析していくアプリです。  
Dashで作られたWebアプリケーションになっていますが、各個人のローカルで動かすことを想定して作っており、基本的にどこかのサーバーにデプロイして運用することは想定していません。

### 画面構成
画面の構成は以下の写真のようになっています。  
![画面概要](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/b2572d80-bb47-4222-9250-337ccd7d33f8)
現状で表示されるグラフとしては以下の四つになります。  
 * 分かち書きしたうえで各単語の出現数、出現頻度
 * 共起ネットワークのネットワーク図
 * 共起ネットワークに関連したサンバーストチャート
 * ワードクラウド  
 
### 内部処理の概要
![処理フロー](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/4c18f820-3175-4043-a373-3025f0eae3a5)  
全体の処理の構成としては、configを外出しし、Get_comment内でループが回るたびにロードすることによって設定値の変更に対応しています。  
一方でcreate_plot等に関しても、呼び出すたびにconfigを読み込む形をとっているのだが、これに関しては作り始めたころと構想が変わり、その頃の処理の仕方が残ってしまっているがためです。

## 周辺準備
こちらのアプリケーションはPythonで書いてあるため、Python環境が必須ですのでない場合は最初にPythonを導入してください。また、requirements.txtを用意してありますのでそちらを使用して環境を作成して下さい。  
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
macではhomebrewを使用してインストールを行います。最初のbrewコマンドを使用してみて動かないようであれば、homebrewを導入してください。
1. 最初にmecabをインストールします。macでターミナルを開き以下のコマンドを実行します。
```
$ brew install mecab mecab-ipadic
```

2. 続いてmecab-ipadic-NEologdをgitからクローンしてきます。以下のコマンドを実行してください。
```
$ git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git

```

3. 2番でclone出来たら。フォルダーに移動したのちに辞書のインストールを行います。この際に、オプションに-nと-n -aがありますが時間はかかるものの後者がお勧めです。
```
$ cd mecab-ipadic-neologd
$ ./bin/install-mecab-ipadic-neologd -n
```
途中で以下の文章が表示された場合は、yesと入力してください。
```
Do you want to install mecab-ipadic-NEologd? Type yes or no.
```

以上で完了です。macの場合でもパスを通す必要があるのですが後ほど実施します。

### Youtube APIのAPIkeyの発行
今回のアプリケーションでは、Youtube Data v3 apiを使用してコメントの取得を行なっています。そのため、GCPでAPIkeyを発行する必要があります。こちらのAPIに関しては無料で使えます。
1. 以下のURLからGoogle Cloudにアクセスします。この際にすでに使ったことがある方はコンソール画面にいくと思いますが、使ったことがない方は画面の指示に従って操作していってください。下の画面まで行ったら、矢印で示しているMy First Projectをクリックしてコンソール画面に移動してください。
![登録完了](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/e815f15c-1241-4168-b0b1-4bc9bacb26d2)

2. すでにGCPを使ったことがある人はここからになると思います。
左側のメニューバーから APIとサービス>ライブラリー を選択してください。
![コンソール1](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/da64f65a-cb06-46f6-8397-274a78c3650a)
そうすると以下の画面が出てくると思うので、検索窓に Youtubeと入れて予測に出てくる Youtube Data api v3 を選択
![api_検索](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/64e34ab9-b4f2-4e89-9157-a3626e952397)
出てきた製品の詳細を開き、有効にするを選択します。

3. 以下の画面に移動したら、左側の認証情報を選択します。
![認証](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/521f2ab9-7b28-4459-b6e8-52bd6e846b2d)
下の画面に遷移したら、認証情報の作成>APIキーを選択します。
![認証_APIキー](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/65105c0b-d59e-4f41-9389-06b5edafe0cb)
そうすると、しばらくして以下のようにAPIキーが表示されます。これは後ほど使うのでどこかにコピーしとくと良いです。（後から確認することもできます。）
![API_key](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/9fd9057f-8809-4c06-816f-8a4f96cd6ed1)

4. APIキーの作成ができたら、APIキーの使用制限を行います。ここに関しては任意なので実施しなくても良いですが、注意書きに書いてあるようにした方がいいです。
認証情報のリストから、先ほど作成したAPIキーを選択します。すると以下の画面に映ると思うので、下のAPIの制限からキーの制限を選択するとドロップダウンが出てくると思うので、Youtube Data API v3を選択します。これで、保存を選択し完了です。
![APIの制限](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/0cdaf171-e357-47d8-a026-acebe0629bbf)

## アプリケーションのダウンロードと準備
### ダウンロード
git cloneできる方はcloneする形で問題ありません。cloneできない方は、NEologdを導入した時と同じようにzipでダウンロードしてくる形でも問題ありません。

### 実行前の準備
実行前にスクリプト内部で書き換える必要がある箇所がいくつかあります。
1. api_config.yaml  
    最初にapi_config.yamlを書き換えます。api_config.yamlはyoutubeのapi-keyを保存するためのyamlファイルになっています。Youtube Data API V3で発行したAPIキーを以下の画像の*****の箇所に貼り付けます。
    ![スクリーンショット 2023-06-09 17 13 46](https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/a3344255-0dda-41e5-9a0a-f5fb5cad4578)
    api_config.yamlの編集はこれで終了です。保存して閉じてください。

2. src/create_plot/main.py
    create_plotフォルダー内のmain.pyに関してもMeCabのユーザー辞書を使用するために書き換える必要があります。これに関しては、windowsとmacで違います。
    1. windowsの場合  
        windowsの場合は、以下のコードが書いてある箇所を書き換えます。
        ```
        if os.name =='nt':
            spliter = MeCab.Tagger(r'-d "C:/Program Files (x86)/MeCab/dic/ipadic" -u "data/mecab_dictionaly/mecab-user-dict-seed.20200910.dic"')
        ```
        ```MeCab.Tagger```の括弧の中の ```r'-d "``` 以降に関してMeCabフォルダー内のipadicフォルダーを探して、右クリックでパスをコピーして貼り付けて書き換えてください。（基本的には、インストール先をいじっていない限りは、書いてある箇所にあると思いますので特に書き換える必要はないかもしれません。）  
        書き換えたのちに、NEologdの導入で作成したmecab-user-dict-seed.20200910.dicをdata/mecab_dictionaly内にコピーしてください。
        windowsに関してはこれで終了です。
    
    2. macの場合
        macの場合は、以下のコードが書いてある箇所を書き換えます。
        ```
        elif os.name =='posix':
            spliter = MeCab.Tagger(r'-d "macのmecab-ipadic-neologdのフォルダーパスを記入"')
        ```
        まず、macのフォルダーディレクトリーの中からmecab-ipadic-neologdフォルダーを探す必要があります。自分の場合は、anacondaを使って環境を構築してその中で色々な準備をしていたので、以下の場所にありました。
        ```
        /Users/ユーザー名/opt/anaconda3/lib/mecab/dic/mecab-ipadic-neologd
        ```
        このフォルダーを見つけたら、パスを ```macのmecab-ipadic-neologdのフォルダーパスを記入``` と書いてある箇所に貼り付けます。
        これでmacの準備は完了です。
    
## 実行方法と画面説明
### スクリプトの実行
ここまでの準備が完了したら、コマンドプロンプトを開きcomment_analysisフォルダー直下まで移動します。基本的には、コマンドプロンプトを開くとユーザーフォルダーにいるので、デスクトップにcomment_analysisフォルダーを配置している場合は、以下の順番でコマンドを実行していけば動くと思います。
```
> cd desktop/comment_analysis
> python management.py
```
これでブラウザーが開いて、サーバーが起動すると画面が表示されると思います。
開かなかった場合は、リロードしてみてそれでも無理な場合はエラーが発生してないか確認してください。

### 画面の説明と使用方法
#### 画面の説明（URL入力欄）
起動した直後には以下のような画面が表示されると思います。
<img width="1439" alt="スクリーンショット 2023-06-09 17 36 34" src="https://github.com/N-OKAMOTO1031/comment_analysis/assets/130206072/107a047d-71a1-417e-8244-a39f7a3d876a">
基本的には、デフォルトの設定値が入っていますが動画のURLだけ入力する必要があります。この項目には、解析対象の動画のURLを貼り付けてください。入力すると入力欄の右上にステータス情報が出るようになっています。それぞれのステータスは以下のような意味になっています。  

* This video is not live or you may have reached the daily comment acquisition limit.  
    動画がライブ動画でないもしくは、Youtube APIの一日の取得制限に達している場合に表示されます。
    また、

* Not Live, please check url  
    入力したURLの動画が、現在ライブ状態ではないことを表しています。ライブが終了してないかを確認してください。（待機所の状態でもコメントは取得可能です。）

* Now Live  
    入力したURLの動画が、ライブ状態であることを表しています。問題なく実行できます。

また、この項目が空欄の状態もしくはNow Live以外のステータスの状態ですと、設定完了ボタンを押した際にボタンの下に状況が表示されますので修正してください。

#### 画面の説明（再読み込みレート）
この項目は、コメントのロードもしくはプロットの更新の間隔を表しています。入力は秒単位で入力してください。  
グラフのロードに関しては、更新をすると拡大等がリセットされてしまうので、詳しくみたい場合にはグラフの更新間隔を長くしてください。変更した次のロードタイミングから適用されます。

#### 画面の説明（除外品詞の設定）
この項目は、分析する対象からどの品詞を除くかを設定します。基本的には、初期値として設定している名詞と動詞のみを解析対象とする形がいいと思います。また、全てを選択状態にするとグラフが更新されなくなります（これに関しては、エラーを内部処理で解決している状態なのでできればやらない方がいいと思います）。

#### 画面の説明（除外単語指定）
解析対象から除外したい単語を設定できます。単語を入力する際には半角のカンマ区切りで入力してください。（内部処理を見たら分かってしまうのですが、一応全角の空白、半角の空白、全角の読点でもなんとかなります。）

#### 画面説明（プロット画面）
プロット画面は以下の3種類に分かれていて上のタブで切り替えることができます。

* 単語出現頻度
    コメントの取得を開始してから、除外品詞及び除外単語を除いた単語がどれぐらい出てきたかを棒グラフで表します。また上側2つのドロップダウンのうち、左側でプロットを全体に対する割合にするか単純に個数にするかを選択でき、右側で表示する単語数を上位のいくつにするかを選択できます

* 共起ネットワーク
    共起ネットワークをプロットする画面になります。共起ネットワークとは、簡単にいうとある単語に対してどういう単語が前後で繋がっていることが多かったかを表しています。また、下側にサンバーストプロットも表示されこれは、それぞれの単語の共起ネットワークに基づくグルーピング結果になります。

* ワードクラウド
    ワードクラウドは、どういった単語が多く出てきているかを視覚的に表した図になります。この図の中で文字の大きさが大きいほど出現頻度が高く、小さいほど出現頻度が低くなります。

以上になっています。

#### 使用方法
使用方法の順番は以下となります。

1. 動画URL欄にURLを入力
2. ロードの間隔を変更する場合には変更
3. 