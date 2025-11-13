import csv
from googleapiclient.discovery import build
from tqdm import tqdm
import pandas as pd
import random
from modules.utils.label_wraplength import label_wraplength
import tkinter as tk
from tkinter import ttk, filedialog

class CommentCollectionApp:
  def __init__(self, root, base_dir, cache_dir):
    self.base_dir = base_dir
    self.cache_dir = cache_dir
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("CommentCollectionApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "YouTubeからコメントを取得し、Word差し込み文章機能のためのCSVを作成します。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=0)
    self.root.grid_rowconfigure(1, weight=0)
    self.root.grid_rowconfigure(2, weight=0)
    self.root.grid_rowconfigure(3, weight=1)
    self.root.grid_rowconfigure(4, weight=0)
    
    ############config############
    self.frame_conf01 = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_conf01 = self.lw.label_maker(self.frame_conf01, "APIキーを入力してください。")
    self.entry_conf01 = tk.Entry(self.frame_conf01)
    self.entry_conf01.bind("<KeyRelease>", self.judging)
    
    self.frame_conf01.grid(row=1, column=0, sticky="ew")
    self.label_conf01.grid(row=0, column=0, sticky="ew")
    self.entry_conf01.grid(row=1, column=0, sticky="ew")
    
    self.frame_conf01.grid_columnconfigure(0, weight=1)
    
    self.frame_conf02 = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_conf02 = tk.Button(self.frame_conf02, text="データCSVを開く", command=self.open_csv)
    
    self.frame_conf02.grid(row=2, column=0, sticky="ew")
    self.button_conf02.grid(row=0, column=0, sticky="ew")
    
    self.frame_conf02.grid_columnconfigure(0, weight=1)
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    self.frame_status.grid(row=3, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
    ############log############
    self.frame_log = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.logbox = tk.Text(self.frame_log, state='disabled', borderwidth=5, wrap='word')
    self.yscroll = ttk.Scrollbar(self.frame_log, orient="vertical", command=self.logbox.yview)
    self.logbox.configure(yscrollcommand=self.yscroll.set)
    
    self.frame_log.grid(row=4, column=0, sticky="ewsn")
    self.logbox.grid(row=0, column=0, sticky="ewsn")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    self.frame_log.grid_rowconfigure(0, weight=1)
    self.frame_log.grid_columnconfigure(0, weight=1)
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_running = tk.Button(self.frame_button, text="実行", command=self.treatment)
    self.button_running.config(state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=5, column=0, sticky="ew")
    self.button_running.grid(row=0, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    self.frame_button.grid_rowconfigure(0, weight=3)
    self.frame_button.grid_rowconfigure(1, weight=1)
    
    self.lw.treatment()
    self.status_read_data = False
  
  def WriteToLog(self, msg):
    self.logbox['state'] = 'normal'
    if self.logbox.index('end-1c') != '1.0':
      self.logbox.insert('end', '\n')
    self.logbox.insert('end', msg)
    self.logbox.see(tk.END)
    self.logbox['state'] = "disabled"
  
  def judging(self, event=None):
    self.APIkey = self.entry_conf01.get().strip().replace(" ", "").replace("　", "")
    self.entry_conf01.delete(0, tk.END)
    self.entry_conf01.insert(0, self.APIkey)
    if (self.APIkey != "")&self.status_read_data:
      self.button_running.config(state=tk.NORMAL)
  
  def open_csv(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      self.read_csv(filepath)
  
  def read_csv(self, filepath):
    try:
      self.df_data = pd.read_csv(filepath)
      self.WriteToLog("読み込んだデータCSVは以下です。")
      self.WriteToLog(self.df_data)
      
      data_columns = ['number','name','videoID','score','judge','bandID']
      
      if not set(data_columns).issubset(self.df_data):
        self.WriteToLog(f"データCSVが条件を満たしていません。")
        self.status_read_data = False
        self.judging()
        return
      self.status_read_data = True
      self.judging()
    except Exception as e:
      self.WriteToLog(f"読み込みの際にエラーが発生しました:{e}")
      self.status_read_data = False
      self.judging()
  
  def treatment(self):
    try:
      filepath = filedialog.asksaveasfilename(title="CSVファイルの保存先を指定", initialfile="comments.csv",defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
      if filepath:
        savefile_path = filepath
      else:
        return
      
      youtube = build('youtube', 'v3', developerKey=self.APIkey)
      
      #CSVファイルへの書き込み
      with open(savefile_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #タイトルの書き込み
        writer.writerow(["number", "name", "videoID", "bandID", "score", "judge", "title", "comments"])
        
        for i in tqdm(range(0, len(self.df_data))):
          #プレイリストデータから動画IDを１つ取得
          number = self.df_data.at[i, "number"]
          name = self.df_data.at[i, "name"]
          video_id = self.df_data.at[i, 'videoID']
          band_id = self.df_data.at[i, 'bandID']
          score = self.df_data.at[i, "score"]
          judge = self.df_data.at[i, "judge"]
          
          #当該動画の詳細情報を取得
          video_response = youtube.videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()
          if not video_response['items']:
            self.WriteToLog(f"{name}の詳細情報が見つかりませんでした。")
            continue
          video_details = video_response['items'][0]
          
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
      
      self.WriteToLog(f"Word差し込み用のCSVを{savefile_path}として保存しました。")
    except Exception as e:
      self.WriteToLog(f"Word差し込み用のCSVの作成に失敗しました:{e}")
  
  def close_app(self):
      self.root.destroy()