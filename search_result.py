# Written by Peng Gao (gaopeng32@gmail.com) in Jan 2018

import webbrowser
import urllib.request
from bs4 import BeautifulSoup


def search_baidu(question):
    """Search Baidu and open the search results page
    """

    url = 'http://www.baidu.com/s?wd=%s' % question
    web = webbrowser.get("chrome") # need to specify brower code in Mac OS
    web.open(url)

def search(question):
    result_list = []
    result_list.extend(search_zhidao(question))
    return result_list

def search_zhidao(question):
    """Search Baidu Zhidao through web scraping. 
    Retrieve the top answers and calculate match scores
    """

    # Get html
    result_list = []
    num_results = 10 
    wd = urllib.request.quote(question)
    url = 'https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn={}&fr=wwwt&word={}'.format(num_results, wd)
    html = BeautifulSoup(urllib.request.urlopen(url).read(), 'html5lib')

    # Parse html
    best_match_div = html.find("div", class_="list-header").find("dd", class_="dd answer")
    if best_match_div is not None:
        best_match_result = best_match_div.get_text()
        # print("best",best_match_result)
        result_list.append(best_match_result)

    second_match_div = html.find("div", class_='list-inner').find("div", class_='list')
    if second_match_div is not None:
        second_match_block_list = second_match_div.findAll("dl")
        if second_match_block_list is not None and len(second_match_block_list) > 0:
            for second_match_block in second_match_block_list:
                second_match_result = second_match_block.find("dd", class_="dd answer").get_text()
                # print("second",second_match_result)
                result_list.append(second_match_result)
    return result_list


def get_best_option(result_list, options, question, is_neg):
    score_list = [0 for i in options]
    for result in result_list:
        for i, opt in enumerate(options):
            if opt in result:
                score_list[i] += 1

    if len(score_list) == 0 or max(score_list) == 0:
        return None
    best_score = min(score_list) if is_neg else max(score_list)
    best_optinon = options[score_list.index(best_score)]
    return best_optinon
