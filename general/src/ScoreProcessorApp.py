import tkinter as tk
from modules.utils.label_wraplength import label_wraplength
from modules.SP_ConfigApp import ConfigApp
from modules.SP_DataTreatmentApp import DataTreatmentApp
from modules.SP_ProcessingMainApp import ProcessingMainApp

class ScoreProcessorApp:
  def __init__(self, root, base_path, exe_path):
    self.bundle_dir = base_path
    self.exe_dir = exe_path
    
    self.root = root
    
    lw = label_wraplength(self.root)
    
    self.root.title("ScoreProcessorApp")
    self.root.geometry("500x400")
    
    self.root.grid_columnconfigure(0, weight=1, uniform="all_frames_width")
    self.root.grid_rowconfigure(1, weight=1)
    
    ############intro############
    frame_intro = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="ridge")
    frame_intro.grid(row=0, column=0, sticky="ew")
    frame_intro.grid_columnconfigure(0, weight=1)
    
    label_intro_text = "このツールは、入力されたバンド、採点項目、及び採点データを用いて偏差値法による点数処理を行います。"
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
    
    ############config############
    frame_config = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_config_text = "バンド一覧、および採点項目をインポートします。"
    label_config = lw.label_maker(frame_config, label_config_text)
    button_config = tk.Button(frame_config, text = "ConfigApp", command=self.run_ConfigApp)
    frame_config.grid(row=1, column=0, sticky="ewsn")
    label_config.grid(row=0, column=0)
    button_config.grid(row=1, column=0, sticky="ewsn")
    
    frame_config.rowconfigure(0, weight=1)
    frame_config.columnconfigure(0, weight=1)
    
    ############data############
    frame_data = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_data_text = "採点データの正規化を行います。"
    label_data = lw.label_maker(frame_data, label_data_text)
    button_data = tk.Button(frame_data, text = "DataTreatmentApp", command=self.run_DataTreatmentApp)
    frame_data.grid(row=2, column=0, sticky="ewsn")
    label_data.grid(row=0, column=0)
    button_data.grid(row=1, column=0, sticky="ewsn")
    
    frame_data.rowconfigure(0, weight=1)
    frame_data.columnconfigure(0, weight=1)
    
    ############main############
    frame_runmain = tk.Frame(frame_main, padx = padx_item, pady = pady_item, bd=2, relief="ridge")
    label_runmain_text = "点数処理を実行します。"
    label_runmain = lw.label_maker(frame_runmain, label_runmain_text)
    button_runmain = tk.Button(frame_runmain, text = "ProcessingMainApp", command=self.run_MainApp)
    frame_runmain.grid(row=3, column=0, sticky="ewsn", columnspan=2)
    label_runmain.grid(row=0, column=0)
    button_runmain.grid(row=1, column=0, sticky="ewsn")
    
    frame_runmain.rowconfigure(0, weight=1)
    frame_runmain.columnconfigure(0, weight=1)
    
    lw.treatment()
  
  def run_ConfigApp(self):
    root_config = tk.Toplevel(self.root)
    ConfigApp(root_config, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_config.transient(self.root)
    root_config.grab_set()
    self.root.wait_window(root_config)

  def run_DataTreatmentApp(self):
    root_data = tk.Toplevel(self.root)
    DataTreatmentApp(root_data, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_data.transient(self.root)
    root_data.grab_set()
    self.root.wait_window(root_data)
  
  def run_MainApp(self):
    root_main = tk.Toplevel(self.root)
    ProcessingMainApp(root_main, base_path=self.bundle_dir, exe_path=self.exe_dir)
    root_main.transient(self.root)
    root_main.grab_set()
    self.root.wait_window(root_main)

if __name__ == "__main__":
  root = tk.Tk()
  app = ScoreProcessorApp(root)
  root.mainloop()