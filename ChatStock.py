import simuse
import time
import pickle
import os

from ChatClass import pickle_dump


def create_word_stock(word_tock_tuple_list:list[tuple],filename:str):
    point_index = filename.rfind('.')
    if point_index!=-1:
        filename = filename[:point_index]
    filename = filename + '.cl'
    question_count = 0
    answer_count = 0
    cl_dict = {}
    for a_tuple in word_tock_tuple_list:
        question_text = a_tuple[0]
        answer_text = a_tuple[1]
        question_key = str([{'type':'Plain','text':question_text}])
        answer_value = str([{'type':'Plain','text':answer_text}])
        if not(question_key in cl_dict.keys()):
            question_count += 1
            cl_dict[question_key] = {
                'time': int(time.time()),
                'answer': [],
                'freq': 9999,
                'regular':False
            }
        question_dict = cl_dict[question_key]
        answerlist = question_dict['answer']
        for answerdict in answerlist:
            if answerdict["answertext"] == answer_value:
                answerdict['same'] += 1
                break
        else:
            answerdict = {
                        'answertext': answer_value,
                        'time': int(time.time()),
                        'same': 1
                    }
            answerlist.append(answerdict)
            answer_count += 1

    if question_count+answer_count == 0:
        return None

    pickle_dump(cl_dict, open('WordStock/' + filename, 'wb'))
    return (question_count,answer_count,f'WordStock/{filename}')



def load_word_stock(filename):
    if not(os.path.exists(filename)):
        return None
    with open(filename,'r',encoding='utf-8') as file:
        word_stock = file.readlines()

    word_stock_tuple_list = []
    
    for line in word_stock:
        word_stock_tuple = line.split('\t',1)
        if len(word_stock_tuple)!=2:
            continue
        word_stock_tuple_list.append(word_stock_tuple)
    return word_stock_tuple_list
