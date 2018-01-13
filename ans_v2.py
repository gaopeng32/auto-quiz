# Written by Peng Gao (gaopeng32@gmail.com) in Jan 2018

import os
import sys
import time
import screen_analysis as sa
import search_result as sr



def main():
    # Record starttime
    start = time.time()
   
    # Parse question and options
    question_raw, options_raw = sa.get_raw_text_from_screen();
    question, options, is_neg = sa.parse_question_option(question_raw, options_raw)
    print("question: ", question)
    print("options: ", options)
    print("negative: ", is_neg)

    # Search results
    result_list = sr.search(question)
    print(result_list)

    # Find the best option match
    best_option = sr.get_best_option(result_list, options, question, is_neg)
    if best_option is None:
        print('No answer')
    else:
        print('Best answer is: \033[1;31m{}\033[0m'.format(best_option))

    # Record endtime
    end = time.time()
    print("Total running time: %.02fms" % ((end-start)*1000))

 

if __name__ == "__main__":
    main()

