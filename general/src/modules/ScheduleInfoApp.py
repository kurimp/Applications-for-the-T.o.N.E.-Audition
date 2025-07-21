import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import pandas as pd
from modules.utils.label_wraplength import label_wraplength
from datetime import datetime, timedelta

class ScheduleInfoApp:
  def __init__(self, root, base_path, exe_path):
    self.save_filepath=os.path.join(exe_path, "cache", "schedule.csv")
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("ScheduleInfoApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=0)
    self.root.grid_rowconfigure(1, weight=0)
    self.root.grid_rowconfigure(2, weight=1)
    self.root.grid_rowconfigure(3, weight=0)
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "開始時間を入力し実行すると、タイムテーブルが作成されます。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.frame_info.grid_columnconfigure(0, weight=1)
    
    ############config############
    self.frame_conf = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_conf = self.lw.label_maker(self.frame_conf, "タイムテーブルの開始時間を9:00:00のような形で入力してください。")
    self.frame_confbox = tk.Frame(self.frame_conf, relief="ridge")
    self.entry_conf = ttk.Entry(self.frame_confbox, width=10)
    self.entry_button = ttk.Button(self.frame_confbox, text="変更を保存", command=self.save_conf)
    self.entry_conf.insert(0, "9:00:00")
    self.label_status = self.lw.label_maker(self.frame_conf)
    self.frame_conf.grid(row=1, column=0, sticky="ew")
    self.label_conf.grid(row=0, column=0, sticky="ew")
    self.frame_confbox.grid(row=1, column=0, sticky="ew")
    self.entry_conf.grid(row=0, column=0)
    self.entry_button.grid(row=0, column=1)
    self.label_status.grid(row=2, column=0)
    
    ############tree############
    self.frame_tree = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.tree = ttk.Treeview(self.frame_tree, show="headings")
    self.frame_tree.grid(row=2, column=0, sticky="ewsn")
    self.tree.grid(row=0, column=0, sticky="ewsn")
    self.frame_tree.grid_rowconfigure(0, weight=1)
    self.frame_tree.grid_columnconfigure(0, weight=1)
    
    self.xscroll = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
    self.yscroll = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
    self.tree.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
    self.xscroll.grid(row=1, column=0, sticky="ew")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_open = tk.Button(self.frame_button, text="CSVを開く", command=self.open_csv)
    self.button_save = tk.Button(self.frame_button, text="CSVを保存", command=self.save_csv, state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=3, column=0, sticky="ew")
    self.button_open.grid(row=0, column=0, sticky="ew")
    self.button_save.grid(row=0, column=1, sticky="ew")
    self.button_close.grid(row=1, column=0, columnspan=2, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    self.frame_button.grid_columnconfigure(1, weight=1)
    
    self.load_initial_csv()
    self.lw.treatment()
  
  def save_conf(self):
    self.value = self.entry_conf.get()
    self.value = self.value.strip().replace(" ", "").replace("　", "")
    self.entry_conf.delete(0, tk.END)
    self.entry_conf.insert(0, self.value)
    
    if self.validate_custom_format(self.value):
      self.initialstatus = False
      self.label_status.config(text="成功しました。", foreground="green")
      self.set_times()
      self.savestatus = False
    else:
      self.label_status.config(text="不正な入力です。", foreground="red")
      return
  
  def validate_custom_format(self, value):
    try:
      self.whole_start_time = datetime.strptime(value, '%H:%M:%S')
    except ValueError:
      return False
    else:
      return True
  
  def display_data_in_treeview(self, df):
    for item in self.tree.get_children():
      self.tree.delete(item)
    
    if df.empty:
      return
    
    self.tree["columns"] = list(df.columns)
    self.tree["show"] = "headings"
    
    default_font = tkFont.Font()
    
    for col in df.columns:
      self.tree.heading(col, text=col)
      
      header_width = default_font.measure(col)
      
      max_data_width = 0
      if not df[col].empty:
        max_data_width = df[col].astype(str).apply(default_font.measure).max()
      
      column_width = max(header_width, max_data_width) + 20
      
      self.tree.column(col, width=column_width, anchor="w")
    
    for index, row in df.iterrows():
      self.tree.insert("", "end", iid=index, values=list(row))
    
    if self.df.iloc[1, 1] == "":
      self.button_save.config(state=tk.DISABLED)
      self.table_correct = False
    else:
      self.button_save.config(state=tk.NORMAL)
      self.table_correct = True
  
  def load_initial_csv(self):
    self.initialstatus = True
    if os.path.exists(self.save_filepath):
      self.read_filepath = self.save_filepath
      self.read_csv(self.read_filepath)
    self.savestatus = True
  
  def open_csv(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      self.read_filepath = filepath
    self.read_csv(self.read_filepath)
    self.savestatus = False
    self.initialstatus = False
  
  def read_csv(self, filepath):
    def preprocess_dataframe(df):
      df = df.fillna("")
      if "time_sta" not in df.columns:
        df.insert(0, "time_sta", "")
      if "time_fin" not in df.columns:
        df.insert(1, "time_fin", "")
      
      return df
    
    try:
      df_raw = pd.read_csv(filepath)
      
      if not("duration" in df_raw.columns)*("item" in df_raw.columns):
        messagebox.showerror("Error", f"ファイルの形式が不正です。")
        return
      
      self.df = preprocess_dataframe(df_raw.copy())
        
      self.set_times()
      
    except Exception as e:
      messagebox.showerror("Error", f"ファイルを読み込めませんでした:{e}")
  
  def set_times(self):
    if self.initialstatus:
      self.display_data_in_treeview(self.df)
      return
      
    if self.whole_start_time is None:
      self.display_data_in_treeview(self.df)
      return
    time_start = []
    time_finish = []
    sta = self.whole_start_time
    for duration in self.df['duration']:
      time_start.append(sta.time())
      
      try:
        duration = timedelta(minutes=int(str(duration).strip()))
      except ValueError:
        messagebox.showerror("エラー", "duration列の値が全て数値であることを確認してください。")
        return
      
      fin = sta + duration
      sta = fin
      time_finish.append(fin.time())
    
    self.df["time_sta"] = time_start
    self.df["time_fin"] = time_finish
    
    self.display_data_in_treeview(self.df)
  
  def save_csv(self):
    try:
      self.df.to_csv(self.save_filepath, index=False, encoding='utf-8')
      self.label_status.config(text="保存しました！", foreground="green")
      self.savestatus = True
    except Exception as e:
      self.label_status.config(text=f"保存に失敗しました:{e}")
      
  def close_app(self):
    if self.savestatus:
      self.root.destroy()
      return
    
    if not self.table_correct:
      select_close = messagebox.askokcancel("確認", "表が未完成のため保存できません。保存せずに終了しますか？")
      if select_close:
        self.root.destroy()
      return
    
    select_close = messagebox.askyesnocancel("確認", "変更を保存しますか？")
    if select_close == None:
      return
    elif select_close:
      self.save_csv()
      self.root.destroy()
    elif not select_close:
      self.root.destroy()
    return