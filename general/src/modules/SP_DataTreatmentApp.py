import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import pandas as pd
import re
from modules.utils.label_wraplength import label_wraplength
from datetime import datetime, timedelta

class DataTreatmentApp:
  def __init__(self, root, base_path, exe_path):
    self.save_filepath=os.path.join(exe_path, "cache", "ScoreProcessorApp", "data.csv")
    self.item_filepath=os.path.join(exe_path, "cache", "ScoreProcessorApp", "item.csv")
    
    #####開発用#####
    self.exe_path = exe_path
    ##########
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("DataTreatmentApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=0)
    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_rowconfigure(2, weight=0)
    self.root.grid_rowconfigure(3, weight=0)
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "データをインポートすると、正規化したデータを返します。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.frame_info.grid_columnconfigure(0, weight=1)
    
    ############data############
    self.frame_data = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    
    self.button_rawdata = tk.Button(self.frame_data, text="採点データを開く", command=self.open_csv_rawdata)
    
    self.frame_tree = tk.Frame(self.frame_data, padx=10, pady=10, bd=1, relief="ridge")
    
    self.tree = ttk.Treeview(self.frame_tree, show="headings")
    self.xscroll = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
    self.yscroll = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
    self.tree.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
    
    self.frame_data.grid(row=1, column=0, sticky="ewsn")
    self.frame_data.grid_rowconfigure(0, weight=0)
    self.frame_data.grid_rowconfigure(1, weight=1)
    self.frame_data.grid_columnconfigure(0, weight=1)
    self.button_rawdata.grid(row=0, column=0, sticky="ew")
    self.frame_tree.grid(row=1, column=0, sticky="ewsn")
    self.tree.grid(row=0, column=0, sticky="ewsn")
    self.frame_tree.grid_rowconfigure(0, weight=1)
    self.frame_tree.grid_columnconfigure(0, weight=1)
    self.xscroll.grid(row=1, column=0, sticky="ew")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    
    self.frame_status.grid(row=2, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_save = tk.Button(self.frame_button, text="CSVを保存", command=self.save_csv, state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=3, column=0, sticky="ew")
    self.button_save.grid(row=0, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    
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
    
    if df.iloc[1, 1] == "":
      self.button_save.config(state=tk.DISABLED)
      self.table_correct = False
    else:
      self.button_save.config(state=tk.NORMAL)
      self.table_correct = True
  
  def load_initial_csv(self):
    self.initialstatus = False
    if os.path.exists(self.save_filepath):
      self.initialstatus = True
      self.read_filepath = self.save_filepath
      self.read_csv(self.read_filepath)
    self.savestatus = True
  
  def open_csv_rawdata(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    self.initialstatus = False
    if filepath:
      self.read_filepath = filepath
    self.read_csv(self.read_filepath)
    self.savestatus = False
  
  def read_csv(self, filepath):
    try:
      df_raw = pd.read_csv(filepath)
      
      if not self.initialstatus:
        ############列のチェックリストを作成############
        root_confirm = tk.Toplevel(self.root)
        
        root_confirm.title("採点データのインポート")
        root_confirm.geometry("400x300")
        
        root_confirm.grid_rowconfigure(0, weight=1)
        root_confirm.grid_rowconfigure(1, weight=0)
        root_confirm.grid_columnconfigure(0, weight=1)
        
        df_raw_columns_list = list(df_raw.columns)
        
        checkbox_vars = {}
        
        canvas = tk.Canvas(root_confirm, bg="lightblue", borderwidth=0, highlightthickness=0)
        
        yscroll_canvas = ttk.Scrollbar(root_confirm, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=yscroll_canvas.set)
        
        canvas.grid(row=0, column=0, sticky="ewsn")
        yscroll_canvas.grid(row=0, column=1, sticky="sn")
        
        frame_checkbox = ttk.Frame(canvas)
        
        canvas_window_id = canvas.create_window((0, 0), window=frame_checkbox, anchor="nw")
        
        frame_checkbox.columnconfigure(0, weight=0)
        frame_checkbox.columnconfigure(1, weight=0)
        frame_checkbox.columnconfigure(2, weight=1)
        
        def on_frame_configure(event=None):
          frame_checkbox.update_idletasks()
          
          req_width = frame_checkbox.winfo_reqwidth()
          req_height = frame_checkbox.winfo_reqheight()
          
          canvas_current_width = canvas.winfo_width()
          set_width = max(req_width, canvas_current_width) if canvas_current_width > 0 else req_width
          
          canvas.itemconfigure(canvas_window_id, width=set_width) 
          
          bbox_all = canvas.bbox("all")
          canvas.configure(scrollregion=bbox_all)
        
        frame_checkbox.bind("<Configure>", on_frame_configure)
        canvas.bind('<Configure>', on_frame_configure)
        
        label_checkbox1 = self.lw.label_maker(frame_checkbox, text="審査員名")
        label_checkbox2 = self.lw.label_maker(frame_checkbox, text="不要列")
        label_checkbox3 = self.lw.label_maker(frame_checkbox, text="列名")
        label_checkbox1.grid(row=0, column=0, sticky="w")
        label_checkbox2.grid(row=0, column=1, sticky="w")
        label_checkbox3.grid(row=0, column=2, sticky="w")
        
        for i, item in enumerate(df_raw_columns_list):
          var1 = tk.BooleanVar()
          chk1 = ttk.Checkbutton(frame_checkbox, variable=var1)
          chk1.grid(row=i+1, column=0, sticky="w")
          
          var2 = tk.BooleanVar()
          chk2 = ttk.Checkbutton(frame_checkbox, variable=var2)
          chk2.grid(row=i+1, column=1, sticky="w")
          
          item_label = self.lw.label_maker(frame_checkbox, text=item)
          item_label.grid(row=i+1, column=2, sticky="w")
          
          checkbox_vars[item] = [var1, var2]
        
        def columnconfig():
          column_name = ""
          column_del = []
          for item, vars_list in checkbox_vars.items():
            if not((vars_list[0].get())|(vars_list[1].get())):
              continue
            elif (vars_list[0].get())&(vars_list[1].get()):
              messagebox.showerror("Error", f"審査員名が不要列に指定されています。")
              return
            elif vars_list[0].get():
              if column_name == "":
                column_name = item
              else:
                messagebox.showerror("Error", f"審査員名が複数選択されています。")
                return
            elif vars_list[1].get():
              column_del.append(item)
          if column_name == "":
            messagebox.showerror("Error", f"審査員名が選択されていません。")
            return
          self.column_name = column_name
          self.column_del = column_del
          root_confirm.destroy()
        
        button_confirm = ttk.Button(root_confirm, command=columnconfig)
        button_confirm.grid(row=1, column=0, sticky="ew")
        
        root_confirm.transient(self.root)
        root_confirm.grab_set()
        
        root_confirm.update_idletasks()
        on_frame_configure()

        self.lw.treatment()
        self.root.wait_window(root_confirm)
        
        ########################
      
        df_raw = df_raw.drop(columns=self.column_del)
        
        column_melted = [col for col in df_raw.columns if col not in self.column_name]
        
        df_melted = pd.melt(df_raw, id_vars=self.column_name, value_vars=column_melted, var_name="表示バンド名_評価項目", value_name="素点")
        
        df_item = pd.read_csv(self.item_filepath)
        item_list = list(df_item['item'])
        pattern = r'(.*)の(' + '|'.join(map(re.escape, item_list)) + r')の点数$'
        extracted = df_melted['表示バンド名_評価項目'].str.extract(pattern)
        
        df_melted['表示バンド名'] = extracted[0]
        df_melted['評価項目'] = extracted[1]
        
        df_melted = df_melted.rename(columns={self.column_name: '審査員名'})
        
        new_column_order = ['審査員名', '表示バンド名', '評価項目', '素点']
        df_melted = df_melted[new_column_order]
        
        df_normalized = df_melted.pivot_table(index=['審査員名', '表示バンド名'], columns='評価項目', values='素点',aggfunc='last').reset_index()
        
        self.df_normalized = df_normalized[['審査員名', '表示バンド名'] + item_list].dropna(subset=item_list)
      else:
        self.df_normalized = df_raw
      
      self.display_data_in_treeview(self.df_normalized)
      
      self.savestatus = False
      
    except Exception as e:
      print(e)
      messagebox.showerror("Error", f"ファイルを読み込めませんでした:{e}")

  def save_csv(self):
    try:
      self.df_normalized.to_csv(self.save_filepath, index=False, encoding='utf-8')
      self.label_status.config(text="保存しました！", foreground="green")
      self.savestatus = True
    except Exception as e:
      self.label_status.config(text=f"保存に失敗しました:{e}")
      
  def close_app(self):
    if self.savestatus:
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