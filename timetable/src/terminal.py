import os
import tkinter as tk
import sys
from modules.utils.label_wraplength import label_wraplength
from modules.band import BandInfoApp
from modules.schedule import ScheduleInfoApp
from modules.main import MainApp

if getattr(sys, 'frozen', False):
  bundle_dir = sys._MEIPASS
  exe_dir = os.path.dirname(sys.executable)
else:
  bundle_dir = os.path.dirname(os.path.abspath(__file__))
  exe_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(bundle_dir)

class ScriptRunnerApp:
  def __init__(self, root):
    self.bundle_dir = bundle_dir
    self.exe_dir = exe_dir
    
    self.make_folders()
    
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
    
    ############band############
    frame_band = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_band_text = "バンド一覧をインポートします。"
    label_band = lw.label_maker(frame_band, label_band_text)
    button_band = tk.Button(frame_band, text = "band.py", command=self.run_BandInfoApp)
    frame_band.grid(row=1, column=0, sticky="ewsn")
    label_band.grid(row=0, column=0)
    button_band.grid(row=1, column=0, sticky="ewsn")
    
    frame_band.rowconfigure(0, weight=1)
    frame_band.columnconfigure(0, weight=1)
    
    ############schedule############
    frame_sche = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_sche_text = "タイムテーブルをインポートします。"
    label_sche = lw.label_maker(frame_sche, label_sche_text)
    button_sche = tk.Button(frame_sche, text = "schedule.py", command=self.run_ScheduleInfoApp)
    frame_sche.grid(row=1, column=1, sticky="ewsn")
    label_sche.grid(row=0, column=0)
    button_sche.grid(row=1, column=0, sticky="ewsn")
    
    frame_sche.rowconfigure(0, weight=1)
    frame_sche.columnconfigure(0, weight=1)
    
    ############main############
    frame_runmain = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_runmain_text = "タイムテーブル作成を実行します。"
    label_runmain = lw.label_maker(frame_runmain, label_runmain_text)
    button_runmain = tk.Button(frame_runmain, text = "main.py", command=self.run_MainApp)
    frame_runmain.grid(row=2, column=0, sticky="ewsn", columnspan=2)
    label_runmain.grid(row=0, column=0)
    button_runmain.grid(row=1, column=0, sticky="ewsn")
    
    frame_runmain.rowconfigure(0, weight=1)
    frame_runmain.columnconfigure(0, weight=1)
    
    lw.treatment()
  
  def run_BandInfoApp(self):
    root_band = tk.Toplevel(self.root)
    BandInfoApp(root_band, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_band.transient(self.root)
    root_band.grab_set()
    self.root.wait_window(root_band)

  def run_ScheduleInfoApp(self):
    root_sche = tk.Toplevel(self.root)
    ScheduleInfoApp(root_sche, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_sche.transient(self.root)
    root_sche.grab_set()
    self.root.wait_window(root_sche)
  
  def run_MainApp(self):
    root_main = tk.Toplevel(self.root)
    MainApp(root_main, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_main.transient(self.root)
    root_main.grab_set()
    self.root.wait_window(root_main)
  
  def make_folders(self):
    
    folder_path_list = [os.path.join(self.exe_dir, "cache", "logs")]
    
    print(f"DEBUG:{self.exe_dir}")
    print(f"DEBUG:{folder_path_list}")
    
    try:
      for folder_path in folder_path_list:
        folder_path = os.path.abspath(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
      print(f"DEBUG:{e}")

if __name__ == "__main__":
  root = tk.Tk()
  app = ScriptRunnerApp(root)
  root.mainloop()