import requests
import xml.dom.minidom
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import matplotlib.cbook as cbook
import locale
import pandas as pd

years = mdates.YearLocator() #every year
months = mdates.MonthLocator() #every month
years_fmt = mdates.DateFormatter('%Y')
#
url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2010&date_req2=31/12/2020&VAL_NM_RQ=R01235'
r = requests.get(url)#Пиздим строку из
dom = xml.dom.minidom.parseString(r.text)#загоняем строку в парсер
dom.normalize()
nodeArray = dom.getElementsByTagName("ValCurs")[0]
dates = []
kurses = []
#
locale.setlocale(locale.LC_ALL, 'fr_FR')
for rec in nodeArray.childNodes:
###
  #Lấy một phần tử nạp vào string datesrec_str
  datesrec_str = rec.getAttribute("Date")
  #Covert string to datetim
  datesrec_datetime = datetime.strptime(datesrec_str, '%d.%m.%Y')#Chuyển đổi dữ liệu dưới dạng datetime
  #Nạp vào mảng dates[]
  dates.append(datesrec_datetime)#Nạp dự liệu vào mạng dates

  #lấy một phần tử string "Giá trị hối đoái"
  kurses_rec = rec.childNodes[1].childNodes[0].nodeValue
  #Covert string to float
  kurses_rec_float = locale.atof(kurses_rec)
  #Nạp vào mảng kures.
  kurses.append(kurses_rec_float)

#Chọn kích thước khung hình cho đồ thị
fig, ax = plt.subplots(figsize = (16, 9))

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)

# format the coords message box
ax.format_xdata = mdates.DateFormatter('%d.%m.%Y')

#Tiêu đề chung.
plt.title("График ретроспективной динамики курса валют к рублю 2010 - 2020")\
#Tiêu đề trục hoành.
plt.xlabel("День.Месяц.Год")
#Tiêu đều trục tung.
plt.ylabel("Курса валют")

#Chuyển kiểu json
d = {'col1':dates, 'col2':kurses}

# DataFrame.
df = pd.DataFrame(d)

#Thiết lập tên cho cột
df.columns=['ds','y']

#short_rolling SMA - 20
short_rolling = df.y.rolling(window=20).mean()
#short_rolling.head(20)

#long_rolling
long_rolling = df.y.rolling(window = 100).mean()

#Thiết lập đồ thị
plt.plot(df.ds, df.y,label = "Обменный курс", color = "green")
plt.plot(df.ds, short_rolling, label = "Обменный курс", color = "yellow")
plt.plot(df.ds, long_rolling, color = "red")

#Hiển thị đồ thị
plt.show()
#
