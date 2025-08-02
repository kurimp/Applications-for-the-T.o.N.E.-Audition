import csv
import os
from datetime import datetime
from googleapiclient.discovery import build
import configparser
from tqdm import tqdm
import pandas as pd
import random

#カレントディレクトリの移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#APIキー、チャンネルID、プレイリストIDの指定
API_KEY = "AIzaSyDhOPU1iHOb--4yVP3lqtnSYUQ_t6CyOtw"
channel_id = 'UCz7sisH24s3iRlVUXwJ2khA'
playlist_id = "PLfjdHEP-_y_a07TyiAKadzoRByFcvtjvi"

#YouTube APIの立ち上げ
youtube = build('youtube', 'v3', developerKey=API_KEY)

#チャンネル情報の取得
channel_response = youtube.channels().list(id=channel_id, part='snippet,contentDetails').execute()
channel_title = channel_response['items'][0]['snippet']['title']

#CSVファイルの作成
folder_name = os.path.join("cache", "CommentCollectionApp")
savefile_path = os.path.join(folder_name, "Comments.csv")
banddata_path = os.path.join(folder_name, "bandlist.csv")

#CSVファイルへの書き込み
with open(savefile_path, mode='w', newline='', encoding='utf-8') as file:
  writer = csv.writer(file)
  #タイトルの書き込み
  writer.writerow(["Number", "Name", "Video ID", "Band ID", "Score", "judge", "Title", "Comments"])
  
  df1 = pd.read_csv(banddata_path)
  
  for i in tqdm(range(0, len(df1))):
    #プレイリストデータから動画IDを１つ取得
    number = df1.at[i, "Number"]
    name = df1.at[i, "Name"]
    video_id = df1.at[i, 'Video ID']
    band_id = df1.at[i, 'Band ID']
    score = df1.at[i, "Score"]
    judge = df1.at[i, "judge"]
    #当該動画の詳細情報を取得
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_details = youtube.videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()['items'][0]
    #当該動画のコメントを取得
    comment_threads = youtube.commentThreads().list(videoId=video_id, part = "snippet", maxResults = 300, textFormat = "plainText").execute()
    #動画のタイトル、コメントを取得
    title = video_details['snippet']['title']
    comment = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comment_threads.get('items', [])]
    
    random.shuffle(comment)
    
    #コメントを改行及び横棒で区切る処理の実施
    i = 0
    text = ""
    for comment_text in comment:
      if "講評はこちらから投稿してください！" not in comment_text:
        if i == 0:
          text = comment_text
        else:
          text = text + "\n--------------------\n" + comment_text
      i = i + 1
    #動画タイトル、動画ID、コメントの書き込み
    writer.writerow([number, name, video_id, band_id, score, judge, title, text])