import tkinter as tk
from modules.utils.label_wraplength import label_wraplength
from modules.FM_CommentCollectionApp import CommentCollectionApp
from modules.FM_SeparatePDFApp import SeparatePDFApp

class FeedbackMakerApp:
  def __init__(self, root, base_path, exe_path):
    self.bundle_dir = base_path
    self.exe_dir = exe_path
    
    self.root = root
    
    lw = label_wraplength(self.root)
    
    self.root.title("FeedbackMakerApp")
    self.root.geometry("500x400")
    
    self.root.grid_columnconfigure(0, weight=1, uniform="all_frames_width")
    self.root.grid_rowconfigure(1, weight=1)
    
    ############intro############
    frame_intro = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="ridge")
    frame_intro.grid(row=0, column=0, sticky="ew")
    frame_intro.grid_columnconfigure(0, weight=1)
    
    label_intro_text = "このツール群は、審査のフィードバックシート作成を支援するためのものです。"
    label_intro = lw.label_maker(frame_intro, label_intro_text)
    label_intro.grid(row=0, column=0)
    
    ############main############
    frame_main = tk.Frame(root, pady=10, padx=10, bd=2, relief="ridge")
    frame_main.grid(row=1, column=0, sticky="ewsn")
    frame_main.grid_rowconfigure(0, weight=1)
    frame_main.grid_rowconfigure(1, weight=5)
    frame_main.grid_rowconfigure(2, weight=5)
    frame_main.grid_rowconfigure(3, weight=5)
    
    frame_main.grid_columnconfigure(0, weight=1, uniform="group1")
    
    padx_item = 5
    pady_item = 5
    
    ############conf############
    frame_conf = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    #label_conf_text = "タイムテーブルの開始時間を定義します。"
    label_conf_text = "このボタンは無効化されています。"
    label_conf = lw.label_maker(frame_conf, label_conf_text)
    #button_conf = tk.Button(frame_conf, text = "config.py", command=lambda: self.run_script(filename_conf))
    button_conf = tk.Button(frame_conf, text = "何も起きません。")
    frame_conf.grid(row=0, column=0, sticky="ewsn", columnspan = 2)
    label_conf.grid(row=0, column=0)
    button_conf.grid(row=1, column=0, sticky="ewsn")
    
    frame_conf.rowconfigure(0, weight=1)
    frame_conf.columnconfigure(0, weight=1)
    
    ############comment############
    frame_comment = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_comment_text = "YouTubeからコメントを取得し、Word差し込み文章機能のためのCSVを作成します。"
    label_comment = lw.label_maker(frame_comment, label_comment_text)
    button_comment = tk.Button(frame_comment, text = "CommentCollectionApp", command=self.run_CommentCollectionApp)
    frame_comment.grid(row=1, column=0, sticky="ewsn")
    label_comment.grid(row=0, column=0)
    button_comment.grid(row=1, column=0, sticky="ewsn")
    
    frame_comment.rowconfigure(0, weight=1)
    frame_comment.columnconfigure(0, weight=1)
    
    ############separate############
    frame_separate = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_separate_text = "1つに繋がったフィードバックシートをバンドごとに分割します。"
    label_separate = lw.label_maker(frame_separate, label_separate_text)
    button_separate = tk.Button(frame_separate, text = "SeparatePDFApp", command=self.run_SeparatePDFApp)
    frame_separate.grid(row=2, column=0, sticky="ewsn")
    label_separate.grid(row=0, column=0)
    button_separate.grid(row=1, column=0, sticky="ewsn")
    
    frame_separate.rowconfigure(0, weight=1)
    frame_separate.columnconfigure(0, weight=1)
    
    lw.treatment()
  
  def run_CommentCollectionApp(self):
    root_config = tk.Toplevel(self.root)
    CommentCollectionApp(root_config, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_config.transient(self.root)
    root_config.grab_set()
    self.root.wait_window(root_config)
  
  def run_SeparatePDFApp(self):
    root_data = tk.Toplevel(self.root)
    SeparatePDFApp(root_data, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_data.transient(self.root)
    root_data.grab_set()
    self.root.wait_window(root_data)