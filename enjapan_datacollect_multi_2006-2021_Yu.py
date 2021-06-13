import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import PySimpleGUI as sg
import os
import warnings

warnings.filterwarnings("ignore")

sg.theme('DarkAmber')
Sheets = range(2006, 2022)

layout = [[sg.Text('【説明】\n'
                   '本プログラムはエン・ジャパン求人一覧データの【追加分】を取得するために作られたものです。\n')],
          [sg.Text('【作業手順】\n'
                   '①Browseをクリックして、出力フォルダーを指定する')],
          [sg.Text('出力フォルダー:'), sg.Input(), sg.FolderBrowse()],
          [sg.Text('②取得したいデータ期間を指定する')],
          [sg.Listbox(Sheets, key='-Sheet_list-', size=(20, 10))],
          [sg.Text('③【作業開始】ボタンを押してください。\n')],
          [sg.Button('作業開始'), sg.Button('キャンセル')],
          [sg.Text('④処理が自動的に始まります。全ての処理が終わりましたら、この作業Windowが自動的に消えます。\n\n'
                   '【成果物】\n'
                   '処理が始まると①year_multi_data.csv(求人データ) ②year_multi_log.csv(作業ログ)が作成されます。(例：2016_multi_data.csv)\n'
                   'データ取得エラーが発生する場合、③year_multi_error.csvに記録されますが、処理自体が継続します。\n\n'
                   '【注意事項】\n'
                   '処理中は作業Windowを動かさないでください。pythonがフリーズする可能性があります。\n'
                   '処理中は成果物のexcelを開かないでください。\n')],
          [sg.Output(size=(60, 5))],
          [sg.Text('© 2021 Yu,lei programmed for Karube-enjapan project.')], ]

# 创造窗口
window = sg.Window('enjapan project data generator(Yu Lei)　v2.0', layout)
# 事件循环并获取输入值
while True:
    event, values = window.read()
    if event in (None, 'キャンセル'):  # 如果用户关闭窗口或点击`Cancel`
        break
    print('出力フォルダーは ', values[0])
    path_out = values[0]
    year = values["-Sheet_list-"][0]

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
    url_1 = "https://employment.en-japan.com/search/issue_index_" + str(year) + "/"  # link of every year
    print(url_1)

    response_1 = requests.get(url_1, headers=headers)  # get url contents
    bs_obj_1 = BeautifulSoup(response_1.text, 'lxml')  # parse with beautifulsoup
    table_td_1 = bs_obj_1.find_all("td", class_="data")  # get the link tables

    for link in table_td_1:
        url_2 = "https://employment.en-japan.com" + link.find('a', href=True).attrs['href']
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
                job_information = results.find_all('a', href=True)
                # print(job_information)
                if len(job_information) > 1:
                    for job_detail in job_information[1:]:
                        # print(job_detail)
                        job_name = job_detail.text
                        job_link = job_detail.attrs['href']
                        #print(job_name)
                        #print(job_link)

                        url_3 = "https://employment.en-japan.com" + job_link
                        print('処理中:' + url_3)
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

                            Item.to_csv(path_out + '\\' + str(year) + "_multi_data.csv", mode='a', index=False, header=None,
                                        encoding="utf-8_sig")
                            time.sleep(10)

                            log = pd.DataFrame([[url_1, url_2, url_3]])

                            log.to_csv(path_out + '\\' + str(year) + "_multi_log.csv", mode='a', index=False, header=None,
                                       encoding="utf-8_sig")
                        except Exception as e:
                            Error = pd.DataFrame([[url_2, url_3, str(e)]])
                            Error.to_csv(path_out + '\\' + str(year) + "_multi_error.csv", mode='a', index=False, header=None,
                                         encoding="utf-8_sig")
                            pass
window.close()
