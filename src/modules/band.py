import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont
import numpy as np
import csv # csvモジュールを明示的にインポート
import re # 正規表現モジュールをインポート
import datetime

# カレントディレクトリを本ファイルが存在するフォルダに変更。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- DataFrameの前処理関数 ---
def preprocess_dataframe(df):
  """
  DataFrameの前処理を行う関数。
  band.csvの特定の列を結合し、整形します。
  """
  # NaNを空白（空文字列）に置換
  df = df.fillna('')

  # 'no'列を追加
  num = np.arange(1, len(df)+1, 1)
  df.insert(0, "no", num)
  df.insert(2, "unavailable_time", "")

  # 選択された列を'member'列にリストとしてまとめる
  selected_columns = ['1', '2', '3', '4', '5', '6', '7']
  # 存在しない列は処理しないようにチェック
  existing_selected_columns = [col for col in selected_columns if col in df.columns]
  if existing_selected_columns:
    df['member'] = df[existing_selected_columns].values.tolist()
    df = df.drop(existing_selected_columns, axis="columns")
  
  return df

# --- CSVEditorクラスの定義 ---
class CSVEditor:
  def __init__(self, master, initial_filepath="../../data/band.csv", save_filepath="../assets/data/band.csv"):
    self.master = master
    master.title("CSV Editor (band.csv)")
    master.geometry("800x600")
    
    self.original_filepath = os.path.abspath(initial_filepath) # 元のファイルの絶対パスを保持
    self.filepath = os.path.abspath(save_filepath) # 保存時のパスとして初期設定
    self.df = pd.DataFrame() # DataFrameを保持する変数
    self.data_raw = [] # Treeviewの編集に使用する生データ（リストのリスト）

    # フレームの作成
    self.frame = ttk.Frame(master, padding="10")
    self.frame.pack(fill=tk.BOTH, expand=True)

    # Treeview (CSVデータの表示用)
    self.tree = ttk.Treeview(self.frame, show="headings")
    self.tree.pack(fill=tk.BOTH, expand=True)

    self.tree.bind("<Double-1>", self.on_cell_double_click) # セルダブルクリックで編集可能にする
    
    #入力ステータスの表示
    self.status_label = ttk.Label(self.frame, text = "出演不可能時間のみここで記入してください。記入の際は、以下の記入例に忠実に従ってください。なお、スペースは自動で消去します。\n09:00:00-13:00:00,15:00:00-16:00:00", anchor = "w")
    self.status_label.pack(side=tk.TOP, fill=tk.X, pady=2)

    # スクロールバー
    self.yscroll = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
    self.xscroll = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
    self.tree.configure(yscrollcommand=self.yscroll.set, xscrollcommand=self.xscroll.set)
    self.yscroll.pack(side="right", fill="y")
    self.xscroll.pack(side="bottom", fill="x")
    
    # ファイル操作ボタン
    self.save_button = ttk.Button(self.frame, text="Save CSV", command=self.save_csv, state=tk.DISABLED)
    self.save_button.pack(side=tk.TOP, pady=2)
    
    # 閉じるボタン
    self.close_button = tk.Button(master, text="閉じる", command=self.close_application)
    self.close_button.pack(pady=10)
    
    # アプリケーション起動時に元のCSVを読み込み、表示
    self.load_initial_csv()

  def load_initial_csv(self):
    """初期のCSVファイルを読み込み、前処理して表示する"""
    if os.path.exists(self.original_filepath):
      try:
        # pandasで読み込み、前処理
        df_raw = pd.read_csv(self.original_filepath)
        self.df = preprocess_dataframe(df_raw.copy()) # 前処理後のDataFrame
        
        # Treeview表示用の生データを準備
        # ヘッダーとデータ部分をリストのリストとして保持
        self.data_raw = [list(self.df.columns)] + self.df.values.tolist()
        
        self.display_data_in_treeview(self.df)
        self.save_button.config(state=tk.NORMAL)
      except Exception as e:
        messagebox.showerror("Error", f"Failed to load initial CSV: {e}")
    else:
      messagebox.showwarning("Warning", f"Initial CSV file not found: {self.original_filepath}")

  def open_csv(self):
    """新しいCSVファイルを開く"""
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
      self.filepath = filepath # 開いたファイルを保存パスとする
      try:
        # pandasで読み込み、前処理
        df_raw = pd.read_csv(filepath)
        self.df = preprocess_dataframe(df_raw.copy()) # 前処理後のDataFrame
        
        # Treeview表示用の生データを準備
        self.data_raw = [list(self.df.columns)] + self.df.values.tolist()
        
        self.display_data_in_treeview(self.df)
        self.save_button.config(state=tk.NORMAL)
        self.master.title(f"CSV Editor - {os.path.basename(filepath)}")
      except Exception as e:
        messagebox.showerror("Error", f"Failed to open CSV: {e}")

  def display_data_in_treeview(self, df_to_display):
    """
    Pandas DataFrameをttk.Treeviewに表示し、列幅を自動調整する関数
    編集機能のために、元のデータはdfで管理し、表示用と編集用で分けています。
    """
    # Treeviewをクリア
    for item in self.tree.get_children():
      self.tree.delete(item)

    if df_to_display.empty:
      return

    # カラムを設定
    self.tree["columns"] = list(df_to_display.columns)
    self.tree["show"] = "headings" # ヘッダーのみ表示

    # フォントオブジェクトを一度だけ作成
    default_font = tkFont.Font()

    for col in df_to_display.columns:
      self.tree.heading(col, text=col)

      # ヘッダーのテキスト幅を取得
      header_width = default_font.measure(col)

      # 列内の最大データ幅を計算
      max_data_width = 0
      if not df_to_display[col].empty: # DataFrameが空でない場合のみ計算
        # 各セルを文字列に変換し、その中で最も長い文字列の幅を取得
        max_data_width = df_to_display[col].astype(str).apply(default_font.measure).max()

      # ヘッダーとデータの幅を比較し、より大きい方を採用 + 余白
      column_width = max(header_width, max_data_width) + 20 # 20はパディング

      self.tree.column(col, width=column_width, anchor="w") # anchor="w" で左寄せ

    # データを挿入
    # DataFrameのデータをTreeviewに挿入
    for index, row in df_to_display.iterrows():
      self.tree.insert("", "end", iid=index, values=list(row)) # iidにDataFrameのインデックスを使用

  def on_cell_double_click(self, event):
    """Treeviewのセルがダブルクリックされたときに編集を可能にする"""
    region = self.tree.identify("region", event.x, event.y)
    if region == "heading": # ヘッダーのクリックは無視
      return
    

    item_id = self.tree.identify_row(event.y)
    column_id = self.tree.identify_column(event.x)

    if not item_id or not column_id:
      return

    # 選択されたセルの情報を取得
    # column_id は "#1" のような形式なので、数値に変換し、0-indexedにする
    column_index = int(column_id.replace("#", "")) - 1
    col_name = self.tree["columns"][column_index]
    
    if col_name != "unavailable_time":
      self.status_label.config(text="unavailable_time列のみ編集可能です。", foreground="orange")
      return
    
    # item_idはTreeviewに挿入したときのiid（DataFrameのインデックス）
    row_index_df = int(item_id) # DataFrameのインデックス

    # Treeviewの現在の値を直接編集するため、Treeviewから値を取得
    current_values = list(self.tree.item(item_id, "values"))
    if column_index >= len(current_values): # 列の範囲外アクセスを防ぐ
      return
    
    current_value = current_values[column_index]

    # 編集用のEntryウィジェットを作成
    x, y, width, height = self.tree.bbox(item_id, column_id)
    
    # もしbboxがNoneを返したら、描画されていない可能性があるので何もしない
    if x is None:
      return
    
    editor = ttk.Entry(
            self.tree,
            width=width
    )
    editor.place(x=x, y=y, width=width, height=height)
    editor.insert(0, current_value)
    editor.focus_set()
    
    
    def on_entry_lost_focus(event):
      new_value = editor.get()
      
      new_value = new_value.strip().replace(" ", "").replace("　", "")
      
      #入力値の検証
      self.validate_custom_format(new_value)
      
      # Treeviewの値を更新
      updated_values = list(self.tree.item(item_id, "values"))
      updated_values[column_index] = new_value
      self.tree.item(item_id, values=updated_values)
      
      # 元のDataFrameも更新
      # df.iloc[row_index_df, column_index_df] = new_value と同じ
      col_name = self.tree["columns"][column_index]
      self.df.loc[row_index_df, col_name] = new_value
      
      editor.destroy()
    
    
    editor.bind("<FocusOut>", on_entry_lost_focus)
    editor.bind("<Return>", on_entry_lost_focus)
  
  
  def extract_values_from_format(self, input_string):
    """
    入力された文字列から、(*)単体、もしくは(*),(*)などの*部分をリストで取り出す。

    Args:
      input_string (str): 抽出元となる文字列。

    Returns:
      list: 抽出された*部分の文字列のリスト。
    """
    if not isinstance(input_string, str):
      return [] # 文字列でない場合は空リストを返す

    # 文字列のトリム（前後空白除去）
    input_string = input_string.strip().replace(" ", "").replace("　", "")

    if not input_string:
      return [] # 空文字列の場合は空リストを返す

    # 正規表現パターンを定義
    # ()で囲まれた部分、またはカンマや文字列の区切りとなる部分を抽出
    # (?:,\s*)?: 非キャプチャグループで、カンマと空白が0回以上続くことを示す
    # \(([^)]*)\): ()で囲まれた部分。^)]* は閉じ括弧以外の0文字以上。
    # |              : または
    # ([^,()]+)    : カンマ、括弧を含まない1文字以上の部分。
    #                               これは単体の値や、括弧なしのカンマ区切りに対応。

    # パターンをコンパイル（パフォーマンス向上のため）
    # re.VERBOSE を使うと、正規表現にコメントを書くことができる（可読性向上）
    # re.IGNORECASE や re.DOTALL など、必要に応じてフラグを追加
    pattern = re.compile(r"""
      (?:,\s*)?           # 先行するカンマと空白（省略可能）
      (?:
        \(([^)]*)\)     # グループ1: 丸括弧で囲まれた内容（括弧自身は含まない）
        |               # OR
        ([^,()]+)       # グループ2: カンマ、丸括弧を含まない内容（単独の値）
      )
    """, re.VERBOSE)

    extracted_list = []
    matches = pattern.finditer(input_string) # finditerでマッチオブジェクトをイテレート

    for match in matches:
      # グループ1がマッチしていればその値を取得
      if match.group(1) is not None:
        extracted_list.append(match.group(1).strip())
      # グループ2がマッチしていればその値を取得
      elif match.group(2) is not None:
        extracted_list.append(match.group(2).strip())
    
    # 最後に、残った単体のカンマ区切りの値（例: "hoge,fuga" のhogeとfuga）を処理
    # これは、上記パターンが `(?:,\s*)?` で先行するカンマを消費するため
    # 最初の要素が括弧なしの場合や、複数の括弧なし要素が続く場合に必要
    if not extracted_list and input_string:
      # 括弧が全くなく、単純なカンマ区切り文字列の場合
      if ',' in input_string and not re.search(r'[\(\)]', input_string):
        extracted_list = [s.strip() for s in input_string.split(',')]
      # 括弧なしの単体文字列の場合
      elif not re.search(r'[\(\)]', input_string):
        extracted_list = [input_string]
    
    return extracted_list
  
  def validate_custom_format(self, new_value):
    #空欄の場合True
    if new_value == "":
      self.status_label.config(text="空欄", foreground="black")
      return True
    
    #許容される文字以外を含む場合False
    allowd_chars = re.compile(r"^[0-9:\-,]*$")
    if not allowd_chars.fullmatch(new_value):
      self.status_label.config(text="許容される文字は半角数字、コロン、ハイフン、カンマ、括弧のみです", foreground = "red")
      return False
    
    value_list = self.extract_values_from_format(new_value)
    print(value_list)
    
    all_valid = True
    for value in value_list:
      date_pattern_01 = re.compile(r"^\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}$")
      
      if date_pattern_01.fullmatch(value): # fullmatchは文字列全体がパターンに一致するか確認
        try:
          start, finish = value.split('-')
          
          def validate_time_format(time_str):
            h, m, s = map(int, time_str.split(":"))
            return 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59
          
          if not (validate_time_format(start) and validate_time_format(finish)):
            all_valid = False
        except ValueError:
          all_valid = False
          break
      else:
        all_valid = False
        break
    
    if all_valid:
      self.status_label.config(text="正しく入力されています。", foreground = "green")
      return True
    else:
      self.status_label.config(text="この入力は正しくありません。以下の例に忠実に入力してください。\n09:00:00-13:00:00,15:00:00-16:00:00", foreground = "red")
      return False
  
  def save_csv(self):
    """現在のファイルパスにCSVを保存する"""
    if not self.filepath:
      messagebox.showwarning("Warning", "No file is open to save.")
      return
    
    try:
      # 現在のTreeviewのデータをDataFrameに変換し直して保存
      # Treeviewから直接データを取り出すのではなく、self.dfの最新状態を保存
      self.df.to_csv(self.filepath, index=False, encoding='utf-8')
      messagebox.showinfo("Success", f"CSV file saved successfully to {os.path.basename(self.filepath)}!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to save CSV: {e}")

  def close_application(self):
    """アプリケーションを閉じる際に呼ばれるメソッド"""
    # 必要に応じて、閉じる前に変更を保存するか確認するダイアログなどを追加できます。
    # 例: if messagebox.askyesno("確認", "変更を保存しますか？"): self.save_csv()
    self.master.destroy()

# --- Tkinter アプリケーションの実行部分 ---
if __name__ == "__main__":
  root = tk.Tk()
  app = CSVEditor(root)
  root.mainloop()