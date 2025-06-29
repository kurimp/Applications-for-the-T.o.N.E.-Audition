import csv
import random
import numpy as np
from datetime import datetime, time as dt_time, timedelta
import ast
import pandas as pd
import time
import os

# カレントディレクトリを本ファイルが存在するフォルダに変更。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

band_file_path = '../assets/data/band.csv'
sche_file_path = '../assets/data/schedule.csv'

df_sche = pd.read_csv(sche_file_path)
df_band = pd.read_csv(band_file_path)

df_band = df_band.fillna('')

df_band['unavailable_time'] = [[cell] for cell in df_band['unavailable_time']]

def give_num(n):
  num = np.arange(0, n, 1)
  random.shuffle(num)
  return num

def clean_list(input_list):
  cleaned_items = []
  for item in input_list:
    # itemがNoneでなく、かつ、文字列に変換してstrip()した結果が空でないことを確認
    if item is not None and str(item).strip() != '':
      cleaned_items.append(str(item).strip()) # 前後の空白を除去して追加
  return cleaned_items

def has_common_elements(list1, list2, ignore_case=False):
  # リストをクリーンアップ
  cleaned_list1 = clean_list(list1)
  cleaned_list2 = clean_list(list2)

  # 大文字・小文字を無視する場合、要素を小文字に変換
  if ignore_case:
    cleaned_list1 = [item.lower() for item in cleaned_list1]
    cleaned_list2 = [item.lower() for item in cleaned_list2]

  # クリーンアップされたリストを集合に変換
  set1 = set(cleaned_list1)
  set2 = set(cleaned_list2)

  # 2つの集合の積集合（共通要素）を計算
  common_elements_set = set1 & set2
  
  # 積集合が空でなければ、共通の要素が存在する
  return len(common_elements_set) > 0

#連続なしになった並びが出演可能時間に該当しているかを判定する関数。
def time_judge(res):
  i = 0
  for band in res:
    i += 1
    block_start_time = df_sche[df_sche['item']==str(i)]['time_sta'].iloc[0]
    block_finish_time = df_sche[df_sche['item']==str(i)]['time_fin'].iloc[0]
    block_start_time = datetime.strptime(block_start_time, '%H:%M:%S').time()
    block_finish_time = datetime.strptime(block_finish_time, '%H:%M:%S').time()
    unavailable_time = df_band[df_band['name']==band[0]]['unavailable_time'].iloc[0]
    unavailable_time = [m.strip() for m in unavailable_time if m.strip()]
    unavailable_time = convert_time_strings_to_time_tuples(unavailable_time)
    status = is_time_frame_available(block_start_time, block_finish_time, unavailable_time)
    if not status:
      print("出演不可能時間に引っかかりました。残念。")
      break
  return status

def is_time_frame_available(start_time: dt_time, end_time: dt_time, unavailable_slots: list[tuple[dt_time, dt_time]]) -> bool:
  """
  指定された時間枠が、参加不可能な時間帯と重複していないかを確認します。
  
  Args:
    start_time (datetime): 確認したい時間枠の開始時刻。
    end_time (datetime): 確認したい時間枠の終了時刻。
    unavailable_slots (list[tuple[datetime, datetime]]): 参加不可能な時間帯のリスト。
                                                          各要素は(開始時刻, 終了時刻)のタプル。
  
  Returns:
    bool: 時間枠が参加不可能な時間帯と重複しない場合はTrue、重複する場合はFalse。
  """
  # 確認したい時間枠が有効か（開始時刻が終了時刻より前か）をチェック
  if start_time >= end_time:
    raise ValueError("時間枠の開始時刻は終了時刻より前である必要があります。")
  
  for unavailable_start, unavailable_end in unavailable_slots:
    # 参加不可能な時間帯が有効か（開始時刻が終了時刻より前か）をチェック
    if unavailable_start >= unavailable_end:
      raise ValueError(f"参加不可能な時間帯の開始時刻が終了時刻より前ではありません: ({unavailable_start}, {unavailable_end})")
    
    # 重複の条件:
    # (A.start <= B.end) and (A.end >= B.start)
    # ここではAが確認したい時間枠、Bが参加不可能な時間帯
    if (start_time < unavailable_end) and (end_time > unavailable_start):
      return False  # 重複が見つかった場合

  return True  # 重複が見つからなかった場合

