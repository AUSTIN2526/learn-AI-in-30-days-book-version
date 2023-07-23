from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def run(y_lim, m_lim, stockNo):
    for y in range(2010, y_lim + 1):
        for m in range(1 , m_lim + 1):
            # 開啟瀏覽器前往網站
            m = m if len(str(m)) > 1 else f'0{m}'
            url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={y}{m}01&stockNo={stockNo}'
            chrome.get(url)
            
            # 解析網站資訊
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            
            # 取得所需的資料
            data_list = get_web_data(soup)
            
            # 儲存資料
            save_csv(data_list, y, m, stockNo)
            
            # 防止過度請求
            time.sleep(10)
        
def get_web_data(soup):

    # 透過CSS選擇器定位元素
    web_datas  = soup.select('body > div > table > tbody')
    
    # 將資料轉換成字串
    web_datas = list(web_datas)[0]
    input(type(web_datas))
    # 移除表格換行\n\n與資料欄內的空白
    filter_datas = web_datas.replace('\n\n','').replace(' ','')
    
    # 將字串轉換成List方便後續處理
    data_list = filter_datas.split('\n')
    
    return data_list
    
def save_csv(data_list, y, m, stockNo):
    # 使用字典紀錄網站資訊
    web_record = {'日期':[],'成交股數':[],'成交金額':[],'開盤價':[],'最高價':[],'最低價':[],'收盤價':[],'漲跌價差':[],'成交筆數':[]}
    
    # 判斷資料與字典長度方便後續計算
    data_length, dict_length = len(data_list), len(web_record)
    
    # 計算第一層數量(總資料/字典長度)
    for i in range(data_length//dict_length):
        # 取得字典的Key與資料的row
        for j, key in enumerate(web_record):
            # 計算List的索引
            index = i * dict_length + j
            # 新增資料到Key對應的List中
            web_record[key].append(data_list[index])
    # 轉換成DataFrame方便後續儲存
    df = pd.DataFrame(web_record)
    
    # 儲存資料為utf-8格式
    df.to_csv(f"{stockNo} {y}-{m}.csv", encoding = 'utf-8-sig', index = False)
    
    


# 修改User-Agent
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
chrome = webdriver.Chrome(options=chrome_options) 

# 設定參數
y_lim = 2022
m_lim = 12
stockNo = 2330

run(y_lim, m_lim, stockNo)
