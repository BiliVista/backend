from snownlp import SnowNLP, sentiment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Modelpath="model/MovieComment.marshal"

def get_comment_score(comment):
    s = SnowNLP(comment)
    return s.sentiments


def Calculate_sentiment(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        comment = f.readlines()
    # Convert to DataFrame
    df = pd.DataFrame(comment, columns=['comment'])
    # Drop rows with missing values
    df['comment'] = df['comment'].fillna('')
    df = df.dropna()
    df['sentiment'] = df['comment'].apply(lambda x: SnowNLP(x).sentiments)
    return df


def Calculate_sentiment2(file_path):
    # Read the xlsx file
    comment = pd.read_excel(file_path)
    # All [like] +1
    comment['like'] = comment['like'] + 1
    # Convert to DataFrame
    df = comment
    # Drop rows with missing values
    df['comment'] = df['comment'].fillna('')
    df = df.dropna()
    df['sentiment'] = df['comment'].apply(lambda x: SnowNLP(x).sentiments)
    return df


def draw_hist(df):
    df['sentiment'].hist(bins=5)
    plt.show()


if __name__ == "__main__":
    sentiment.load(Modelpath)
    # print("这个电影真的太好看了！",get_comment_score("这个电影真的太好看了！"))
    # print("byd,真唐",get_comment_score("byd,真唐"))
    # print("今天天气真好！",get_comment_score("今天天气真好！"))
    df1 = Calculate_sentiment2('comment.xlsx')
    # Sum of all [like]
    sum_like = df1['like'].sum()
    # sentiment times like
    df1['sentiment_like'] = df1['sentiment'] * df1['like']
    # sentiment times like sum
    mean_sentiment = df1['sentiment_like'].sum() / sum_like
    print(mean_sentiment)
    # Export xlsx file
    # print(df1.head(10))
    # df1.to_excel("comment.xlsx", index=False)
    # # df2 = Calculate_sentiment('danmu.txt')
    # print(df1['sentiment'].mean())
    # # print(df2['sentiment'].mean())
    draw_hist(df1)
    # # draw_hist(df2)
    # print(df1[(df1['sentiment'] < 0.1)].head(10))
    # print(df2[(df2['sentiment'] <0.1)].head(10))
    # print(df1[(df1['sentiment'] > 0.9)].head(10))
    # print(df2[(df2['sentiment'] > 0.9)].head(10))
    # print(df[(df['sentiment'] > 0.9)])
