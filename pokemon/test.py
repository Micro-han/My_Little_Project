import requests
import bs4
import pandas as pd
import openpyxl
from openpyxl.drawing.image import Image


def get_url(url):
    res = requests.get(url)
    return res


def url_name_get_name(url_name_before):
    # uesless code
    url_name_after = ""
    for i in url_name_before:
        if i == " ":
            url_name_after = url_name_after + "-"
        elif ord('A') <= ord(i) <= ord('Z'):
            url_name_after = url_name_after + str(chr(ord(i) + ord('a') - ord('A')))
        else:
            url_name_after = url_name_after + str(i)
    return url_name_after


def download_icons(target_fixed):
    # download pokemon icons
    for i in range(0, 1045):
        icon_png_url = ""
        each = str(target_fixed[i])
        pos = each.find("data-src") + 10
        while each[pos] != "\"":
            icon_png_url = icon_png_url + each[pos]
            pos = pos + 1
        icon_png_html = requests.get(icon_png_url)
        print(icon_png_url)
        down_url = "D:/MyProjects/webcrawler/icons/" + str(i) + ".png"
        with open(down_url, "wb") as f:
            f.write(icon_png_html.content)


def find_data(res):
    # total
    # num    every 7 in one group
    # name
    # icon

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    content = soup.find(id="pokedex")
    target_total = content.find_all("td", class_="cell-total")
    target_num = content.find_all("td", class_="cell-num")
    target_name = content.find_all("td", class_="cell-name")
    target_icon = content.find_all("td", class_="cell-icon")
    target_fixed = content.find_all("td", class_="cell-fixed")

    url_list = []
    name_list = []
    no_list = []
    type_list = []
    total_list = []
    hp_list = []
    attack_list = []
    defense_list = []
    sp_atk_list = []
    sp_def_list = []
    speed_list = []
    pos = -1
    for i in range(0, 1045):
        name_list.append(target_name[i].text)
        type_list.append(target_icon[i].text)
        total_list.append(target_total[i].text)
        url_list.append("")

        pos = pos + 1
        no_list.append(target_num[pos].text)
        pos = pos + 1
        hp_list.append(target_num[pos].text)
        pos = pos + 1
        attack_list.append(target_num[pos].text)
        pos = pos + 1
        defense_list.append(target_num[pos].text)
        pos = pos + 1
        sp_atk_list.append(target_num[pos].text)
        pos = pos + 1
        sp_def_list.append(target_num[pos].text)
        pos = pos + 1
        speed_list.append(target_num[pos].text)

    print("#:", len(target_fixed))
    print("name:", len(target_name))
    print("type:", len(target_icon))
    print("total:", len(target_total))
    print("nums:", len(target_num))

    # download_icons(target_fixed)
    # csv
    # output_excel = {'NO': no_list, 'Name': name_list, 'type': type_list, 'total': total_list, 'HP': hp_list, 'Attack': attack_list, 'Defense': defense_list, 'Sp.Atk': sp_atk_list, 'Sp.Def': sp_def_list, 'Speed': speed_list}
    # output = pd.DataFrame(output_excel)
    # output.to_csv("result.csv", index=False, encoding="utf_8_sig")

    # excel
    output_excel = {'Icon': url_list, 'NO': no_list, 'Name': name_list, 'type': type_list, 'total': total_list, 'HP': hp_list,
                    'Attack': attack_list, 'Defense': defense_list, 'Sp.Atk': sp_atk_list, 'Sp.Def': sp_def_list,
                    'Speed': speed_list}
    output = pd.DataFrame(output_excel)
    output.to_excel("result.xlsx", index=False)
    # output icons to excel
    # icons are 56 * 42
    wb = openpyxl.load_workbook('result.xlsx')
    sh = wb['Sheet1']
    sh.column_dimensions["A"].width = 6.38
    for i in range(0, 1045):
        sh.row_dimensions[2 + i].height = 31.5
        img = Image("D:/MyProjects/webcrawler/icons/" + str(i) + ".png")
        sh.add_image(img, 'A' + str(i + 2))
        wb.save('result.xlsx')


def main():
    url = "https://pokemondb.net/pokedex/all"
    res = get_url(url)
    find_data(res)

    with open("res.txt", "w", encoding="utf-8") as file:
        file.write(res.text)


if __name__ == "__main__":
    main()