def convert_time_strings_to_time_tuples(unavailable_slots_str: list[str]) -> list[tuple[dt_time, dt_time]]:
  """
  文字列のリストとして与えられた時間帯（例: ["09:00-10:00", "13:30-14:30"] や ["09:00:00-12:00:00,14:00:00-15:00:00"]）を
  datetime.timeオブジェクトのタプルのリストに変換します。
  """
  converted_slots = []
  for slot_group_str in unavailable_slots_str: # 各要素が単一または複数時間帯の文字列
    if not slot_group_str: # 空文字列はスキップ
      continue

    # ★修正点1: 1つの文字列に複数の時間帯が含まれている場合を考慮し、カンマで分割★
    # 例: "09:00:00-12:00:00,14:00:00-15:00:00" -> ["09:00:00-12:00:00", "14:00:00-15:00:00"]
    individual_slot_strings = [s.strip() for s in slot_group_str.split(',') if s.strip()]

    for slot_str in individual_slot_strings:
      try:
        # ハイフンで開始時刻と終了時刻に分割
        # 'too many values to unpack' はここで発生していた
        start_time_str, end_time_str = slot_str.split('-')
        
        # strptime を使って datetime.time オブジェクトに変換
        # ★修正点2: まず '%H:%M:%S' を試し、次に '%H:%M' を試す★
        parsed_start_time = None
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                parsed_start_time = datetime.strptime(start_time_str.strip(), fmt).time()
                break # 成功したらループを抜ける
            except ValueError:
                continue # 次のフォーマットを試す
        
        parsed_end_time = None
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                parsed_end_time = datetime.strptime(end_time_str.strip(), fmt).time()
                break # 成功したらループを抜ける
            except ValueError:
                continue # 次のフォーマットを試す
        
        if parsed_start_time and parsed_end_time:
            converted_slots.append((parsed_start_time, parsed_end_time))
        else:
            # どちらかのパースが完全に失敗した場合
            print(f"警告: 時間帯 '{slot_str}' の時刻部分のパースに失敗しました。スキップします。")
            continue

      except ValueError as e:
        print(f"警告: 時間帯 '{slot_str}' の形式が不正です（ハイフン区切りでないか、余分なカンマ）。スキップします。エラー: {e}")
        continue
  return converted_slots

with open(band_file_path, 'r', newline='', encoding='utf-8') as csvfile:
  reader = csv.DictReader(csvfile)
  
  bandlist = []
  
  for row in reader:
    band_name = row['name']
    member_string = row['member']
    
    members_list = ast.literal_eval(member_string)
    members = [m.strip() for m in members_list if m.strip()]
    
    bandlist.append([band_name, members])
  
  count = 0
  
  start = time.time()
  
  times = np.zeros(len(bandlist))
  
  while True:
    count += 1
    if count % 1000000 == 0:
      now = time.time()
      elapsed_time = now - start
      print(f"{count}回目の試行。経過時間は{elapsed_time:.1f}秒。")
    num = give_num(len(bandlist))
    res = []
    j = 0
    for i in num:
      res.append(bandlist[i])
      if j != 0:
        status = has_common_elements(res[j-1][1], res[j][1], ignore_case=False)
        if status == True:
          break
      j += 1
    times[j-1] += 1
    if (j == len(num)) and time_judge(res):
      print("並べ替えが終了しました。やったね。")
      break
    elif count == 100000000:
      print("条件に合う組み合わせを見つけるのに失敗しました。残念。")
      break

now = time.time()
elapsed_time = now - start

print("-"*30)
for item in res:
  print(item[0])
  print("")
print(f"試行回数は{count}回。経過時間は{elapsed_time:.1f}秒。")
print("-"*30)

number = np.arange(1, len(times)+1, 1)

output_folder_path = '../../output/'

os.makedirs(output_folder_path, exist_ok=True)

output_folder_path = os.path.join(output_folder_path, 'result.csv')

with open(output_folder_path, 'w', encoding='utf-8') as out:
  out.write("number\t"
            "count")
  for i in range(len(times)):
    out.write(f"\n{number[i]}\t"
              f"{times[i]:.1f}")