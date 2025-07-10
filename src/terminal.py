import os
import tkinter as tk
from tkinter import ttk
import sys
import subprocess
from modules.utils.label_wraplength import label_wraplength

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ScriptRunnerApp:
  def __init__(self, root):
    self.root = root
    
    lw = label_wraplength(self.root)
    
    self.root.title("ScriptRunnerApp")
    self.root.geometry("500x400")
    
    self.root.grid_columnconfigure(0, weight=1, uniform="all_frames_width")
    self.root.grid_rowconfigure(1, weight=1)
    
    ############intro############
    frame_intro = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="ridge")
    frame_intro.grid(row=0, column=0, sticky="ew")
    frame_intro.grid_columnconfigure(0, weight=1)
    
    label_intro_text = "このツールは、入力されたタイムテーブル、バンド、及び出演不可能時間を用いてランダムにタイムテーブルを作成します。"
    label_intro = lw.label_maker(frame_intro, label_intro_text)
    label_intro.grid(row=0, column=0)
    
    ############main############
    frame_main = tk.Frame(root, pady=10, padx=10, bd=2, relief="ridge")
    frame_main.grid(row=1, column=0, sticky="ewsn")
    frame_main.grid_rowconfigure(0, weight=1)
    frame_main.grid_rowconfigure(1, weight=5)
    frame_main.grid_rowconfigure(2, weight=5)
    
    frame_main.grid_columnconfigure(0, weight=1, uniform="group1")
    frame_main.grid_columnconfigure(1, weight=1, uniform="group1")
    
    padx_item = 5
    pady_item = 5
    
    ############conf############
    filename_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "config.py")
    
    frame_conf = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_conf_text = "タイムテーブルの開始時間を定義します。"
    label_conf = lw.label_maker(frame_conf, label_conf_text)
    button_conf = tk.Button(frame_conf, text = "config.py", command=lambda: self.run_script(filename_conf))
    frame_conf.grid(row=0, column=0, sticky="ewsn", columnspan = 2)
    label_conf.grid(row=0, column=0)
    button_conf.grid(row=1, column=0, sticky="ewsn")
    
    frame_conf.rowconfigure(0, weight=1)
    frame_conf.columnconfigure(0, weight=1)
    
    ############band############
    filename_band = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "band.py")
    frame_band = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_band_text = "バンド一覧をインポートします。"
    label_band = lw.label_maker(frame_band, label_band_text)
    button_band = tk.Button(frame_band, text = "band.py", command=lambda: self.run_script(filename_band))
    frame_band.grid(row=1, column=0, sticky="ewsn")
    label_band.grid(row=0, column=0)
    button_band.grid(row=1, column=0, sticky="ewsn")
    
    frame_band.rowconfigure(0, weight=1)
    frame_band.columnconfigure(0, weight=1)
    
    ############schedule############
    filename_sche = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "schedule.py")
    frame_sche = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_sche_text = "タイムテーブルをインポートします。"
    label_sche = lw.label_maker(frame_sche, label_sche_text)
    button_sche = tk.Button(frame_sche, text = "schedule.py", command=lambda: self.run_script(filename_sche))
    frame_sche.grid(row=1, column=1, sticky="ewsn")
    label_sche.grid(row=0, column=0)
    button_sche.grid(row=1, column=0, sticky="ewsn")
    
    frame_sche.rowconfigure(0, weight=1)
    frame_sche.columnconfigure(0, weight=1)
    
    ############main############
    filename_main = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "main.py")
    frame_runmain = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_runmain_text = "タイムテーブル作成を実行します。"
    label_runmain = lw.label_maker(frame_runmain, label_runmain_text)
    button_runmain = tk.Button(frame_runmain, text = "main.py", command=lambda: self.run_script(filename_main))
    frame_runmain.grid(row=2, column=0, sticky="ewsn", columnspan=2)
    label_runmain.grid(row=0, column=0)
    button_runmain.grid(row=1, column=0, sticky="ewsn")
    
    frame_runmain.rowconfigure(0, weight=1)
    frame_runmain.columnconfigure(0, weight=1)
    
    lw.treatment()
  
  def run_script(self, path):
    try:
      if sys.platform == "win32":
        subprocess.Popen(['python', path], creationflags=subprocess.CREATE_NEW_CONSOLE)
      else:
        subprocess.Popen([sys.executable, path])
      print(f"{path}が実行されました！")
    except Exception as e:
        print(f"起動に失敗しました: {e}")

if __name__ == "__main__":
  root = tk.Tk()
  app = ScriptRunnerApp(root)
  root.mainloop()