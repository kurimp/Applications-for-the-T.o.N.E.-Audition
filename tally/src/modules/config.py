import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import re
import pandas as pd
import numpy as np
from utils.label_wraplength import label_wraplength

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class BandInfoApp:
  def __init__(self, root):
    self.save_filepath=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "band.csv")
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("BandInfoApp")
    self.root.geometry("800x600")
    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "バンド一覧、および祭典項目一覧をインポートします。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.frame_info.grid_columnconfigure(0, weight=1)
    
    ############contents############
    self.frame_cont = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.frame_cont.grid(row=1, column=0, sticky="ewsn")
    
    ############band############
    self.frame_band = tk.Frame(self.frame_cont, padx=10, pady=10, bd=1, relief="ridge")
    self.button_band = tk.Button(self.frame_band, text="バンドCSVを開く", command=self.open_csv_band)
    
    self.box_band = tk.Text(self.frame_band, state='disabled', borderwidth=5, wrap='word')
    self.yscroll_band = ttk.Scrollbar(self.frame_band, orient="vertical", command=self.box_band.yview)
    self.box_band.configure(yscrollcommand=self.yscroll_band.set)
    
    self.frame_band.grid(row=0, column=0, sticky="ewsn")
    self.button_band.grid(row=0, column=0, sticky="ew")
    self.box_band.grid(row=1, column=0, sticky="ewsn")
    self.yscroll.grid(row=1, column=1, sticky="sn")
    
    ############item############
    self.frame_item = tk.Frame(self.frame_cont, padx=10, pady=10, bd=1, relief="ridge")
    self.button_item = tk.Button(self.frame_band, text="バンドCSVを開く", command=self.open_csv_band)
    
    self.box_item = tk.Text(self.frame_band, state='disabled', borderwidth=5, wrap='word')
    self.yscroll_band = ttk.Scrollbar(self.frame_band, orient="vertical", command=self.box_band.yview)
    self.box_band.configure(yscrollcommand=self.yscroll_band.set)
    
    self.frame_band.grid(row=0, column=0, sticky="ewsn")
    self.button_band.grid(row=0, column=0, sticky="ew")
    self.box_band.grid(row=1, column=0, sticky="ewsn")
    self.yscroll.grid(row=1, column=1, sticky="sn")
    
    
    
    self.frame_tree = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.tree = ttk.Treeview(self.frame_tree, show="headings")
    self.frame_tree.grid(row=1, column=0, sticky="ewsn")
    self.tree.grid(row=0, column=0, sticky="ewsn")
    self.tree.bind("<Double-1>", self.on_cell_double_click)
    self.frame_tree.grid_rowconfigure(0, weight=1)
    self.frame_tree.grid_columnconfigure(0, weight=1)
    
    self.xscroll = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
    self.yscroll = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
    self.tree.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
    self.xscroll.grid(row=1, column=0, sticky="ew")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    self.frame_status.grid(row=2, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
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
  
  def on_cell_double_click(self, event):
    region = self.tree.identify("region" ,event.x, event.y)
    if region == "heading":
      return
    
    item_id = self.tree.identify_row(event.y)
    column_id = self.tree.identify_column(event.x)
    
    column_index = int(column_id.replace("#", "")) - 1
    col_name = self.tree["columns"][column_index]
    
    if col_name != "unavailable_time":
      self.label_status.config(text="unavailable_time列のみ編集可能です。", foreground="orange")
      self.root.after(1000, lambda: self.label_status.config(text=""))
      return
    
    row_index = int(item_id)
    
    current_values = list(self.tree.item(item_id, "values"))
    if column_index >= len(current_values):
      return
    
    current_value = current_values[column_index]
    
    x, y, width, height = self.tree.bbox(item_id, column_id)
    
    if x is None:
      return
    
    editor = ttk.Entry(self.tree, width=width)
    editor.place(x=x, y=y, width=width, height = height)
    editor.insert(0, current_value)
    editor.focus_set()
    editor.grab_set()
    
    #選択状態が解除された時の処理
    def on_entry_lost_focus(event):
      new_value = editor.get()
      new_value = new_value.strip().replace(" ", "").replace("　", "")
      
      updated_values = list(self.tree.item(item_id, "values"))
      updated_values[column_index] = new_value
      self.tree.item(item_id, values=updated_values)
      
      col_name = self.tree["columns"][column_index]
      self.df.loc[row_index, col_name] = new_value
      
      editor.grab_release()
      editor.destroy()
      
      self.savestatus = False
      
      self.scanning()
      
    self.root.after(50, lambda: editor.bind("<FocusOut>", on_entry_lost_focus))
    self.root.after(50, lambda: editor.bind("<Return>", on_entry_lost_focus))
  
  def scanning(self):
    i = 0
    for value in self.df["unavailable_time"]:
      if not self.validate_custom_format(value):
        self.list_status[i] = False
      else:
        self.list_status[i] = True
      i += 1
  
    if all(self.list_status):
      self.button_save.config(state=tk.NORMAL)
    else:
      self.button_save.config(state=tk.DISABLED)
    
    error_found = False
    for i in range(0, len(self.list_status)):
      if self.list_status[i]:
        pass
      else:
        self.label_status.config(text="unavailable_time列の不正な入力です:"+self.list_bandname[i], foreground="red")
        error_found = True
        break
    
    if not error_found:
      self.label_status.config(text="unavailable_time列は正しく入力されています！", foreground="green")
  
  def validate_custom_format(self, new_value):
    def extract_values_from_format(input_string):
      if not isinstance(input_string, str):
        return []
      input_string = input_string.strip().replace(" ", "").replace("　", "")
      
      if not input_string:
        return []
      
      pattern = re.compile(r"(?:,)?([^,]+)")
      
      extracted_list = []
      matches = pattern.finditer(input_string)
      
      for match in matches:
        if match.group(1) is not None:
          extracted_list.append(match.group(1).strip())
      
      return extracted_list
    
    def validate_time_format(time_str):
      h, m, s = map(int, time_str.split(":"))
      return 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59
    
    if new_value == "":
      return True
    allowd_chars = re.compile(r"^[0-9:\-,]*$")
    if not allowd_chars.fullmatch(new_value):
      return False
    
    value_list = extract_values_from_format(new_value)
    
    all_valid = True
    for value in value_list:
      date_pattern_01 = re.compile(r"^\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}$")
      
      if date_pattern_01.fullmatch(value):
        try:
          start, finish = value.split('-')
          
          if not (validate_time_format(start) and validate_time_format(finish)):
            all_valid = False
        except ValueError:
          all_valid = False
          break
      else:
        all_valid = False
        break
    
    if all_valid:
      return True
    else:
      return False
  
  def load_initial_csv(self):
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
  
  def read_csv(self, filepath):
    def preprocess_dataframe(df):
      df = df.fillna("")
      if "unavailable_time" not in df.columns:
        df.insert(2, "unavailable_time", "")
      
      if "no" not in df.columns:
        num = np.arange(1, len(df)+1, 1)
        df.insert(0, "no", num)
      
      if "member" not in df.columns:
        selected_columns = ['1', '2', '3', '4', '5', '6', '7']
        existing_selected_columns = [col for col in selected_columns if col in df.columns]
        if existing_selected_columns:
          df['member'] = df[existing_selected_columns].values.tolist()
          df = df.drop(existing_selected_columns, axis="columns")
      return df
    
    try:
      df_raw = pd.read_csv(filepath)
      self.df = preprocess_dataframe(df_raw.copy())
      
      if not("name" in self.df.columns)*("member" in self.df.columns):
        messagebox.showerror("Error", f"ファイルの形式が不正です。")
        return
      
      self.display_data_in_treeview(self.df)
      
      self.list_bandname = [name for name in self.df['name']]
      self.list_status = [True]*len(self.df)
      
      self.button_save.config(state=tk.NORMAL)
      
      self.scanning()
    except Exception as e:
      messagebox.showerror("Error", f"ファイルを読み込めませんでした:{e}")
  
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
    
    if not all(self.list_status):
      select_close = messagebox.askokcancel("確認", "不正な入力があるため保存できません。保存せずに終了しますか？")
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
  
if __name__=="__main__":
  root = tk.Tk()
  app = BandInfoApp(root)
  root.mainloop()