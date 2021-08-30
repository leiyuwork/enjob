# -- coding: utf-8 --
import os
import pandas as pd
import openpyxl
import itertools
from datetime import datetime, timedelta
from operator import itemgetter

# import file
path = r"C:\Users\Ray94\OneDrive\Research\PHD\Research\20210428-202108_enjapan\tougo\in\\"
files = os.listdir(path)
for file in files:
    print(file)
    # read excel, drop all the nan row and column
    df = pd.read_excel(path + file, header=None, index_col=None)
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # turn all the cases into a big list
    df_list = df.values.tolist()


    # identify info by search item and get next cell, for example: search"会社名", get next cell"大和証券" by index + 1, if no info exists, return "NULL"

    def add_result(search_item):
        if search_item in every:
            try:
                message = every[every.index(search_item) + 1]
            except:
                message = 'NULL'
        else:
            message = 'NULL'
        result.append(message)


    # prepare a box for final
    unique = []

    # for each element(case) in the big list
    for case in df_list:

        # drop nan cells
        cleanedList = [x for x in case if str(x) != 'nan']

        # there are chances that date is in integer form, convert them into right date form
        try:
            cleanedList = [
                str((datetime(1900, 1, 1) + timedelta(x)).strftime("%Y-%m-%d")) if type(x) == int or type(x) == float else x
                for x in
                cleanedList]
        except:
            pass

        # some multi cases are in one list/row (this is due to a former bug in the data collection step)
        if sum("https://employment.en-japan.com/desc_" in str(s) for s in cleanedList) > 1:
            splitted = []

            # split them by specific pattern 'https://employment.en-japan.com/search/'
            for item in cleanedList:
                try:
                    if 'https://employment.en-japan.com/search/' in item:
                        splitted.append([])
                    splitted[-1].append(item)
                except:
                    pass

            # now for each separate case
            for each in splitted:
                # print(each)
                unique.append(each)
        else:
            # print(cleanedList)
            unique.append(cleanedList)

    unique.sort()
    unique = list(final for final, _ in itertools.groupby(unique))

    final = []
    for every in unique:

        result = []
        for data in every[0:7]:
            #print(every[1])
            result.append(data)
        add_result("仕事内容")
        add_result("応募資格")
        add_result("募集背景")
        add_result("雇用形態")
        add_result("勤務地・交通")
        add_result("勤務時間")
        add_result("給与")
        add_result("休日休暇")
        add_result("福利厚生・待遇")
        add_result("配属部署・教育制度")
        add_result("配属部署")
        add_result("教育制度")
        add_result("会社名")
        add_result("設立")
        add_result("創業")
        add_result("代表者")
        add_result("資本金")
        add_result("売上高")
        add_result("従業員数")
        add_result("事業内容")
        add_result("事業所")
        add_result("関連会社")
        add_result("主要取引先")
        add_result("企業ホームページ")

        add_2 = [x for x in every if x not in result]
        for index in ['仕事内容', '応募資格', '募集背景', '雇用形態', '勤務地・交通', '勤務時間', '給与', '休日休暇', '福利厚生・待遇', "配属部署・教育制度",
                      '配属部署', "教育制度", '会社名', '設立', "創業", '代表者', '資本金', "売上高", '従業員数', '事業内容', '事業所', "関連会社", '主要取引先',
                      '企業ホームページ']:
            try:
                add_2.remove(index)
            except:
                pass
        for add in add_2:
            result.append(add)
        final.append(result)

    sorted(final, key=itemgetter(1))
    # print(final)
    Item = pd.DataFrame(final)
    Item.to_csv(r"C:\Users\Ray94\OneDrive\Research\PHD\Research\20210428-202108_enjapan\tougo\out\enjapan_final_20210830_1920.csv", mode="a",
                  index=False, header=None, encoding='utf_8_sig')
