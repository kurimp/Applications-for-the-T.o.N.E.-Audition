import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import re
import pandas as pd
import numpy as np
from datetime import datetime, time as dt_time, timedelta
from utils.label_wraplength import label_wraplength
import random
import time
import csv
import ast
import threading

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MainApp:
  def __init__(self, root):
    self.band_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "data", "band.csv")
    self.sche_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "data", "schedule.csv")
    
    self.df_band = pd.read_csv(self.band_file_path)
    self.df_sche = pd.read_csv(self.sche_file_path)
    
    self.df_band = self.df_band.fillna('')

    self.df_band['unavailable_time'] = [[cell] for cell in self.df_band['unavailable_time']]
    self.df_band['member'] = [ast.literal_eval(cell) for cell in self.df_band['member']]
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("MainApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "以下の実行ボタンを押すことで、タイムテーブルの作成を試みます。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=0)
    self.root.grid_rowconfigure(1, weight=0)
    self.root.grid_rowconfigure(2, weight=0)
    self.root.grid_rowconfigure(3, weight=1)
    self.root.grid_rowconfigure(4, weight=0)
    
    ############config############
    self.check01 = tk.BooleanVar()
    self.check02 = tk.BooleanVar()
    
    self.frame_conf = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.frame_conf01 = tk.Frame(self.frame_conf)
    self.frame_conf02 = tk.Frame(self.frame_conf)
    
    self.check01_box = ttk.Checkbutton(self.frame_conf01, variable=self.check01, command = self.judging)
    self.frame_checkbox01 = tk.Frame(self.frame_conf01)
    self.check01_text = self.lw.label_maker(self.frame_checkbox01, "band.csvが正しく生成されていることを確認しましたか。")
    
    self.check02_box = ttk.Checkbutton(self.frame_conf01, variable=self.check02, command = self.judging)
    self.frame_checkbox02 = tk.Frame(self.frame_conf01)
    self.check02_text = self.lw.label_maker(self.frame_checkbox02, "schedule.csvが正しく生成されていることを確認しましたか。")
    
    self.frame_checkbox03 = tk.Frame(self.frame_conf02)
    self.check03_text = self.lw.label_maker(self.frame_checkbox03, "最大試行回数を整数で入力してください。")
    self.check03_entry = tk.Entry(self.frame_conf02, width=10)
    self.check03_entry.bind("<KeyRelease>", self.judging)
    self.check03_entry.insert(0, 100000000)
    
    self.frame_conf.grid(row=1, column=0, sticky="ew")
    self.frame_conf01.grid(row=0, column=0, sticky="ew")
    
    self.check01_box.grid(row=0, column=0)
    self.frame_checkbox01.grid(row=0, column=1, sticky="ew")
    self.check01_text.grid(row=0, column=0)
    
    self.check02_box.grid(row=1, column=0)
    self.frame_checkbox02.grid(row=1, column=1, sticky="ew")
    self.check02_text.grid(row=0, column=0)
    
    self.frame_conf02.grid(row=1, column=0, sticky="ew")
    
    self.frame_checkbox03.grid(row=0, column=1, sticky="ew")
    self.check03_text.grid(row=0, column=0)
    self.check03_entry.grid(row=0, column=0)
    
    self.frame_conf.grid_columnconfigure(0, weight=1)
    self.frame_conf01.grid_columnconfigure(0, weight=0)
    self.frame_conf01.grid_columnconfigure(1, weight=1)
    self.frame_conf02.grid_columnconfigure(0, weight=0)
    self.frame_conf02.grid_columnconfigure(1, weight=1)
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    self.frame_status.grid(row=2, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
    ############log############
    self.frame_log = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.logbox = tk.Text(self.frame_log, state='disabled', borderwidth=5, wrap='word')
    self.yscroll = ttk.Scrollbar(self.frame_log, orient="vertical", command=self.logbox.yview)
    self.logbox.configure(yscrollcommand=self.yscroll.set)
    
    self.frame_log.grid(row=3, column=0, sticky="ewsn")
    self.logbox.grid(row=0, column=0, sticky="ewsn")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    self.frame_log.grid_rowconfigure(0, weight=1)
    self.frame_log.grid_columnconfigure(0, weight=1)
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_running = tk.Button(self.frame_button, text="実行", command=self.start_running_thread)
    self.button_running.config(state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=4, column=0, sticky="ew")
    self.button_running.grid(row=0, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    self.frame_button.grid_rowconfigure(0, weight=3)
    self.frame_button.grid_rowconfigure(1, weight=1)
    
    self.lw.treatment()
  
  def writeToLog(self, msg):
    
    self.logbox['state'] = 'normal'
    
    if self.logbox.index('end-1c')!='1.0':
        self.logbox.insert('end', '\n')
    
    self.logbox.insert('end', msg)
    
    self.logbox.see(tk.END)
    
    self.logbox['state'] = 'disabled'
  
  def judging(self, event=None):
    self.maximum_attempts = self.check03_entry.get().strip().replace(" ", "").replace("　", "")
    self.check03_entry.delete(0, tk.END)
    self.check03_entry.insert(0, self.maximum_attempts)
    if self.check01.get() and self.check02.get():
      try:
        self.maximum_attempts = int(self.maximum_attempts)
        if self.maximum_attempts>0:
          self.button_running.config(state=tk.NORMAL)
          return
      except Exception:
        pass
    self.button_running.config(state=tk.DISABLED)
  
  def give_num(self, n):
    num = np.arange(0, n, 1)
    random.shuffle(num)
    return num

  def clean_list(self, input_list):
    cleaned_items = []
    for item in input_list:
      if item is not None and str(item).strip() != '':
        cleaned_items.append(str(item).strip())
    return cleaned_items

  def has_common_elements(self, list1, list2):
    cleaned_list1 = self.clean_list(list1)
    cleaned_list2 = self.clean_list(list2)
    
    set1 = set(cleaned_list1)
    set2 = set(cleaned_list2)

    common_elements_set = set1 & set2
    
    return len(common_elements_set) > 0
  
  def time_judge(self, res):
    i = 0
    for band in res:
      i += 1
      block_start_time = self.df_sche[self.df_sche['item']==str(i)]['time_sta'].iloc[0]
      block_finish_time = self.df_sche[self.df_sche['item']==str(i)]['time_fin'].iloc[0]
      block_start_time = datetime.strptime(block_start_time, '%H:%M:%S').time()
      block_finish_time = datetime.strptime(block_finish_time, '%H:%M:%S').time()
      unavailable_time = self.df_band[self.df_band['name']==band[0]]['unavailable_time'].iloc[0]
      unavailable_time = [m.strip() for m in unavailable_time if m.strip()]
      unavailable_time = self.convert_time_strings_to_time_tuples(unavailable_time)
      status = self.is_time_frame_available(block_start_time, block_finish_time, unavailable_time)
      if not status:
        return False
    return True

  def is_time_frame_available(self, start_time: dt_time, end_time: dt_time, unavailable_slots: list[tuple[dt_time, dt_time]]):
    # 確認したい時間枠が有効か（開始時刻が終了時刻より前か）をチェック
    if start_time >= end_time:
      raise ValueError("時間枠の開始時刻は終了時刻より前である必要があります。")
    
    for unavailable_start, unavailable_end in unavailable_slots:
      # 参加不可能な時間帯が有効か（開始時刻が終了時刻より前か）をチェック
      if unavailable_start >= unavailable_end:
        raise ValueError(f"参加不可能な時間帯の開始時刻が終了時刻より前ではありません: ({unavailable_start}, {unavailable_end})")
      
      # 重複の条件:
      # (A.start <= B.end) and (A.end >= B.start)
      # ここではAが確認したい時間枠、Bが参加不可能な時間帯
      if (start_time < unavailable_end) and (end_time > unavailable_start):
        return False  # 重複が見つかった場合
  
    return True  # 重複が見つからなかった場合
  
  def convert_time_strings_to_time_tuples(self, unavailable_slots_str: list[str]) -> list[tuple[dt_time, dt_time]]:
    converted_slots = []
    for slot_group_str in unavailable_slots_str:
      if not slot_group_str:
        continue
      individual_slot_strings = [s.strip() for s in slot_group_str.split(',') if s.strip()]

      for slot_str in individual_slot_strings:
        start_time_str, end_time_str = slot_str.split('-')
        parsed_start_time = datetime.strptime(start_time_str.strip(), '%H:%M:%S').time()
        parsed_end_time = datetime.strptime(end_time_str.strip(), '%H:%M:%S').time()
        converted_slots.append((parsed_start_time, parsed_end_time))
    
    return converted_slots
  
  def running(self):
    bandlist = []
    for index, row in self.df_band.iterrows():
      band_name = row['name']
      members = [m.strip() for m in row['member'] if m.strip()]
      bandlist.append([band_name, members])
    
    self.count = 0
    
    start = time.time()
    
    times = np.zeros(len(bandlist))
    
    self.exit_condition = False
    
    while self.count < self.maximum_attempts:
      self.count += 1
      if self.count % 1000000 == 0:
        now = time.time()
        self.elapsed_time = now - start
        self.root.after(0, lambda: self.writeToLog(f"{self.count}回目の試行。経過時間は{self.elapsed_time:.1f}秒。"))
      
      num = self.give_num(len(bandlist))
      res = []
      j = 0
      for i in num:
        res.append(bandlist[i])
        if j != 0:
          status = self.has_common_elements(res[j-1][1], res[j][1])
          if status == True:
            break
        j += 1
      times[j-1] += 1
      if (j == len(num)) and self.time_judge(res):
        self.exit_condition = True
        break
    
    now = time.time()
    self.elapsed_time = now - start
    
    if self.exit_condition:
      self.root.after(0, lambda: self.writeToLog(f"並べ替えが終了しました。やったね。"))
      self.root.after(0, lambda: self.writeToLog("-"*30))
      for item in res:
        self.root.after(0, lambda band_name=item[0]: self.writeToLog(band_name))
        self.root.after(0, lambda: self.writeToLog(""))
      self.root.after(0, lambda: self.writeToLog("-"*30))
    elif not self.exit_condition:
      self.root.after(0, lambda: self.writeToLog(f"条件に合う組み合わせを見つけるのに失敗しました。残念。"))
    self.root.after(0, lambda: self.writeToLog(f"試行回数は{self.count}回。経過時間は{self.elapsed_time:.1f}秒。"))
    
    number = np.arange(1, len(times)+1, 1)
    
    output_folder_path = '../../output/'
    output_file_name = "result_"+datetime.now().strftime('%y%m%d%H%M%S')+".csv"
    
    os.makedirs(output_folder_path, exist_ok=True)
    
    output_folder_path = os.path.join(output_folder_path, output_file_name)
    
    with open(output_folder_path, 'w', encoding='utf-8') as out:
      out.write("number\t"
                "count")
      for i in range(len(times)):
        out.write(f"\n{number[i]}\t"
                  f"{times[i]:.1f}")
    
    self.button_running.config(state=tk.NORMAL)
  
  def start_running_thread(self):
    self.button_running.config(state=tk.DISABLED)
    self.root.after(0, lambda: self.writeToLog("処理を開始しました。"))
    
    self.running_thread = threading.Thread(target=self.running)
    self.running_thread.daemon = True
    self.running_thread.start()
  
  def close_app(self):
      self.root.destroy()

if __name__=="__main__":
  root = tk.Tk()
  app = MainApp(root)
  root.mainloop()