import fitz
import os
from tqdm import tqdm
import pandas as pd
import pypdf

#カレントディレクトリの移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#PDF内のテキストを検索する関数の定義(by ChatGPT)
def search_text_in_pdf(pdf_path, search_text):
  # PDFファイルを開く
  pdf_document = fitz.open(pdf_path)
  # 検索結果のページ番号リスト
  pages_with_text = []
  
  # 各ページをループし、テキストを検索
  for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    text = page.get_text()
    
    # テキストが含まれているかを確認
    if str(search_text) in text:
      pages_with_text.append(page_num + 1)  # ページ番号は1から始まるように+1
  # PDFファイルを閉じる
  pdf_document.close()
  
  return pages_with_text

folder_name = os.path.join("cache", "SeparatePDFApp")
pdf_path = os.path.join(folder_name, "審査フィードバックシート.pdf")
base_pdf = pypdf.PdfReader(pdf_path)

output_path = os.path.join(folder_name, "feedback")

df1 = pd.read_csv(os.path.join(folder_name, "bandlist.csv"))

err=[]

for i in tqdm(range(0, len(df1))):
  
  search_text = df1.at[i, "Band ID"]
  result = search_text_in_pdf(pdf_path, search_text)
  if i == len(df1)-1:
    nresult = [len(base_pdf.pages)]
  else:
    search_ntext = df1.at[i+1, "Band ID"]
    nresult = search_text_in_pdf(pdf_path, search_ntext)
  
  print(result, nresult)
  
  if len(result) == 0:
    err.append(df1.at[i, "Band ID"])
    continue
  elif len(nresult) == 0:
    err.append(df1.at[i+1, "Band ID"])
    continue
  
  pdf_writer = pypdf.PdfWriter()
  for j in range(result[0], nresult[0]):
    pdf_writer.add_page(base_pdf.pages[j-1])
  pdf_writer.write(output_path + "/" + "千葉大祭2025ステージ企画審査一次審査フィードバックシート_" + df1.at[i, "Number"] + "_" + df1.at[i, "Name"] + ".pdf")
  pdf_writer.close()

print(err)