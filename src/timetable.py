import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys

# カレントディレクトリを本ファイルが存在するフォルダに変更。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ScriptRunnerApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Python スクリプト実行ツール")
    self.root.geometry("500x400")
    
    self.script_listbox_frame = tk.Frame(root)
    self.script_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    self.script_listbox_label = tk.Label(self.script_listbox_frame, text="実行可能なPythonスクリプト:")
    self.script_listbox_label.pack()
    
    self.script_listbox = tk.Listbox(self.script_listbox_frame, selectmode=tk.SINGLE, height=10)
    self.script_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    self.scrollbar = tk.Scrollbar(self.script_listbox_frame, orient="vertical", command=self.script_listbox.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill="y")
    self.script_listbox.config(yscrollcommand=self.scrollbar.set)
    
    self.button_frame = tk.Frame(root)
    self.button_frame.pack(pady=10)
    
    self.refresh_button = tk.Button(self.button_frame, text="リストを更新", command=self.load_scripts)
    self.refresh_button.pack(side=tk.LEFT, padx=5)
    
    self.run_button = tk.Button(self.button_frame, text="選択したスクリプトを実行", command=self.run_selected_script)
    self.run_button.pack(side=tk.LEFT, padx=5)
    
    self.current_dir_label = tk.Label(root, text="")
    self.current_dir_label.pack(pady=5)
    
    self.load_scripts()

  def load_scripts(self):
    """カレントディレクトリ内のPythonスクリプトをリストボックスに読み込む"""
    self.script_listbox.delete(0, tk.END)
    current_dir = os.path.join(os.getcwd(), "modules")
    self.current_dir_label.config(text=f"対象のディレクトリ: {current_dir}")
    
    python_scripts = [f for f in os.listdir(current_dir) if f.endswith(".py") and f != os.path.basename(__file__)]
    if not python_scripts:
      self.script_listbox.insert(tk.END, "このディレクトリには実行可能なPythonスクリプトがありません。")
      self.run_button.config(state=tk.DISABLED)
    else:
      for script in sorted(python_scripts):
        self.script_listbox.insert(tk.END, script)
      self.run_button.config(state=tk.NORMAL)

  def run_selected_script(self):
    """選択されたPythonスクリプトを実行する"""
    selected_index = self.script_listbox.curselection()
    if not selected_index:
      messagebox.showwarning("スクリプトが選択されていません", "実行するスクリプトを選択してください。")
      return

    selected_script = self.script_listbox.get(selected_index[0])
    script_path = os.path.join(os.getcwd(), selected_script)

    try:
      # 新しいプロセスでスクリプトを実行
      # Windowsでは'start'、macOS/Linuxでは'open'または直接pythonコマンド
      if sys.platform == "win32":
        subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
      else:
        # ターミナルで実行したい場合は以下のように変更
        # subprocess.Popen(['open', '-a', 'Terminal', script_path]) # macOS
        # subprocess.Popen(['x-terminal-emulator', '-e', f'python {script_path}']) # Linux (例)
        subprocess.Popen([sys.executable, script_path])
      
      messagebox.showinfo("スクリプト実行", f"'{selected_script}' を実行しました。")
    except Exception as e:
      messagebox.showerror("実行エラー", f"スクリプトの実行中にエラーが発生しました:\n{e}")

if __name__ == "__main__":
  root = tk.Tk()
  app = ScriptRunnerApp(root)
  root.mainloop()
