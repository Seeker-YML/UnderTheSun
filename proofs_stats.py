'''
A small test .py file for data preprocessing and data pipeline construction ... 
'''

import os 
import time 
import csv 
import json 
import pandas as pd 
from collections import Counter


def only_parse_statement(s):
    s = s.replace('(', ' ').replace(')', ' ')
    s = s.split() # add the number 2 to remove the radundant word ...
    length = len(s)
    s = s [2: length-1]
    return s

'''
For deeper understanding, I have to expand this function as more powerful one to acquire more statistics ...
'''
def all_words_with_frequency( src_dir, dst_dir, goal_tac_csv_file):
    with open( src_dir + goal_tac_csv_file) as csv_file:
        goal_tactic_pairs = pd.read_csv(csv_file)
        # how to obtain frequency of each word in all the goal statements ... 
        # first, obtain the word_set and word_list together  
        # second, count the frequency of each word (*** think about this part ... )
        all_sep_goal_list = []
        num = 0
        print ( "the number of goal_tactic pairs is {}".format( len(goal_tactic_pairs.iloc[:,0])) )
        for goal in goal_tactic_pairs.iloc[ :, 0]:
            sep_goal_list = only_parse_statement( goal )  # memoty usage ... 
            all_sep_goal_list.extend( sep_goal_list )
            sep_goal_set = set(sep_goal_list)
            sep_goal_set_2 = sep_goal_set
            if num == 0 :
                sep_goal_set_1 = sep_goal_set 
            sep_goal_set_1 = sep_goal_set_1 | sep_goal_set_2
            num = num + 1 
        
    # print ( sep_goal_set_1[0:10] )    # the set object can't be called by indexes ... 
    print ( " the number of all words exiting in the goal statements is {} ".format( len(sep_goal_set_1) ) )
    goal_word_dict = {}
    for goal_word in sep_goal_set_1:
        word_count = all_sep_goal_list.count(goal_word)  # the speed is still very slow ... 
        print ("word - {} appeared {} times in the whole dataset ... ".format(goal_word, word_count) )
        goal_word_dict[goal_word] = word_count
    with open(dst_dir + '/train_word_freq_id.json') as f:
        json.dump( goal_word_dict, f )

'''
more statistics and more efficient methods to acquire stats ... 
'''
def all_words_statistics( src_dir, dst_dir, goal_tac_csv_file ):
    with open( src_dir + goal_tac_csv_file) as csv_file:
        goal_tactic_pairs = pd.read_csv(csv_file)
        all_sep_goal_list = []
        num = 0
        print ( "the number of goal_tactic pairs is {}".format( len(goal_tactic_pairs.iloc[:,0])) )
        for goal in goal_tactic_pairs.iloc[ :, 0]:
            sep_goal_list = only_parse_statement( goal )  # memoty usage ... 
            all_sep_goal_list.extend( sep_goal_list )
            sep_goal_set = set(sep_goal_list)
            sep_goal_set_2 = sep_goal_set
            if num == 0 :
                sep_goal_set_1 = sep_goal_set 
            sep_goal_set_1 = sep_goal_set_1 | sep_goal_set_2
            num = num + 1 
    '''
    goal_word_dict = {}
    for goal_word in sep_goal_set_1:
        word_count = all_sep_goal_list.count(goal_word)  # the speed is still very slow ... 
        print ("word - {} appeared {} times in the whole dataset ... ".format(goal_word, word_count) )
        goal_word_dict[goal_word] = word_count
    '''

    # take care - the usage of collections.Counter(): https://pymotw.com/2/collections/counter.html 

    time_1 = time.time()
    goal_word_dict_counter = Counter(all_sep_goal_list)
    time_2 = time.time()
    interval = time_2 - time_1
    print ("Using the Counter to help will take {} s. ".format( interval ) )
    word_num = len( goal_word_dict_counter.items() )
    print ( "The number of goal word is {}".format(word_num) )
    time_1 = time.time()
    goal_word_dict_order = goal_word_dict_counter.most_common( word_num )
    # take care of the returned type of most_common() method ...; [ [x, x_num], [y, y_num], ... ]
    time_2 = time.time()
    interval = time_2 - time_1
    print ("getting the new order with get_most_common method will take {} s. ".format( interval ) )
    print (goal_word_dict_order)
    with open(dst_dir + '/test_word_freq_id_counter_order.json', 'w') as f:
        json.dump( goal_word_dict_order, f )



def main():
    src_dir = os.getcwd() + '/data/premise_selection/human/'
    dst_dir = os.getcwd() + '/data/premise_selection/human/'   
    # csv_files = ['train.csv', 'test.csv', 'valid.csv']
    all_words_statistics(src_dir, dst_dir, 'test.csv')   # the data in the train.csv file disappeared ...

    
if __name__ == '__main__':
    main()



