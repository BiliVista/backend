from snownlp import SnowNLP, sentiment


def get_comment_score(comment):
    sentiment.load("model/MovieComment.marshal")
    s = SnowNLP(comment)
    return s.sentiments

if __name__ == "__main__":    
    print("这个电影真的太好看了！",get_comment_score("这个电影真的太好看了！"))
    print("byd,真唐",get_comment_score("byd,真唐"))
    print("今天天气真好！",get_comment_score("今天天气真好！"))