from snownlp import SnowNLP, sentiment


def get_comment_score(comment):
    sentiment.load("libs/Model/MovieComment.marshal")
    s = SnowNLP(comment)
    return s.sentiments

if __name__ == "__main__":    
    print(get_comment_score("这个电影真的太好看了！"))
    print(get_comment_score("byd"))
    print(get_comment_score("今天天气真好！"))