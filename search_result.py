import webbrowser
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup


def search_baidu(question):
    url = 'http://www.baidu.com/s?wd=%s' % question
    web = webbrowser.get("chrome") # need to specify brower code in Mac OS
    web.open(url)

def search(question):
    result_list = []
    result_list.extend(search_zhidao(question))
    return result_list

def search_zhidao(question):
    result_list = []
    wd = urllib.request.quote(question)
    url = 'https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn={}&fr=wwwt&word={}'.format(20,
        wd)
    result = urlopen(url)
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    second_result_div = body.find(class_='list-inner').find(class_='list')
    if good_result_div is not None:
        good_result = good_result_div.get_text()
        result_list.append(good_result)

    if second_result_div is not None:
        second_result_10 = second_result_div.findAll('dl')  # .find(class_='answer').get_text()
        if second_result_10 is not None and len(second_result_10) > 0:
            for index, each_result in enumerate(second_result_10):
                result_dd = each_result.dd.get_text()
                result_list.append(result_dd)
    return result_list

def get_best_option(result_list, options, question, is_neg):
    score_arr = [0 for i in options]
    for result in result_list:
        for i, opt in enumerate(options):
            if opt in result:
                score_arr[i] += 10

    if len(score_arr) == 0 or max(score_arr) == 0:
        return None
    best_score = min(score_arr) if is_neg else max(score_arr)
    best_optinon = options[score_arr.index(best_score)]
    return best_optinon
