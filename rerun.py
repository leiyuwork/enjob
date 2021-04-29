import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://employment.en-japan.com/search/issue_index_2010/',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'S13U20=6GEz7MhrYH; LPID=--; FPDT=20210427213616; FPID=--; FPREF=https%253A%252F%252Fwww.google.com%252F; S13URECENTWORKID=1070534%7C1075944%7C1076691%7C1072135; PHPSESSID=d1khgulkiuha1k3qrmlme84ms7; S13U35=1; not_display_ie7_8_alert_text=1; not_display_ie7_8_alert_modal=1; _kys=QEkRHYPk8RFAIA_.en-japan.com; LPREF=; E13CC=077e7191d3574d36851ef5d633822069; LPDT=20210428230812; TAGKNIGHT_CONTROL_CLUSTER=132; __hd_ss=1619618892540; AWSALB=he+zuGup1HnT+ZLsJniCkOMid+t/Un39IIvcIMiUjocUDve+FN3cYV637yqXOrf07FsNA0+3Uws9HryNDM7NQNYPPhgU1icyjjIth4I5VqRWmXmIhCBQPf9o3LzF; AWSALBCORS=he+zuGup1HnT+ZLsJniCkOMid+t/Un39IIvcIMiUjocUDve+FN3cYV637yqXOrf07FsNA0+3Uws9HryNDM7NQNYPPhgU1icyjjIth4I5VqRWmXmIhCBQPf9o3LzF; _kyp=QEkQBhnOpiHVppTw09kEA22fRapXoYJcPkGLFNmoGnKW8jGeQURglw+QYvFMbQjVelce4UboScIwZ4iSKA_.en-japan.com+eh+employment.en-japan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36',
}

url_2 = "https://employment.en-japan.com/search/issue_list_1158/"
print(url_2)
response_2 = requests.get(url_2, headers=headers)  # open everyday link
bs_obj_2 = BeautifulSoup(response_2.text, 'lxml')  # parse with beautifulsoup
date = bs_obj_2.find("em", class_="date").text


final = []


job_links = ['/desc_92026/', '/desc_91871/', '/desc_91769/',
            '/desc_92629/', '/desc_92004/', '/desc_92597/', '/desc_91665/', '/desc_92559/', '/desc_91917/',
            '/desc_91870/', '/desc_91788/', '/desc_92215/', '/desc_92378/', '/desc_92303/', '/desc_92044/',
            '/desc_90463/', '/desc_92473/', '/desc_91618/', '/desc_89567/', '/desc_92198/', '/desc_91785/',
            '/desc_92453/', '/desc_92347/', '/desc_91826/', '/desc_91625/', '/desc_91579/', '/desc_92156/',
            '/desc_92263/', '/desc_92247/', '/desc_92483/', '/desc_91792/', '/desc_91691/', '/desc_92415/',
            '/desc_92446/', '/desc_91789/', '/desc_92315/', '/desc_91069/', '/desc_92519/', '/desc_92178/',
            '/desc_91344/', '/desc_92204/', '/desc_92218/', '/desc_92380/', '/desc_92613/', '/desc_92427/',
            '/desc_92032/', '/desc_92487/', '/desc_92192/', '/desc_92649/', '/desc_92253/', '/desc_89553/',
            '/desc_92138/', '/desc_91729/', '/desc_92217/', '/desc_92104/', '/desc_90703/', '/desc_88220/',
            '/desc_91992/', '/desc_92254/', '/desc_92556/', '/desc_90235/', '/desc_92627/', '/desc_92206/',
            '/desc_92041/', '/desc_92354/', '/desc_90509/', '/desc_92288/', '/desc_92291/', '/desc_90998/',
            '/desc_92257/', '/desc_92458/', '/desc_92142/', '/desc_92086/', '/desc_91712/', '/desc_92304/',
            '/desc_91976/', '/desc_92409/', '/desc_92057/', '/desc_92134/', '/desc_92423/', '/desc_92363/',
            '/desc_92522/']


for job_link in job_links:
    url_3 = "https://employment.en-japan.com" + job_link
    print(url_3)

    try:
        response_3 = requests.get(url_3, headers=headers)  # open everyday link
        # print(response_2)
        bs_obj_3 = BeautifulSoup(response_3.text, 'lxml')  # parse with beautifulsoup
        # print(bs_obj_2)
        # time.sleep(3)

        industry = bs_obj_3.find_all("div", class_="searchListUnit searchListUnitJobChain")[2].find("li", class_="job").text
        company_name = bs_obj_3.find("span", class_="companyName").text
        job_name = bs_obj_3.find("div", class_="nameSet").find("span", class_="name").text
        catchphrase = bs_obj_3.find("div", class_="copyArea").text

        final.append(url_2)
        final.append(url_3)
        final.append(date)
        final.append(industry)
        final.append(company_name)
        final.append(job_name)
        final.append(catchphrase)

        tb = pd.read_html(url_3)[1]
        tb_2 = pd.read_html(url_3)[2]
        bosyuyoko = tb.values.tolist()
        kaisyajyoho = tb_2.values.tolist()


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

        Item.to_csv(r"C:\\Users\Ray94\Desktop\000.csv", mode='a', index=False, header=None,
                    encoding="utf-8_sig")
        time.sleep(10)
    except Exception as e:
        Error = pd.DataFrame([[url_2, url_3, str(e)]])
        Error.to_csv(r"C:\\Users\Ray94\Desktop\error.csv", mode='a', index=False, header=None,
                     encoding="utf-8_sig")
        pass

