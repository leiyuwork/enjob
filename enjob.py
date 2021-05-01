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
    'Cookie': 'S13U20=6GEz7MhrYH; LPID=--; FPDT=20210427213616; FPID=--; '
              'FPREF=https%253A%252F%252Fwww.google.com%252F; E13CC=3ff74fde92f2386d4b2fe4b63b641a31; S13U35=1; '
              'not_display_ie7_8_alert_text=1; not_display_ie7_8_alert_modal=1; _kys=QEkRGcOJoZjTYA_.en-japan.com; '
              'PHPSESSID=og8k0gplm9lduu2do5npmai552; '
              'S13_SEARCH_HISTORY01_url=%2Fkeyword%2F%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%82%A8%E3%82%B0%E3%82%BC'
              '%2F%3Fkeywordtext%3D%25E3%2582%25B7%25E3%2582%25B9%25E3%2583%2586%25E3%2583%25A0%25E3%2582%25A8%25E3'
              '%2582%25B0%25E3%2582%25BC; S13_SEARCH_HISTORY01_upd=2021-04-28+15%3A50%3A26; '
              'S13_SEARCH_HISTORY01_str=%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%82%A8%E3%82%B0%E3%82%BC; '
              'S13_SEARCH_HISTORY01_are=1; S13URECENTWORKID=1070534%7C1075944%7C1076691%7C1072135; '
              '__hd_ss=1619594542596; LPREF=; LPDT=20210428163327; TAGKNIGHT_CONTROL_CLUSTER=132; '
              'AWSALB=OoQ/U3rnW5sk188UaAvWtkmnmIfTCaaqqR7+xrXau+lXQVM8zQ6MvWFw9p4eBMoQpJ8RwxSEyyCWIB6X'
              '/QJp0YiquEWeJju2FuNoOEmJezB/R4Nhup9vPS81Qepx; '
              'AWSALBCORS=OoQ/U3rnW5sk188UaAvWtkmnmIfTCaaqqR7+xrXau+lXQVM8zQ6MvWFw9p4eBMoQpJ8RwxSEyyCWIB6X'
              '/QJp0YiquEWeJju2FuNoOEmJezB/R4Nhup9vPS81Qepx; '
              '_kyp=QEkQBhnOpiHVppTw09kEA22fRapXoYJcPjY/1vGoGnKW8i7PSHBglw+Nk/h4bQjVelce4UboScIwTIiSKA_.en-japan.com'
              '+eh+employment.en-japan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Connection': 'keep-alive',
}
for year in range(2007, 2008):

    url_1 = "https://employment.en-japan.com/search/issue_index_" + str(year) + "/"  # link of every year
    print(url_1)

    response_1 = requests.get(url_1, headers=headers)  # get url contents
    bs_obj_1 = BeautifulSoup(response_1.text, 'lxml')  # parse with beautifulsoup
    table_td_1 = bs_obj_1.find_all("td", class_="data")  # get the link tables

    for link in table_td_1:
        url_2 = "https://employment.en-japan.com"+link.find('a', href=True).attrs['href']
        print(url_2)
        response_2 = requests.get(url_2, headers=headers)  # open everyday link
        bs_obj_2 = BeautifulSoup(response_2.text, 'lxml')  # parse with beautifulsoup
        # print(bs_obj_2)

        date = bs_obj_2.find("em", class_="date").text
        table_list = bs_obj_2.find_all("div", class_="listBase")

        for firms in table_list:
            # print(firms)

            for results in firms.find_all("tr"):
                final = []

                industry = firms.find("span").text
                company_name = results.find("span", class_="name").text
                job_name = results.find("td", class_="job").text
                job_link = results.find('a', href=True).attrs['href']

                url_3 = "https://employment.en-japan.com" + job_link
                print(url_3)
                try:
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
                    final.append(url_2)
                    final.append(url_3)
                    final.append(date)
                    final.append(industry)
                    final.append(company_name)
                    final.append(job_name)
                    final.append(catchphrase)

                    for item in bosyuyoko:
                        for a in item:
                            final.append(a)

                    if len(bosyuyoko) * 2 < 30:
                        list_null = [""] * (30 - len(bosyuyoko) * 2)

                        final = final + list_null

                    for item2 in kaisyajyoho:
                        for b in item2:
                            final.append(b)
                    Item = pd.DataFrame([final])

                    Item.to_csv(r"C:\\Users\Ray94\Desktop\2007.csv", mode='a', index=False, header=None,
                                encoding="utf-8_sig")
                    time.sleep(10)
                except Exception as e:
                    Error = pd.DataFrame([[url_2, url_3, str(e)]])
                    Error.to_csv(r"C:\\Users\Ray94\Desktop\error.csv", mode='a', index=False, header=None,
                                 encoding="utf-8_sig")
                    pass


