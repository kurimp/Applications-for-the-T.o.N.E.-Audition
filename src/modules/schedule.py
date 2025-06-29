import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont
import subprocess
import sys
import configparser
from datetime import datetime, timedelta # datetimeモジュールを追加

# カレントディレクトリを本ファイルが存在するフォルダに変更。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- DataFrameの前処理 ---
try:
  df_sche = pd.read_csv("../../data/schedule.csv")
except FileNotFoundError:
  messagebox.showerror("ファイルエラー", "data/schedule.csv が見つかりません。")
  sys.exit()

# ConfigParser インスタンスを初期化
config = configparser.ConfigParser()
config_filepath = "../assets/config.ini" # デフォルトの設定ファイル名

# config.iniを読み込む前にファイル存在チェックとセクション・キー存在チェックを追加
if os.path.exists(config_filepath):
  config.read(config_filepath)
else:
  messagebox.showerror("設定エラー", f"{config_filepath} が見つかりません。適切なconfig.iniを作成してください。")
  sys.exit()

# 'time'セクションと'start_time'キーの存在を確認
if 'time' not in config:
  messagebox.showerror("設定エラー", "config.ini に [time] セクションが見つかりません。")
  sys.exit()
if 'start_time' not in config['time']:
  messagebox.showerror("設定エラー", "config.ini の [time] セクションに start_time キーが見つかりません。")
  sys.exit()

try:
  # start_timeを文字列として取得し、datetimeオブジェクトに変換
  # '%H:%M:%S'形式を想定
  start_time_str = config['time']['start_time']
  # 例えば今日の日付と結合してdatetimeオブジェクトを作成（日付自体は計算に影響しない）
  dummy_date = datetime.now().date()
  current_time_dt = datetime.combine(dummy_date, datetime.strptime(start_time_str, '%H:%M:%S').time())
except ValueError:
  messagebox.showerror("設定エラー", "config.iniのstart_timeは 'HH:MM:SS' 形式で指定してください。")
  sys.exit()

time_start = []
time_finish = []

# duration列が存在することを確認
if "duration" not in df_sche.columns:
  messagebox.showerror("データエラー", "schedule.csv に 'duration' 列が見つかりません。")
  sys.exit()

for duration in df_sche["duration"]:
  time_start.append(current_time_dt.strftime('%H:%M:%S')) # 現在の時刻を文字列で追加
  
  # durationをtimedeltaに変換して加算
  # durationが分単位の数値であると仮定
  try:
    duration_delta = timedelta(minutes=int(duration))
  except ValueError:
    messagebox.showerror("データエラー", f"duration列の値が無効です: '{duration}' は数値である必要があります。")
    sys.exit()
  
  current_time_dt = current_time_dt + duration_delta
  time_finish.append(current_time_dt.strftime('%H:%M:%S')) # 計算後の時刻を文字列で追加

df_sche.insert(0, 'time_fin', time_finish)
df_sche.insert(0, 'time_sta', time_start)

# --- Tkinter アプリケーション部分 ---

def show_dataframe_treeview(df_to_display): # 引数名を変更して衝突を避ける
  """
  Pandas DataFrameをttk.Treeviewに表示し、列幅を自動調整する関数
  """
  # Treeviewをクリア
  for item in tree.get_children():
    tree.delete(item)

  # カラムを設定
  tree["columns"] = list(df_to_display.columns)
  tree["show"] = "headings" # ヘッダーのみ表示

  # フォントオブジェクトを一度だけ作成
  default_font = tkFont.Font()

  for col in df_to_display.columns:
    tree.heading(col, text=col)

    # ヘッダーのテキスト幅を取得
    header_width = default_font.measure(col)

    # 列内の最大データ幅を計算
    max_data_width = 0
    if not df_to_display[col].empty: # DataFrameが空でない場合のみ計算
      # 各セルを文字列に変換し、その中で最も長い文字列の幅を取得
      max_data_width = df_to_display[col].astype(str).apply(default_font.measure).max()

    # ヘッダーとデータの幅を比較し、より大きい方を採用 + 余白
    column_width = max(header_width, max_data_width) + 20 # 20はパディング

    tree.column(col, width=column_width, anchor="w") # anchor="w" で左寄せ

  # データを挿入
  for index, row in df_to_display.iterrows():
    tree.insert("", "end", values=list(row))

root = tk.Tk()
root.title("DataFrame Treeview 表示")
root.geometry("800x400") # ウィンドウサイズを少し大きくして確認しやすくする

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame)
tree.pack(side="left", fill="both", expand=True)

# スクロールバー
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
tree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
hsb.pack(side="bottom", fill="x")
tree.configure(xscrollcommand=hsb.set)

# ボタンの代わりに、アプリケーション起動時に直接関数を呼び出す
# df_band の代わりに df_sche を表示
show_dataframe_treeview(df_sche)

def close():
  df_sche.to_csv("../assets/data/schedule.csv", index=False) # index=False でインデックスを保存しない
  messagebox.showinfo("保存完了", "schedule.csv にスケジュールが保存されました。")
  root.destroy()

button = tk.Button(root, text="正常に作成されていることを確認したら押してください。", command=close)
button.pack()

root.mainloop()