import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from modules.utils.label_wraplength import label_wraplength

class ProcessingMainApp:
  def __init__(self, root, base_path, exe_path):
    self.base_path = base_path
    self.exe_path = exe_path
    
    self.read_csvs()
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("MainApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "以下の実行ボタンを押すことで、点数の処理し結果を表示します。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=0)
    self.root.grid_rowconfigure(1, weight=0)
    self.root.grid_rowconfigure(2, weight=1)
    self.root.grid_rowconfigure(3, weight=0)
    
    ############config############
    self.check01 = tk.BooleanVar()
    self.check02 = tk.BooleanVar()
    self.check03 = tk.BooleanVar()
    
    self.frame_conf = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.frame_conf01 = tk.Frame(self.frame_conf)
    
    self.check01_box = ttk.Checkbutton(self.frame_conf01, variable=self.check01, command = self.judging)
    self.frame_checkbox01 = tk.Frame(self.frame_conf01)
    self.check01_text = self.lw.label_maker(self.frame_checkbox01, "バンドデータが正しく生成されていることを確認しましたか。")
    
    self.check02_box = ttk.Checkbutton(self.frame_conf01, variable=self.check02, command = self.judging)
    self.frame_checkbox02 = tk.Frame(self.frame_conf01)
    self.check02_text = self.lw.label_maker(self.frame_checkbox02, "採点項目データが正しく生成されていることを確認しましたか。")
    
    self.check03_box = ttk.Checkbutton(self.frame_conf01, variable=self.check03, command = self.judging)
    self.frame_checkbox03 = tk.Frame(self.frame_conf01)
    self.check03_text = self.lw.label_maker(self.frame_checkbox03, "採点データが正しく生成されていることを確認しましたか。")
    
    self.frame_conf02 = tk.Frame(self.frame_conf)
    
    self.label_threshold = self.lw.label_maker(self.frame_conf02, "最低審査数を指定してください。")
    self.entry_threshold = tk.Entry(self.frame_conf02)
    
    self.frame_conf.grid(row=1, column=0, sticky="ew")
    self.frame_conf01.grid(row=0, column=0, sticky="ew")
    self.frame_conf02.grid(row=1, column=0, sticky="ew")
    
    self.check01_box.grid(row=0, column=0)
    self.frame_checkbox01.grid(row=0, column=1, sticky="ew")
    self.check01_text.grid(row=0, column=0)
    
    self.check02_box.grid(row=1, column=0)
    self.frame_checkbox02.grid(row=1, column=1, sticky="ew")
    self.check02_text.grid(row=0, column=0)
    
    self.check03_box.grid(row=2, column=0)
    self.frame_checkbox03.grid(row=2, column=1, sticky="ew")
    self.check03_text.grid(row=0, column=0)
    
    self.label_threshold.grid(row=0, column=0)
    self.entry_threshold.grid(row=1, column=0)
    self.entry_threshold.bind("<KeyRelease>", self.judging)
    
    self.frame_conf.grid_columnconfigure(0, weight=1)
    self.frame_conf01.grid_columnconfigure(0, weight=0)
    self.frame_conf01.grid_columnconfigure(1, weight=1)
    self.frame_conf02.grid_columnconfigure(0, weight=0)
    
    ############log############
    self.frame_log = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.logbox = tk.Text(self.frame_log, state='disabled', borderwidth=5, wrap='word')
    self.yscroll = ttk.Scrollbar(self.frame_log, orient="vertical", command=self.logbox.yview)
    self.logbox.configure(yscrollcommand=self.yscroll.set)
    
    self.frame_log.grid(row=2, column=0, sticky="ewsn")
    self.logbox.grid(row=0, column=0, sticky="ewsn")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    self.frame_log.grid_rowconfigure(0, weight=1)
    self.frame_log.grid_columnconfigure(0, weight=1)
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_running = tk.Button(self.frame_button, text="実行", command=self.running)
    self.button_running.config(state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=3, column=0, sticky="ew")
    self.button_running.grid(row=0, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    self.frame_button.grid_rowconfigure(0, weight=3)
    self.frame_button.grid_rowconfigure(1, weight=1)
    
    self.lw.treatment()
  
  def judging(self, event=None):
    self.threshold = self.entry_threshold.get().strip().replace(" ", "").replace("　", "")
    self.entry_threshold.delete(0, tk.END)
    self.entry_threshold.insert(0, self.threshold)
    if self.check01.get() and self.check02.get() and self.check03.get():
      try:
        self.threshold = int(self.threshold)
        if self.threshold >= 0:
          self.button_running.config(state=tk.NORMAL)
          return
      except Exception:
        pass
    self.button_running.config(state=tk.DISABLED)
  
  def WriteToLog(self, msg):
    self.logbox['state'] = 'normal'
    
    if self.logbox.index('end-1c')!='1.0':
        self.logbox.insert('end', '\n')
    
    self.logbox.insert('end', msg)
    
    self.logbox.see(tk.END)
    
    self.logbox['state'] = 'disabled'
  
  def read_csvs(self):
    self.band_file_path = os.path.join(self.exe_path, "cache", "ScoreProcessorApp", "band.csv")
    self.item_file_path = os.path.join(self.exe_path, "cache", "ScoreProcessorApp", "item.csv")
    self.data_file_path = os.path.join(self.exe_path, "cache", "ScoreProcessorApp", "data.csv")
    
    try:
      self.df_band = pd.read_csv(self.band_file_path)
      self.df_band = self.df_band.drop('member', axis="columns")
    except Exception as e:
      messagebox.showerror("Error", f"バンドデータの読み込みに失敗しました:{e}")
      self.close_app(self)
      
    try:
      self.df_item = pd.read_csv(self.item_file_path)
    except Exception as e:
      messagebox.showerror("Error", f"採点項目データの読み込みに失敗しました:{e}")
      self.close_app(self)
      
    try:
      self.df_data_raw = pd.read_csv(self.data_file_path)
    except Exception as e:
      messagebox.showerror("Error", f"採点データの読み込みに失敗しました:{e}")
      self.close_app(self)
  
  def close_app(self):
      self.root.destroy()
  
  def running(self):
    df_data = self.df_data_raw.copy()
    item_list = []
    #傾斜配点の適用
    for item, weight in zip(self.df_item['item'], self.df_item['weight']):
      df_data[item] = df_data[item] * weight
      item_list.append(item)
    
    #合計点数の計算
    df_data['合計'] = df_data[self.df_item['item']].sum(axis=1)
    
    item_list = ['合計'] + item_list
    
    #審査員ごとの審査数の計算
    df_judge = pd.DataFrame(df_data['審査員名'].unique(), columns=['審査員名'])
    df_judge_count = df_data.groupby('審査員名')['表示バンド名'].count().reset_index()
    df_judge_count = df_judge_count.rename(columns={'表示バンド名': '審査員審査数'})
    df_judge = pd.merge(df_judge, df_judge_count, on='審査員名', how='left')
    
    #結果のDataFrameの作成
    df_result = pd.DataFrame(df_data['表示バンド名'].unique(), columns=['表示バンド名'])
    
    #審査員ごとの平均および標準偏差の計算
    def culc_values_for_judges(item):
      df_judge_mean = df_data.groupby('審査員名')[item].mean().reset_index()
      df_judge_mean = df_judge_mean.rename(columns={item: item+"_平均"})
      df_judge_std = df_data.groupby('審査員名')[item].std(ddof=0).reset_index()
      df_judge_std = df_judge_std.rename(columns={item: item+"_標準偏差"})
      _df_judge = pd.merge(df_judge, df_judge_mean, on='審査員名', how='left')
      _df_judge = pd.merge(_df_judge, df_judge_std, on='審査員名', how='left')
      
      return _df_judge
    
    def culc_scores(item):
      _df_data = df_data.copy()
      #偏差値の計算
      _df_data[item+'_偏差値'] = (df_data[item]-df_data[item+'_平均'])/_df_data[item+'_標準偏差']*10+50
      
      #バンドごとの偏差値の平均(スコア)の計算
      _df_result_item = _df_data.groupby('表示バンド名')[item+'_偏差値'].apply(
        lambda x: x.sort_values().iloc[1:-1].mean() if len(x) > 2 else x.mean()
      ).reset_index()
      _df_result_item = _df_result_item.rename(columns={item+'_偏差値': item+'_スコア'})
      
      _df_result = pd.merge(df_result, _df_result_item, on='表示バンド名', how='left')
      
      return _df_data, _df_result
    
    for item in item_list:
      df_judge = culc_values_for_judges(item)
    
    #審査員データを採点データに適用
    df_data = pd.merge(df_data, df_judge, on='審査員名', how='left')
    
    #審査員審査数が基準値未満の審査員のデータを除外
    df_data = df_data[df_data['審査員審査数']>=self.threshold]
    
    for item in item_list:
      df_data, df_result = culc_scores(item)
    
    df_result = pd.merge(self.df_band, df_result, right_on='表示バンド名' , left_on='name_on_form', how="left").drop(columns='name_on_form').rename(columns={'name': 'バンド名'})
    
    #バンドごとの審査数の計算
    _df_result_judge = df_data.groupby('表示バンド名')['審査員名'].count().reset_index()
    _df_result_judge = _df_result_judge.rename(columns={'審査員名': 'バンド審査数'})
    df_result = pd.merge(df_result, _df_result_judge, on='表示バンド名', how='left')
    
    #結果を順位で並べ替え
    df_result = df_result.sort_values(by='合計_スコア', ascending=False)
    
    self.WriteToLog("以下に処理の結果を表示します。")
    self.WriteToLog(f"{df_result}")
    try:
      log_dir = os.path.join(self.exe_path, "cache", "ScoreProcessorApp", "logs")
      path_data_raw = os.path.join(log_dir, "data_raw.csv")
      path_judge = os.path.join(log_dir, "judge.csv")
      path_data = os.path.join(log_dir, "data.csv")
      path_result = os.path.join(log_dir, "result.csv")
      
      self.WriteToLog(f"ログを出力します。")
      self.df_data_raw.to_csv(path_data_raw)
      self.WriteToLog(f"生データ:{path_data_raw}")
      df_judge.to_csv(path_judge)
      self.WriteToLog(f"審査員データ:{path_judge}")
      df_data.to_csv(path_data)
      self.WriteToLog(f"処理データ:{path_data}")
      df_result.to_csv(path_result)
      self.WriteToLog(f"結果:{path_result}")
    except Exception as e:
      self.WriteToLog(f"ログ出力に際しエラーが発生しました:{e}")
    
    self.button_running.config(state=tk.NORMAL)