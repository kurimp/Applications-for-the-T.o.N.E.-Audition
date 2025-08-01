import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import re
import pandas as pd
import numpy as np
from modules.utils.label_wraplength import label_wraplength

class ConfigApp:
  def __init__(self, root, base_path, exe_path):
    self.save_filepath_band=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "ScoreProcessorApp", "band.csv")
    self.save_filepath_item=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "ScoreProcessorApp", "item.csv")
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("ConfigApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "バンド一覧、および採点項目一覧をインポートします。")
    self.frame_info.grid(row=0, column=0, sticky="ew")
    self.label_info.grid(row=0, column=0, sticky="ew")
    
    self.frame_info.grid_columnconfigure(0, weight=1)
    
    ############contents############
    self.frame_cont = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.frame_cont.grid(row=1, column=0, sticky="ewsn")
    
    self.frame_cont.columnconfigure(0, weight=1)
    self.frame_cont.columnconfigure(1, weight=1)
    self.frame_cont.rowconfigure(0, weight=1)
    
    ############band############
    self.frame_band = tk.Frame(self.frame_cont, padx=10, pady=10, bd=1, relief="ridge")
    
    self.button_band = tk.Button(self.frame_band, text="バンドCSVを開く", command=self.open_csv_band)
    
    self.frame_box_band = tk.Frame(self.frame_band, padx=10, pady=10, bd=1, relief="ridge")
    self.box_band = tk.Text(self.frame_box_band, state='disabled', borderwidth=5, wrap='word')
    self.yscroll_band = ttk.Scrollbar(self.frame_box_band, orient="vertical", command=self.box_band.yview)
    self.box_band.configure(yscrollcommand=self.yscroll_band.set)
    
    self.frame_band.grid(row=0, column=0, sticky="ewsn")
    self.frame_band.columnconfigure(0, weight=1)
    self.frame_band.rowconfigure(1, weight=1)
    self.button_band.grid(row=0, column=0, sticky="ew")
    self.frame_box_band.grid(row=1, column=0, sticky="ewsn")
    self.frame_box_band.columnconfigure(0, weight=1)
    self.frame_box_band.rowconfigure(0, weight=1)
    self.box_band.grid(row=0, column=0, sticky="ewsn")
    self.yscroll_band.grid(row=0, column=1, sticky="sn")
    
    ############item############
    self.frame_item = tk.Frame(self.frame_cont, padx=10, pady=10, bd=1, relief="ridge")
    
    self.button_item = tk.Button(self.frame_item, text="採点項目CSVを開く", command=self.open_csv_item)
    
    self.frame_box_item = tk.Frame(self.frame_item, padx=10, pady=10, bd=1, relief="ridge")
    self.box_item = tk.Text(self.frame_box_item, state='disabled', borderwidth=5, wrap='word')
    self.yscroll_item = ttk.Scrollbar(self.frame_box_item, orient="vertical", command=self.box_item.yview)
    self.box_item.configure(yscrollcommand=self.yscroll_item.set)
    
    self.frame_item.grid(row=0, column=1, sticky="ewsn")
    self.frame_item.columnconfigure(0, weight=1)
    self.frame_item.rowconfigure(1, weight=1)
    self.button_item.grid(row=0, column=0, sticky="ew")
    self.frame_box_item.grid(row=1, column=0, sticky="ewsn")
    self.frame_box_item.columnconfigure(0, weight=1)
    self.frame_box_item.rowconfigure(0, weight=1)
    self.box_item.grid(row=0, column=0, sticky="ewsn")
    self.yscroll_item.grid(row=0, column=1, sticky="sn")
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    self.frame_status.grid(row=2, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    
    self.frame_button.grid(row=3, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    
    self.load_initial_csv()
    self.lw.treatment()
  
  def display_in_box_band(self, text):
    self.box_band['state'] = 'normal'
    self.box_band.delete('1.0', tk.END)
    self.box_band.insert('end', text)
    self.box_band.see(tk.END)
    self.box_band['state'] = 'disabled'
  
  def display_in_box_item(self, text):
    self.box_item['state'] = 'normal'
    self.box_item.delete('1.0', tk.END)
    self.box_item.insert('end', text)
    self.box_item.see(tk.END)
    self.box_item['state'] = 'disabled'
  
  def load_initial_csv(self):
    if os.path.exists(self.save_filepath_band):
      read_filepath = self.save_filepath_band
      self.read_csv_band(read_filepath)
    if os.path.exists(self.save_filepath_item):
      read_filepath = self.save_filepath_item
      self.read_csv_item(read_filepath)
    
  def open_csv_band(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      read_filepath = filepath
    
    self.read_csv_band(read_filepath)
    self.savestatus = False
  
  def open_csv_item(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      self.read_filepath = filepath
    
    self.read_csv_item(self.read_filepath)
    self.savestatus = False
  
  def read_csv_band(self, filepath):
    try:
      df_band = pd.read_csv(filepath)
      
      if not(("name" in df_band.columns)&("name_on_form" in df_band.columns)):
        messagebox.showerror("Error", f"ファイルの形式が不正です。")
        return
      
      member_columns = ['1', '2', '3', '4', '5', '6', '7']
      
      self.df_band = df_band[['name_on_form', 'name']+member_columns]
      
      existing_selected_columns = [col for col in member_columns if col in self.df_band]
      if existing_selected_columns:
        self.df_band['member'] = self.df_band[existing_selected_columns].apply(lambda row: row.tolist(), axis=1)
        self.df_band = self.df_band.drop(existing_selected_columns, axis="columns")
      
      output = "name_on_form,name, member"
      for name_on_form, name, member in zip(self.df_band['name_on_form'], self.df_band['name'], self.df_band['member']):
        if output != "":
          output += "\n"
        output += str(name_on_form) + ", " + str(name) + ", "  + str(member)
      
      self.display_in_box_band(output)
      
    except Exception as e:
      messagebox.showerror("Error", f"ファイルを読み込めませんでした:{e}")
  
  def read_csv_item(self, filepath):
    try:
      df_item = pd.read_csv(filepath)
      
      if not("item" in df_item.columns)*("full" in df_item.columns)*("weight" in df_item.columns):
        messagebox.showerror("Error", f"ファイルの形式が不正です。")
        return
      
      self.df_item = df_item[['item', 'full', 'weight']]
      
      list_item = self.df_item['item']
      list_full = self.df_item['full']
      list_weight = self.df_item['weight']
      
      output = "項目, 満点, 傾斜配点"
      for item, full, weight in zip(list_item, list_full, list_weight):
        if output != "":
          output += "\n"
        output += item + ", " + str(full) + ", " + str(weight)
      
      self.display_in_box_item(output)
      
    except Exception as e:
      messagebox.showerror("Error", f"ファイルを読み込めませんでした:{e}")
  
  def save_csv(self):
    try:
      self.df_band.to_csv(self.save_filepath_band, index=False, encoding='utf-8')
      self.df_item.to_csv(self.save_filepath_item, index=False, encoding='utf-8')
    except Exception as e:
      messagebox.showerror("Error", f"保存に失敗しました:{e}")
      
  def close_app(self):
    self.save_csv()
    self.root.destroy()
  
if __name__=="__main__":
  root = tk.Tk()
  app = ConfigApp(root)
  root.mainloop()