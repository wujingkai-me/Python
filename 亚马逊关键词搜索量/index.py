# -*- encoding: utf8 -*-
import requests
import const
import re
import csv
import console


def Analyze_HTML(url="", HEADER={}, params={}, timeout=15):
    if url == "" or HEADER == {}: return None
    try:
        result = requests.get(url=url, headers=HEADER, params=params, timeout=timeout)
        result.raise_for_status()
        return result
    except Exception as e:
        print(e)
        return None


def Number_of_actual_products(AfterAnaHTML):
    # 真实的HTML文本段
    actual_HTML = str(AfterAnaHTML)
    regular_expression = r"<span>1-.*?for</span>"
    s = re.search(regular_expression, actual_HTML, re.M)
    if s == None: return "0"
    else: return re.search(r"1-.*?for", s.group(0), re.M).group(0)


def replace_line(word):
    return word.replace("\n","")

def Read_keyword_for_dot_txt(path="./keyword.txt"):
    const.FILE = open(path, "r", encoding="utf-8")
    const.FILE_LINE = const.FILE.readlines()
    keyword_list = list()
    for line in const.FILE_LINE:
        keyword_list.append(replace_line(line))
    const.FILE.close()
    return keyword_list

if __name__ == "__main__":
    const.HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.5261 SLBChan/105",
        "Cookie": "session-id=261-0871107-7613113; i18n-prefs=GBP; ubid-acbuk=260-1846767-8815407; sp-cdn=\"L5Z9:CN\"; lc-acbuk=en_GB; session-id-time=2082787201l; session-token=\"1BaTc9VE4Ab8JYHWWShOALqyX6Flhnis++k0byCTi2yjJnzvUZVmBOjRJw1i53k82RxEYdi2p6MYzWZu7kZ2WbSv+drYzzCELYVnkboesgC8KKzh4NGPIsUptZ8XaojuIyvXu+hsM8cedxlwe7FldT585HpAR1Xtd/rIcX7k6OQy0sUbg6PrKaGLoLF9LzqXhX1FxeWbRK29dk41KSZ0sg==\""
    }
    const.URL = "https://www.amazon.co.uk/s"
    keyword_list = Read_keyword_for_dot_txt()
    Search_number = list()
    HTML_Error = list()
    for keyword in keyword_list:
        console.log("关键词{}正在搜寻中。。。".format(keyword))
        # 获得HTML的节点元素
        HTML = Analyze_HTML(const.URL, HEADER=const.HEADER, params={"k": keyword})
        # print(HTML.text, "result")
        # 获得HTML中的实际搜索量
        if HTML == None:
            HTML_Error.append(keyword)
            console.log("HTML节点元素获取失败")
            continue
        r = Number_of_actual_products(HTML.text)
        console.log("关键词正在写入文件")
        f = open("keyword_temp.txt", "a+", encoding="utf-8")
        f.write("{0}\t{1} \n".format(r, keyword))
        f.close()
        console.log("关键词({})写入文件结束".format(keyword))
        # with open("keyword.csv", "wb") as file:
        #     w = csv.writer(file)
        #     temp_list = [ "{0} {1}".format(r, keyword) ]
        #     print(temp_list.__class__)
        #     w.writerow( temp_list )
        #     file.close()
    
    with open("errorKeyword.txt", "a+") as f:
        for k in HTML_Error:
            f.write(k + "\n")
        f.close()
    