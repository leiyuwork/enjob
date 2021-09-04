import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import PySimpleGUI as sg
import os
import warnings

warnings.filterwarnings("ignore")

sg.theme('DarkAmber')

layout = [[sg.Text('【説明】\n'
                   '本プログラムはエン・ジャパン求人一覧データの【追加分】を取得するために作られたものです。\n')],
          [sg.Text('【作業手順】\n'
                   '①Browseをクリックして、出力フォルダーを指定する')],
          [sg.Text('Input file:'), sg.Input(), sg.FileBrowse()],
          [sg.Text('出力フォルダー:'), sg.Input(), sg.FolderBrowse()],
          [sg.Text('②【作業開始】ボタンを押してください。\n')],
          [sg.Button('作業開始'), sg.Button('キャンセル')],
          [sg.Text('③処理が自動的に始まります。全ての処理が終わりましたら、この作業Windowが自動的に消えます。\n\n'
                   '【成果物】\n'
                   '処理が始まると①enjapan_bug_fix_data.csv(求人データ) ②enjapan_bug_fix_log.csv(作業ログ)が作成されます。\n'
                   'データ取得エラーが発生する場合、③enjapan_bug_fix_error.csvに記録されますが、処理自体が継続します。\n\n'
                   '【注意事項】\n'
                   '処理中は作業Windowを動かさないでください。pythonがフリーズする可能性があります。\n'
                   '処理中は成果物のexcelを開かないでください。\n')],
          [sg.Output(size=(60, 5))],
          [sg.Text('© 2021 Yu,lei programmed for Karube-enjapan project.')], ]

# 创造窗口
window = sg.Window('enjapan project bug fix data generator(Yu Lei)　v1.0', layout)
# 事件循环并获取输入值
while True:
    event, values = window.read()
    if event in (None, 'キャンセル'):  # 如果用户关闭窗口或点击`Cancel`
        break
    print('Input fileは ', values[0])
    print('出力フォルダーは ', values[1])
    path_out = values[1]

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

    bug = pd.read_excel(values[0], index_col=False, header=None)
    urllist = bug[2].tolist()
    for url_3 in urllist:
        final = []
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
            final.append(url_3)
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

            Item.to_csv(path_out + '\\' + "enjapan_bug_fix_data.csv", mode='a', index=False, header=None,
                        encoding="utf-8_sig")
            time.sleep(8)

            log = pd.DataFrame([[url_3]])

            log.to_csv(path_out + '\\' + "enjapan_bug_fix_log.csv", mode='a', index=False, header=None,
                       encoding="utf-8_sig")
        except Exception as e:
            Error = pd.DataFrame([[url_3, str(e)]])
            Error.to_csv(path_out + '\\' + "enjapan_bug_fix_error.csv", mode='a', index=False, header=None,
                         encoding="utf-8_sig")
            pass