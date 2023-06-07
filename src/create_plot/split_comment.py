def get_specified_word(comment, spliter, except_part_of_speech_list, except_word_list):
    """
    渡した文章を分割し、指定したワードおよび品詞のものを取り除く関数
    
    Parameters:
    ---------------------------------
    comment: str
        分離対象のコメント

    spliter: MeCab.Tagger
        MeCabの分かち書き用のtagger

    except_part_of_speech_list: list of str
        除外対象の品詞のリスト

    except_word_list: list of str
        除外対象の単語のリスト

    Return:
    ---------------------------------
    word_list: list of str
        MeCabで分割し、必要なwordのみにしたリスト

    """

    word_list = get_word(comment, spliter)
    part_of_speech_list = get_part_of_speech(comment, spliter)
    word_list = [word_list[i] for i in range(len(part_of_speech_list)) if part_of_speech_list[i] not in except_part_of_speech_list + ['']]
    word_list = [i for i in word_list if i not in except_word_list]
    return word_list
    


def get_word(comment, spliter):
    """
    渡した文章を分割し、wordのみを取得する関数
    
    Parameters:
    ---------------------------------
    comment: str
        分離対象のコメント

    spliter: MeCab.Tagger
        MeCabの分かち書き用のtagger

    Return:
    ---------------------------------
    word_list: list of str
        MeCabで分割し、wordのみを取得したリスト

    """
    word_list = spliter.parse(comment)
    word_list = word_list.replace('\n', '\t').split('\t')[0::2]
    return word_list

def get_part_of_speech(comment, spliter):
    """
    渡した文章を分割し、品詞のみを取得する関数
    
    Parameters:
    ---------------------------------
    comment: str
        分離対象のコメント

    spliter: MeCab.Tagger
        MeCabの分かち書き用のtagger

    Return:
    ---------------------------------
    part_of_speech_list: list of str
        MeCabで分割し、品詞のみを取得したリスト

    """
    part_of_speech_list = spliter.parse(comment)
    part_of_speech_list = [i.split(',')[0] for i in part_of_speech_list.replace('\n', '\t').split('\t')[1::2]]
    return part_of_speech_list