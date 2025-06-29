import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser
import os
import datetime # datetimeモジュールを追加

# カレントディレクトリを本ファイルが存在するフォルダに変更。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ConfigApp:
  def __init__(self, root):
    self.root = root
    self.root.title("設定ツール")
    self.root.geometry("550x450") # 少しウィンドウサイズを大きく

    self.config_filepath = "../assets/config.ini" # デフォルトの設定ファイル名
    
    # アプリケーション起動時に設定ファイルをチェックし、存在しなければ初期作成
    if not os.path.exists(self.config_filepath):
      self._create_initial_config_file()

    # ConfigParser インスタンスを初期化
    self.config = configparser.ConfigParser()

    # 設定項目を保存する辞書（エントリウィジェットの参照用）
    self.config_entries = {}

    # --- ファイル操作フレーム ---
    file_frame = ttk.LabelFrame(root, text="設定ファイルの操作")
    file_frame.pack(padx=10, pady=10, fill=tk.X)

    self.file_path_label = ttk.Label(file_frame, text=f"ファイルパス: {self.config_filepath}")
    self.file_path_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    select_file_button = ttk.Button(file_frame, text="ファイル選択", command=self.select_config_file)
    select_file_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # --- 設定項目表示フレーム ---
    settings_frame = ttk.LabelFrame(root, text="設定項目")
    settings_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    self.canvas = tk.Canvas(settings_frame)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    self.scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=self.canvas.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill="y")

    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    # キャンバスのサイズが変更されたときにスクロール領域を更新
    self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

    self.inner_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

    # --- 操作ボタン ---
    button_frame = ttk.Frame(root)
    button_frame.pack(padx=10, pady=10, fill=tk.X)

    save_button = ttk.Button(button_frame, text="設定を保存", command=self.save_config)
    save_button.pack(side=tk.LEFT, padx=5, expand=True)

    load_button = ttk.Button(button_frame, text="設定を再読み込み", command=self.load_config)
    load_button.pack(side=tk.LEFT, padx=5, expand=True)

    add_section_button = ttk.Button(button_frame, text="セクション追加", command=self.add_section_dialog)
    add_section_button.pack(side=tk.LEFT, padx=5, expand=True)

    add_option_button = ttk.Button(button_frame, text="項目追加", command=self.add_option_dialog)
    add_option_button.pack(side=tk.LEFT, padx=5, expand=True)

    # アプリケーション起動時に設定を読み込む
    self.load_config()

  def _create_initial_config_file(self):
    """
    config.ini ファイルが存在しない場合に初期設定で作成するヘルパー関数
    """
    initial_config = configparser.ConfigParser()
    initial_config['time'] = {
      'start_time': datetime.time(9, 0, 0).strftime("%H:%M:%S")
    }
    initial_config['general'] = {
      'app_name': 'My Tkinter App',
      'version': '1.0',
      'debug_mode': 'False' # ブール値も文字列で保存
    }

    try:
      with open(self.config_filepath, 'w', encoding='utf-8') as configfile:
        initial_config.write(configfile)
      messagebox.showinfo("初期設定ファイル作成", f"'{self.config_filepath}' を初期設定で作成しました。")
    except Exception as e:
      messagebox.showerror("エラー", f"初期設定ファイルの作成中にエラーが発生しました:\n{e}")

  def _get_time_from_string(self, time_str):
    """
    "HH:MM:SS" 形式の文字列を datetime.time オブジェクトに変換
    """
    try:
      return datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
      return None # 変換失敗時はNoneを返すなど、エラーハンドリングを考慮

  def load_config(self):
    """設定ファイルを読み込み、GUIに表示する"""
    # 既存のウィジェットをクリア
    for widget in self.inner_frame.winfo_children():
      widget.destroy()

    self.config_entries = {} # 辞書もクリア
    self.config = configparser.ConfigParser() # 新しいConfigParserインスタンスでクリア

    if os.path.exists(self.config_filepath):
      self.config.read(self.config_filepath, encoding='utf-8')
      self.file_path_label.config(text=f"ファイルパス: {self.config_filepath} (読み込み済み)")
      messagebox.showinfo("読み込み完了", f"'{self.config_filepath}' から設定を読み込みました。")
    else:
      # ここに到達することは_create_initial_config_file()で防がれるが、念のため
      messagebox.showwarning("ファイルなし", f"'{self.config_filepath}' が見つかりませんでした。新規作成されます。")
      self.file_path_label.config(text=f"ファイルパス: {self.config_filepath} (新規)")
      # ファイルが存在しない場合、空のConfigParserオブジェクトのまま進む

    row_idx = 0
    for section in self.config.sections():
      # セクション名表示
      section_label = ttk.Label(self.inner_frame, text=f"[{section}]", font=("Arial", 10, "bold"))
      section_label.grid(row=row_idx, column=0, columnspan=3, sticky="w", padx=5, pady=(10, 2))
      row_idx += 1

      for key, value in self.config.items(section):
        label = ttk.Label(self.inner_frame, text=f"{key}:")
        label.grid(row=row_idx, column=0, sticky="w", padx=15, pady=2)

        entry = ttk.Entry(self.inner_frame, width=40)
        entry.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
        entry.insert(0, value)

        # 削除ボタン
        delete_button = ttk.Button(self.inner_frame, text="削除",
                                   command=lambda s=section, k=key: self.delete_option(s, k))
        delete_button.grid(row=row_idx, column=2, sticky="e", padx=5, pady=2)

        # エントリウィジェットの参照を保存
        if section not in self.config_entries:
          self.config_entries[section] = {}
        self.config_entries[section][key] = entry
        row_idx += 1

      # セクション削除ボタン
      delete_section_button = ttk.Button(self.inner_frame, text=f"[{section}] セクション削除",
                                         command=lambda s=section: self.delete_section(s))
      delete_section_button.grid(row=row_idx, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
      row_idx += 1

    self.inner_frame.update_idletasks()
    self.canvas.config(scrollregion=self.canvas.bbox("all"))

  def save_config(self):
    """GUIの入力内容を設定ファイルに保存する"""
    try:
      # 現在の ConfigParser オブジェクトをGUIの入力内容で更新
      # この段階ではセクションやオプションの追加は行わず、
      # 既存のEntryウィジェットの内容をConfigParserに反映する
      for section_name in self.config_entries:
        if not self.config.has_section(section_name):
          # GUIで追加されたセクションはここでConfigParserに追加される
          self.config.add_section(section_name)
        for key, entry_widget in self.config_entries[section_name].items():
          self.config.set(section_name, key, entry_widget.get())

      with open(self.config_filepath, 'w', encoding='utf-8') as configfile:
        self.config.write(configfile)

      self.file_path_label.config(text=f"ファイルパス: {self.config_filepath} (保存済み)")
      messagebox.showinfo("保存完了", f"設定を'{self.config_filepath}'に保存しました。")
    except Exception as e:
      messagebox.showerror("保存エラー", f"設定の保存中にエラーが発生しました:\n{e}")

  def select_config_file(self):
    """設定ファイルのパスを選択するダイアログを開く"""
    filepath = filedialog.asksaveasfilename(
      defaultextension=".ini",
      filetypes=[("INI files", "*.ini"), ("All files", "*.*")],
      title="設定ファイルを保存/開く"
    )
    if filepath:
      self.config_filepath = filepath
      self.file_path_label.config(text=f"ファイルパス: {self.config_filepath}")
      self.load_config() # 新しいファイルパスで読み込み直す

  def add_section_dialog(self):
    """新しいセクションを追加するためのダイアログを表示"""
    dialog = tk.Toplevel(self.root)
    dialog.title("セクション追加")
    dialog.geometry("300x120") # 少し広めに
    dialog.transient(self.root) # 親ウィンドウの上に表示
    dialog.grab_set() # 親ウィンドウの操作をロック
    dialog.resizable(False, False) # サイズ変更不可

    tk.Label(dialog, text="新しいセクション名:").pack(pady=5)
    section_entry = ttk.Entry(dialog, width=30)
    section_entry.pack(pady=5)
    section_entry.focus_set() # 初期フォーカス

    def add_section():
      section_name = section_entry.get().strip()
      if section_name:
        if not self.config.has_section(section_name):
          self.config.add_section(section_name)
          # 新しく追加したセクションも config_entries に含める準備
          self.config_entries[section_name] = {}
          messagebox.showinfo("追加完了", f"セクション '{section_name}' を追加しました。")
          self.load_config() # GUIを更新
          dialog.destroy()
        else:
          messagebox.showwarning("エラー", f"セクション '{section_name}' は既に存在します。")
      else:
        messagebox.showwarning("エラー", "セクション名を入力してください。")

    ttk.Button(dialog, text="追加", command=add_section).pack(pady=5)
    self.root.wait_window(dialog) # ダイアログが閉じるまで待機

  def add_option_dialog(self):
    """新しい項目（オプション）を追加するためのダイアログを表示"""
    dialog = tk.Toplevel(self.root)
    dialog.title("項目追加")
    dialog.geometry("300x220") # 少し広めに
    dialog.transient(self.root)
    dialog.grab_set()
    dialog.resizable(False, False)

    tk.Label(dialog, text="セクション名:").pack(pady=5)
    # 現在の設定にあるセクションを候補にする
    sections_available = self.config.sections()
    section_combobox = ttk.Combobox(dialog, values=sections_available, width=27)
    section_combobox.pack(pady=5)
    if sections_available:
      section_combobox.set(sections_available[0]) # デフォルトで最初のセクションを選択
    else:
      section_combobox.set("新しいセクション") # セクションがない場合

    tk.Label(dialog, text="項目名 (キー):").pack(pady=5)
    key_entry = ttk.Entry(dialog, width=30)
    key_entry.pack(pady=5)

    tk.Label(dialog, text="値:").pack(pady=5)
    value_entry = ttk.Entry(dialog, width=30)
    value_entry.pack(pady=5)
    
    key_entry.focus_set() # 初期フォーカス

    def add_option():
      section_name = section_combobox.get().strip()
      key_name = key_entry.get().strip()
      value = value_entry.get()

      if not section_name:
        messagebox.showwarning("エラー", "セクション名を選択または入力してください。")
        return
      if not key_name:
        messagebox.showwarning("エラー", "項目名を入力してください。")
        return

      if not self.config.has_section(section_name):
        self.config.add_section(section_name)
        # GUI表示を更新するためにconfig_entriesにも追加
        self.config_entries[section_name] = {}
      
      # オプションが既に存在するか確認
      if self.config.has_option(section_name, key_name):
        messagebox.showwarning("エラー", f"セクション '{section_name}' に項目 '{key_name}' は既に存在します。\n既存の項目を編集してください。")
        return

      self.config.set(section_name, key_name, value)
      messagebox.showinfo("追加完了", f"セクション '{section_name}' に項目 '{key_name}={value}' を追加しました。")
      self.load_config() # GUIを更新
      dialog.destroy()

    ttk.Button(dialog, text="追加", command=add_option).pack(pady=5)
    self.root.wait_window(dialog)

  def delete_option(self, section, key):
    """指定されたセクションから項目を削除する"""
    if messagebox.askyesno("確認", f"セクション '{section}' から項目 '{key}' を削除しますか？"):
      self.config.remove_option(section, key)
      # config_entriesからも削除
      if section in self.config_entries and key in self.config_entries[section]:
        del self.config_entries[section][key]
        if not self.config_entries[section]: # セクションが空になったら、そのセクションエントリも削除
          del self.config_entries[section]
      messagebox.showinfo("削除完了", f"項目 '{key}' を削除しました。")
      self.load_config() # GUIを更新

  def delete_section(self, section):
    """指定されたセクションを削除する"""
    if messagebox.askyesno("確認", f"セクション '{section}' を削除しますか？\n(全ての項目も削除されます)"):
      self.config.remove_section(section)
      # config_entriesからも削除
      if section in self.config_entries:
        del self.config_entries[section]
      messagebox.showinfo("削除完了", f"セクション '{section}' を削除しました。")
      self.load_config() # GUIを更新


if __name__ == "__main__":
  root = tk.Tk()
  app = ConfigApp(root)

  # 追加された close 関数とボタン
  def close():
    root.destroy()

  button = tk.Button(root, text="正常に作成されていることを確認したら押してください。", command=close)
  button.pack()

  root.mainloop()