#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kaivalya mannam
"""

import glob
from collections import Counter
from preprocess_helper import readTextFile, readAnnFile, readEntities, readRelations, fill_in
from preprocess_helper import makeSentences, isNumber

# unify

def main():
    unify("data_new_0622/train", "data_new_1122/train.txt")
    unify("data_new_0622/dev", "data_new_1122/dev.txt")
    unify("data_new_0622/test", "data_new_1122/test.txt")

# Merges data in txt and ann files to provide labels for words

def unify(folder, t_filename):

    text_files = glob.glob(folder + "/*.txt")
    # 获取路径内所有文件名
    t_output = open(t_filename, "w")    

    orig_tok_counter = Counter()
    orig_rel_counter = Counter()
    new_tok_counter = Counter()
    sent_len_counter = Counter()

    for i in range(0, len(text_files)):

        #print("Processing file -"+text_files[i])

        ann_file = text_files[i].replace(".txt", ".ann")

        # read the txt file
        text_info = readTextFile(text_files[i])

        # get the annotated lines from the file
        t_lines, t_stats, r_lines, r_stats = readAnnFile(ann_file)

        orig_tok_counter.update(t_stats)
        orig_rel_counter.update(r_stats)

        # read the ann file and update text_info
        text_info, entity_dict, entity_dict_with_linenumber = readEntities(t_lines, text_info)
        # 当当前实体横跨多行文本时，需要对该实体进行正确的标注
        text_info, relation_dict, relation_dict_with_line = readRelations(entity_dict, r_lines, text_info)
        # r =[['R118','Reason-Drug', 'Arg1:T154','Arg2:T143']]

        # convert text_info to sentences
        sentences = makeSentences(
            text_info, new_tok_counter, sent_len_counter, entity_dict_with_linenumber, relation_dict)

        sentences = fill_in(sentences, entity_dict)
        # write tokens
        writeSeqFile(sentences, t_output, text_files[i])
       
    t_output.close()
    #print(relation_dict)
    print("Original Statistics:\n\tTokens:\n")
    print(orig_tok_counter)
    print("\tRels:\n")
    print(orig_rel_counter)
    print("New Statistics:\n\tTokens:")
    print(new_tok_counter)
  
    #print("Sentence Lengths:\n")
    #print(sent_len_counter.most_common(50))

def writeSeqFile(sentences, output_file, text_file):

    # for each sentence
    for sent in sentences:
        if sent['relation_label'][0] != 'delete' and sent['targets'][0][0] != 'I':
        # write a line for each word
            output_file.write('#' + text_file + '\n')
            for i in range(0, len(sent['words'])):

                # get the word and check if its a number
                word = sent['words'][i]
                origword = word
                numeric, newword = isNumber(word)
                if numeric:
                    word = newword
                # write the line
                # if str(sent['word_index'][i]) == '0':
                #     output_file.write('#\n')

                # output_file.write(" ".join([text_file, str(i), sent['line_num'][i], sent['word_index'][i], sent['seq'][i], sent['starts'][i], str(
                #     int(sent['starts'][i]) + len(origword)), origword, word, sent['targets'][i], \
                #                             str(sent['relation_label'][i]), str(sent['object_label'][i])]))

                output_file.write("\t".join(
                    [str(i), origword, sent['targets'][i], str(sent['relation_label'][i]), str(sent['object_label'][i])]))
                output_file.write('\n')


            

if __name__ == "__main__":
    main()
    #r = ['R116','Reason-Drug','Arg1:T152','Arg2:T143']