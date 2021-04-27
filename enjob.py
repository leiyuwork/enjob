import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://employment.en-japan.com/search/issue_index_2010/',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'E13CC=dbc976628df4f995f150e50f11ca1d30; PHPSESSID=ca94tmafrjp2qp5d4rrfp1lon2; S13U35=1; '
              'not_display_ie7_8_alert_text=1; S13U20=6GEz7MhrYH; not_display_ie7_8_alert_modal=1; '
              '_kys=QEkRCHXQMp/UwA_.en-japan.com; LPREF=https%253A%252F%252Fwww.google.com%252F; LPID=--; '
              'LPDT=20210427213616; FPREF=https%253A%252F%252Fwww.google.com%252F; FPID=--; FPDT=20210427213616; '
              '__hd_ss=1619526977030; TAGKNIGHT_CONTROL_CLUSTER=132; '
              'AWSALB=RcIzgekppHcuMI1OE+nmTZXMk09+T'
              '+seFv7VjGakrOckQ8wbLuGKtbS5XgLa6uz75ENOV4nfGfTSukZjU0ljjhYHER5NjOkuiooY2LRLPIQDkFA2FlCd4GkUD7yX; '
              'AWSALBCORS=RcIzgekppHcuMI1OE+nmTZXMk09+T'
              '+seFv7VjGakrOckQ8wbLuGKtbS5XgLa6uz75ENOV4nfGfTSukZjU0ljjhYHER5NjOkuiooY2LRLPIQDkFA2FlCd4GkUD7yX; '
              '_kyp=QEkQBhnOpiHVppTw09kEA22fRapXoYJcPhXDMuGoGnKW8iasuApglw+FcWgQbQjVelce4UboScIgsiSK_.en-japan.com+eh'
              '+employment.en-japan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36',
}
for year in range(2006, 2022):

    url_1 = "https://employment.en-japan.com/search/issue_index_" + str(year) + "/"  # link of every year
    print(url_1)

    response_1 = requests.get(url_1, headers=headers)  # get url contents
    bs_obj_1 = BeautifulSoup(response_1.text, 'lxml')  # parse with beautifulsoup
    table_td_1 = bs_obj_1.find_all("td", class_="data")  # get the link tables

    for link in table_td_1:
        url_2 = "https://employment.en-japan.com/"+link.find('a', href=True).attrs['href']
        print(url_2)
        response_2 = requests.get(url_2, headers=headers)  # open everyday link
        bs_obj_2 = BeautifulSoup(response_2.text, 'lxml')  # parse with beautifulsoup
        # print(bs_obj_2)

        date = bs_obj_2.find("em", class_="date").text

        table_td_industry = bs_obj_2.find_all("h2", class_="title")  # get the link tables
        # print(table_td_industry)
        table_td_2 = bs_obj_2.find_all("tr")  # get the link tables

        for industries in table_td_industry:
            industry = industries.find("span").text

            for results in table_td_2[2:]:
                final = []
                firm = results.find("span", class_="name").text
                job_name = results.find("td", class_="job").text
                job_link = results.find('a', href=True).attrs['href']
                url_3 = "https://employment.en-japan.com/" + job_link
                print(url_3)
                response_3 = requests.get(url_3, headers=headers)  # open everyday link
                # print(response_2)
                bs_obj_3 = BeautifulSoup(response_3.text, 'lxml')  # parse with beautifulsoup
                # print(bs_obj_2)
                # time.sleep(3)
                catchphrase = bs_obj_3.find("div", class_="copyArea").text
                tb = pd.read_html(url_3)[1]
                tb_2 = pd.read_html(url_3)[2]
                bosyuyoko = tb.values.tolist()
                kaisyajyoho = tb_2.values.tolist()
                final.append(date)
                final.append(industry)
                final.append(firm)

                for item in bosyuyoko:
                    for a in item:
                        final.append(a)

                if len(bosyuyoko) < 15:
                    list_null = [""] * (15 - len(tb.values.tolist()))
                    final = final + list_null

                for item2 in kaisyajyoho:
                    for b in item2:
                        final.append(b)

                Item = pd.DataFrame([final])
                Item.to_csv(r"C:\Users\Ray94\Desktop\000.csv", mode='a', index=False, header=None, encoding="utf-8_sig")
                time.sleep(15)

