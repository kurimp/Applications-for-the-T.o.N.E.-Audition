import os
import tkinter as tk
import sys
from modules.utils.label_wraplength import label_wraplength
from TimetableMakerApp import TimetableMakerApp
from ScoreProcessorApp import ScoreProcessorApp

#実行ファイル化のためのコマンド
#pyinstaller --onefile --windowed ./general/src/AuditionManagerApp.py

if getattr(sys, 'frozen', False):
  bundle_dir = sys._MEIPASS
  exe_dir = os.path.dirname(sys.executable)
else:
  bundle_dir = os.path.dirname(os.path.abspath(__file__))
  exe_dir = os.path.dirname(os.path.abspath(__file__))

print(f"【DEBUG】bundle_dir:{bundle_dir}")
print(f"【DEBUG】exe_dir:{exe_dir}")

os.chdir(bundle_dir)

class AuditionManagerApp:
  def __init__(self, root):
    self.bundle_dir = bundle_dir
    self.exe_dir = exe_dir
    
    self.make_folders()
    
    self.root = root
    
    self.lw = label_wraplength(self.root)
    
    self.root.title("AuditionManagerApp")
    self.root.geometry("500x400")
    
    self.root.grid_columnconfigure(0, weight=1, uniform="all_frames_width")
    self.root.grid_rowconfigure(1, weight=1)
    
    ############intro############
    frame_intro = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="ridge")
    frame_intro.grid(row=0, column=0, sticky="ew")
    frame_intro.grid_columnconfigure(0, weight=1)
    
    label_intro_text = "千葉大学アカペラサークルT.o.N.E.が実施するサークル内審査の運営を補助するためのツール群です。"
    label_intro = self.lw.label_maker(frame_intro, label_intro_text)
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
    label_conf = self.lw.label_maker(frame_conf, label_conf_text)
    #button_conf = tk.Button(frame_conf, text = "config.py", command=lambda: self.run_script(filename_conf))
    button_conf = tk.Button(frame_conf, text = "何も起きません。")
    frame_conf.grid(row=0, column=0, sticky="ewsn", columnspan = 2)
    label_conf.grid(row=0, column=0)
    button_conf.grid(row=1, column=0, sticky="ewsn")
    
    frame_conf.rowconfigure(0, weight=1)
    frame_conf.columnconfigure(0, weight=1)
    
    ############TimetableMakerApp############
    frame_timetable = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_timetable_text = "対面審査のタイムテーブル作成"
    label_timetable = self.lw.label_maker(frame_timetable, label_timetable_text)
    button_timetable = tk.Button(frame_timetable, text = "TimetableMakerApp", command=self.run_TimetableMakerApp)
    frame_timetable.grid(row=1, column=0, sticky="ewsn")
    label_timetable.grid(row=0, column=0)
    button_timetable.grid(row=1, column=0, sticky="ewsn")
    
    frame_timetable.rowconfigure(0, weight=0)
    frame_timetable.rowconfigure(1, weight=1)
    frame_timetable.columnconfigure(0, weight=1)
    
    ############ScoreProcessorApp############
    frame_score = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_score_text = "偏差値法を用いた得点処理"
    label_score = self.lw.label_maker(frame_score, label_score_text)
    button_score = tk.Button(frame_score, text = "ScoreProcessorApp", command=self.run_ScoreProcessorApp)
    frame_score.grid(row=1, column=1, sticky="ewsn")
    label_score.grid(row=0, column=0)
    button_score.grid(row=1, column=0, sticky="ewsn")
    
    frame_score.rowconfigure(0, weight=0)
    frame_score.rowconfigure(1, weight=1)
    frame_score.columnconfigure(0, weight=1)
    
    self.lw.treatment()
  
  def run_TimetableMakerApp(self):
    root_timetable = tk.Toplevel(self.root)
    TimetableMakerApp(root_timetable, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_timetable.transient(self.root)
    root_timetable.grab_set()
    self.root.wait_window(root_timetable)
  
  def run_ScoreProcessorApp(self):
    root_score = tk.Toplevel(self.root)
    ScoreProcessorApp(root_score, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_score.transient(self.root)
    root_score.grab_set()
    self.root.wait_window(root_score)
    
  def make_folders(self):
    
    folder_path_list = [os.path.join(self.exe_dir, "cache", "TimetableMakerApp", "logs"), 
                        os.path.join(self.exe_dir, "cache", "ScoreProcessorApp", "logs")]
    
    try:
      for folder_path in folder_path_list:
        folder_path = os.path.abspath(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
      print(f"DEBUG:{e}")

if __name__ == "__main__":
  root = tk.Tk()
  app = AuditionManagerApp(root)
  root.mainloop()