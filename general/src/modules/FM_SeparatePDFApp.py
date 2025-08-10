import csv
import os
from googleapiclient.discovery import build
from tqdm import tqdm
import pandas as pd
import random
from modules.utils.label_wraplength import label_wraplength
import tkinter as tk
from tkinter import ttk, filedialog
import fitz
import pypdf

class SeparatePDFApp:
  def __init__(self, root, base_path, exe_path):
    self.base_path = base_path
    self.exe_path = exe_path
    
    self.root = root
    self.lw = label_wraplength(self.root)
    self.root.title("SeparatePDFApp")
    self.root.geometry("800x600")
    
    self.root.attributes("-topmost", True)
    self.root.after(500, lambda: self.root.attributes("-topmost", False))
    
    ############information############
    self.frame_info = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_info = self.lw.label_maker(self.frame_info, "Wordの差し込み文章機能を用いて作成した1つに繋がったフィードバックシートをバンドごとに分割します。")
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
    self.label_conf01_1 = self.lw.label_maker(self.frame_conf01, "保存するファイルのファイル名を指定します。")
    self.entry_conf01 = tk.Entry(self.frame_conf01)
    self.label_conf01_2 = self.lw.label_maker(self.frame_conf01)
    self.entry_conf01.bind("<KeyRelease>", self.judging)
    self.frame_conf01.grid(row=1, column=0, sticky="ew")
    self.label_conf01_1.grid(row=0, column=0, sticky="ew")
    self.entry_conf01.grid(row=1, column=0, sticky="ew")
    self.label_conf01_2.grid(row=2, column=0, sticky="ew")
    
    self.status_read_data = False
    self.status_read_pdf = False
    
    self.frame_conf01.grid_columnconfigure(0, weight=1)
    
    self.frame_conf02 = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_conf02 = tk.Button(self.frame_conf02, text="データCSVを開く", command=self.open_csv_data)
    
    self.frame_conf02.grid(row=2, column=0, sticky="ew")
    self.button_conf02.grid(row=0, column=0, sticky="ew")
    
    self.frame_conf02.grid_columnconfigure(0, weight=1)
    
    self.frame_conf03 = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_conf03 = tk.Button(self.frame_conf03, text="フィードバックのPDFを開く", command=self.open_csv_pdf)
    
    self.frame_conf03.grid(row=3, column=0, sticky="ew")
    self.button_conf03.grid(row=0, column=0, sticky="ew")
    
    self.frame_conf03.grid_columnconfigure(0, weight=1)
    
    ############status############
    self.frame_status = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.label_status = self.lw.label_maker(self.frame_status)
    self.frame_status.grid(row=4, column=0, sticky="ew")
    self.label_status.grid(row=0, column=0, sticky="ew")
    
    ############log############
    self.frame_log = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.logbox = tk.Text(self.frame_log, state='disabled', borderwidth=5, wrap='word')
    self.yscroll = ttk.Scrollbar(self.frame_log, orient="vertical", command=self.logbox.yview)
    self.logbox.configure(yscrollcommand=self.yscroll.set)
    
    self.frame_log.grid(row=5, column=0, sticky="ewsn")
    self.logbox.grid(row=0, column=0, sticky="ewsn")
    self.yscroll.grid(row=0, column=1, sticky="sn")
    
    self.frame_log.grid_rowconfigure(0, weight=1)
    self.frame_log.grid_columnconfigure(0, weight=1)
    
    ############button############
    self.frame_button = tk.Frame(self.root, padx=10, pady=10, bd=1, relief="ridge")
    self.button_running = tk.Button(self.frame_button, text="実行", command=self.treatment)
    self.button_running.config(state=tk.DISABLED)
    self.button_close = tk.Button(self.frame_button, text="閉じる", command=self.close_app)
    self.frame_button.grid(row=6, column=0, sticky="ew")
    self.button_running.grid(row=0, column=0, sticky="ew")
    self.button_close.grid(row=1, column=0, sticky="ew")
    
    self.frame_button.grid_columnconfigure(0, weight=1)
    self.frame_button.grid_rowconfigure(0, weight=3)
    self.frame_button.grid_rowconfigure(1, weight=1)
    
    self.lw.treatment()
    self.judging()
  
  def WriteToLog(self, msg):
    self.logbox['state'] = 'normal'
    if self.logbox.index('end-1c') != '1.0':
      self.logbox.insert('end', '\n')
    self.logbox.insert('end', msg)
    self.logbox.see(tk.END)
    self.logbox['state'] = "disabled"
  
  def judging(self, event=None):
    self.filename_temp = self.entry_conf01.get().strip().replace(" ", "").replace("　", "")
    self.entry_conf01.delete(0, tk.END)
    self.entry_conf01.insert(0, self.filename_temp)
    if self.filename_temp != "":
      self.label_conf01_2.configure(text=f"{self.filename_temp}_[バンド名].pdf")
    self.WriteToLog(self.filename_temp != "")
    self.WriteToLog(self.status_read_data)
    self.WriteToLog(self.status_read_pdf)
    if (self.filename_temp != "") & self.status_read_data & self.status_read_pdf:
      self.button_running.config(state=tk.NORMAL)
  
  def open_csv_data(self):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      self.read_csv_data(filepath)
  
  def read_csv_data(self, filepath):
    try:
      self.df_data = pd.read_csv(filepath)
      self.WriteToLog("読み込んだデータCSVは以下です。")
      self.WriteToLog(self.df_data)
      
      data_columns = ['Number','Name','Video ID','Score','judge','Band ID']
      
      if not set(data_columns).issubset(self.df_data):
        self.WriteToLog(f"データCSVが条件を満たしていません。")
        self.status_read_data = False
        return
      self.status_read_data = True
    except Exception as e:
      self.WriteToLog(f"読み込みの際にエラーが発生しました:{e}")
      self.status_read_data = False
  
  def open_csv_pdf(self):
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
      self.read_csv_pdf(filepath)
  
  def read_csv_pdf(self, filepath):
    try:
      self.pdf_path = filepath
      self.WriteToLog("PDFファイルを読み込みました。")
      self.status_read_pdf = True
      self.judging()
    except Exception as e:
      self.WriteToLog(f"読み込みの際にエラーが発生しました:{e}")
      self.status_read_pdf = False
      self.judging()
  
  def treatment(self):
    try:
      folderpath = filedialog.askdirectory(title="分割したPDFファイルの保存先を指定")
      if folderpath:
        output_path = folderpath
      else:
        return
      
      #PDF内のテキストを検索する関数の定義
      def search_text_in_pdf(pdf_path, search_text):
        # PDFファイルを開く
        pdf_document = fitz.open(pdf_path)
        # 検索結果のページ番号リスト
        pages_with_text = []
        
        # 各ページをループし、テキストを検索
        for page_num in range(pdf_document.page_count):
          page = pdf_document[page_num]
          text = page.get_text()
          
          # テキストが含まれているかを確認
          if str(search_text) in text:
            pages_with_text.append(page_num + 1)  # ページ番号は1から始まるように+1
        # PDFファイルを閉じる
        pdf_document.close()
        
        return pages_with_text
      
      base_pdf = pypdf.PdfReader(self.pdf_path)

      df1 = self.df_data

      err=[]

      for i in tqdm(range(0, len(df1))):
        
        search_text = df1.at[i, "Band ID"]
        result = search_text_in_pdf(self.pdf_path, search_text)
        if i == len(df1)-1:
          nresult = [len(base_pdf.pages)]
        else:
          search_ntext = df1.at[i+1, "Band ID"]
          nresult = search_text_in_pdf(self.pdf_path, search_ntext)
        
        self.WriteToLog(f"{df1.at[i, 'Name']}, {result}, {nresult}")
        
        if len(result) == 0:
          err.append(df1.at[i, "Band ID"])
          continue
        elif len(nresult) == 0:
          err.append(df1.at[i+1, "Band ID"])
          continue
        
        pdf_writer = pypdf.PdfWriter()
        for j in range(result[0], nresult[0]):
          pdf_writer.add_page(base_pdf.pages[j-1])
        pdf_writer.write(os.path.join(output_path, f"{self.filename_temp}_{df1.at[i, 'Name']}.pdf"))
        pdf_writer.close()
      
      self.WriteToLog(err)
    except Exception as e:
      self.WriteToLog(f"分割に失敗しました:{e}")
      
  def close_app(self):
      self.root.destroy()

