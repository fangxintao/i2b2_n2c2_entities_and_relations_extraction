#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kaivalya mannam
"""
import re
from bisect import bisect_right
from word2number import w2n

max_sentence_length = 100

def readTextFile(filename):

    # open the txt file with prescription data
    text_file = open(filename, 'rt')

    # an array of dicts - each dict contains information about the words for a particular line
    text_info = []

    index = 0  # position of character in txt file
    line = text_file.readline()

    # read txt file
    while line != '':

        line_dict = {"start": index, "end": index + len(line)}

        # get the array of words, and start indices, initial sequence labels, target labels for each word
        words_array, starts, normwords = getWordsArray(line, index)

        # default sequence label is NA and default target label is O
        sequence_labels = ['NA' for i in range(0, len(words_array))]
        target_labels = ['O' for i in range(0, len(words_array))]
        relation_labels = [[] for i in range(0, len(words_array))]
        object_labels = [[] for i in range(0, len(words_array))]

        # update the dictionary, and append it
        line_dict.update({'words': words_array, 'sequences': sequence_labels,
                          'targets': target_labels, 'starts': starts, 'normwords': normwords,\
                          'relation_label': relation_labels, 'object_label':object_labels})
        text_info.append(line_dict)

        # update the buffer
        index += len(line)
        line = text_file.readline()
        # readline是每次只读一行，并作为字符串返回
    text_file.close()

    return text_info

# gets annotated lines

def readAnnFile(filename):

    # open annotation file, and read the lines
    ann_file = open(filename, 'rt')
    inplines = ann_file.readlines()
    
    lines = []
    for line in inplines:
        # get rid of \n at the end of the line 
        if line[-1:]=='\n':
            line = line.strip()
        inpcomps = line.split('\t')  # 取的是T
        newcomps = []
        # inpcomps[0] is entity
        newcomps.append(inpcomps[0])
        if len(inpcomps)<2:
            print("problem skipping line {} in file {}".format(line, filename))
            continue
        # inpcomps[1] is metadata, split by space and append
        for comp in inpcomps[1].split(' '):
            newcomps.append(comp)
        if len(inpcomps)>2:
            # finally what is left is word string, split it using getWordsArray
            # this is so getWordsArray will work properly
            inpcomps[2] = inpcomps[2]+'\n'
            for comp in getWordsArray(inpcomps[2]):
                newcomps.append(comp)
        lines.append(newcomps)

    # convert each line to an array of words

    # extract the T and R lines
    t_lines = list(filter(lambda line: "T" in line[0], lines))
    r_lines = list(filter(lambda line: "R" in line[0], lines))

    # sort by start #
    t_lines = sorted(t_lines, key=lambda line: int(line[2]))

    t_stats = list(map(lambda tok: tok[1], t_lines))
    r_stats = list(map(lambda tok: tok[1], r_lines))

    return t_lines, t_stats, r_lines, r_stats

# use annotated lines to update sequences and entities in our dictionaries
# assumes input is T lines

def readEntities(lines, text_info):

    # obtain a list of the starting location of each line in the file
    start_indices = list(
        map(lambda line_dict: int(line_dict['start']), text_info))

    entity_dict = {}
    entity_dict_with_linenumber = {}
    relarion_dict = {}
    # read annotation file
    for line_array in lines:

        # if its not a blank line
        if (not(len(line_array) == 0)):

            [sequence, entity, start, end, word_array] = getAnnInfo(
                line_array)  # unpack information about the annotation
           # [rel_sequence, relation, rel_start, rel_end] = getRelInfo()

            # entity_dict[sequence]={'entity':entity, 'start': start, 'end':end, 'span': word_array}

            # finds which lines are spanned by the annotation
            line_start = bisect_right(start_indices, int(start)) - 1
            line_end = bisect_right(start_indices, int(end)) - 1
            extraLines = line_end - line_start
            entity_dict[sequence] = {'entity': entity, 'start': start, 'end': end, 'span': word_array,
                                     'line_start': line_start, 'line_end': line_end, 'extraLines': extraLines}
            entity_dict_with_linenumber[line_start] = {'entity': entity, 'start': start, 'end': end, 'span': word_array,
                                     'sequence': sequence, 'line_end': line_end, 'extraLines': extraLines}
            # how many extra lines the annotation spans (in the txt file)

            currentLine = 0  # current line being read (indexed at 0)

            # current line dictionary we're looking to find the words in our annotation
            my_dict = text_info[line_start]

            # the location (in dictionary) of the first word
            index = bisect_right(my_dict['starts'], int(start)) - 1
            # 第一个实体在该行的索引
            # loop through each word in the annotation
            i = 0
            while i < len(word_array):

                # found the word and it matches :)
                if my_dict['words'][index] == word_array[i]:

                    # update info accordingly
                    update_target = True
                    if my_dict['sequences'][index] != 'NA':
                        # if it exists, we give preference to ADE over Reason
                        existing = my_dict['targets'][index]
                        if existing in ['B-ADE', 'I-ADE'] and entity == 'Reason':
                            #print("Keeping ADE over Reason")
                            update_target = False
                        elif existing in ['B-Reason', 'I-Reason'] and entity == 'ADE':
                            #print("Prefering ADE over Reason")
                            update_target = True
                        elif existing in ['B-Drug'] and entity == 'ADE':
                            # the first word is a Drug as well as ADE
                            # so we will write this as a Drug for first token
                            # and keep the rest as ADE
                            #print("ADE overlaps with Drug, keeping subset for ADE")
                            update_target = False
                        elif existing in ['B-ADE', 'B-Form'] and entity == 'Drug':
                            # this is same as the previous case
                            # for form its like Insulin Pen where the Insulin part is Drug
                            # and Pen part is Form
                            # so we will write this as a Drug for first token
                            # and keep the rest as is
                            #print("... overlaps with Drug, keeping subset ...")
                            update_target = True
                        elif existing in ['B-Drug'] and entity == 'Form':
                            # skip this case and put the I- when we loop
                            #print("... overlap with Drug 2, keeping subset ...")
                            update_target = False
                        elif existing in ['B-Reason', 'I-Reason'] and entity == 'Drug':
                            # here reason ends with drug name
                            #print("... overlap of drug with Reason, keeping subset ...")
                            update_target = True
                        elif existing in ['I-Drug'] and entity == 'Strength':
                            # here strength overlaps with Drug ...
                            #print("... overlap of strength with Drug, keeping subset ...")
                            update_target = True
                        elif entity == existing[2:]:
                            # this is fine they are same
                            update_target = True
                        else:
                            print("Skipping duplicate:")
                            # print(entity_dict['sequence'])
                            print("\tExisting: " + my_dict['targets'][index])
                            print("\tNew: " + entity)
                    if update_target:
                        my_dict['sequences'][index] = sequence
                        if (i == 0):
                            my_dict['targets'][index] = "B-" + entity
                        else:
                            my_dict['targets'][index] = "I-" + entity

                # found the word, but its in a compound word :|
                elif word_array[i] in my_dict['words'][index]:
                # 当当前实体只能找到一部分的时候,说明另一部分在另一行中。
                    # here we don't do the update_target check for now.
                    # try modifying the dict because the word is hidden in a compound word
                    new_dict, index = modifyDict(my_dict, word_array[i], index)

                    # we found the word in the modified dict, so update it
                    text_info[line_start + currentLine] = new_dict

                    continue

                # didn't find the word :(
                else:

                    # try moving along the dictionary to see if we can find it
                    index += 1

                    # if we've moved along the dictionary too far, raise an error
                    if (index == len(my_dict['words'])):
                        # raise "Error! Couldn't find " + word_array[i] + " within" + '\n' + str(my_dict['words'])
                        print(
                            "Uh oh, couldn't update data structure for this annotation")
                        print(word_array)
                        break
                    continue

                 # if this word was the last in txt file line, and we know we have multiple lines in this annotation
                if (index == len(my_dict['words']) - 1) and (currentLine < extraLines):
                    # 当当前实体的末位置已经等于当前文本的末位置的时候
                    # move to the next line
                    while (currentLine < extraLines):
                        currentLine += 1
                        my_dict = text_info[line_start + currentLine]

                        # skip empty lines, and stop jumping past lines once we reach a non-blank line
                        if len(my_dict['words']) != 0:
                            break

                    # make index -1, so it becomes 0 after incrementing below
                    index = -1
                    # 是等于-1

                # move onto next word
                index += 1
                i += 1
    return text_info, entity_dict, entity_dict_with_linenumber

# converts the text_info data structure into sentences

def readRelations(entity_dict, rel_lines, text_info):
    # obtain a list of the starting location of each line in the file
    start_indices = list(
        map(lambda line_dict: int(line_dict['start']), text_info))

    relation_dict = {}
    relation_dict_with_line = {}
    # read annotation file
    for line_array in rel_lines:

        # if its not a blank line
        if (not (len(line_array) == 0)):

            # [sequence, entity, start, end, word_array] = getAnnInfo(
            #     line_array)  # unpack information about the annotation
            [rel_sequence, relation, rel_start, rel_end] = getRelInfo(line_array)

            rel_index_start = rel_start.split(':')[1]
            rel_index_end = rel_end.split(':')[1]

            relation_dict[rel_index_start] = {'relation': relation, 'rel_sequence': rel_sequence, 'rel_index_end': rel_index_end}
            # 例子：{'T2':{'entity':'x', 'rel_sequence': R1, 'rel_end': T3 }}
            entity = entity_dict[rel_index_start]['entity']
            word_array = entity_dict[rel_index_start]['span']
            start = entity_dict[rel_index_start]['start']
            end = entity_dict[rel_index_start]['end']

            entity_2 = entity_dict[rel_index_end]['entity']
            word_array_2 = entity_dict[rel_index_end]['span']
            start_2 = entity_dict[rel_index_end]['start']
            end_2 = entity_dict[rel_index_end]['end']


            # finds which lines are spanned by the annotation
            line_start = bisect_right(start_indices, int(start)) - 1
            line_end = bisect_right(start_indices, int(end)) - 1

            line_start_2 = bisect_right(start_indices, int(start_2)) - 1
            line_end_2 = bisect_right(start_indices, int(end_2)) - 1

            # how many extra lines the annotation spans (in the txt file)
            extraLines = line_end - line_start

            rel_extralines = line_start_2 - line_start
            #  额外再造一个字典，多一个键用来储存两个实体是否跨行了
            relation_dict_with_line[rel_index_start] = {'relation': relation, 'rel_sequence': rel_sequence,
                                              'rel_index_end': rel_index_end, 'rel_extralines': rel_extralines}

            currentLine = 0  # current line being read (indexed at 0)

            # current line dictionary we're looking to find the words in our annotation
            my_dict = text_info[line_start]

            # the location (in dictionary) of the first word
            index = bisect_right(my_dict['starts'], int(start)) - 1

            # loop through each word in the annotation
            i = 0
            while i < len(word_array):

                # found the word and it matches :)
                if my_dict['words'][index] == word_array[i]:
                # 在找头实体的位置
                    # update info accordingly
                    update_target = True
                    if my_dict['sequences'][index] != 'NA':
                        # if it exists, we give preference to ADE over Reason
                        existing = my_dict['targets'][index]
                        if existing in ['B-ADE', 'I-ADE'] and entity == 'Reason':
                            #print("Keeping ADE over Reason")
                            update_target = False
                        elif existing in ['B-Reason', 'I-Reason'] and entity == 'ADE':
                            #print("Prefering ADE over Reason")
                            update_target = True
                        elif existing in ['B-Drug'] and entity == 'ADE':
                            # the first word is a Drug as well as ADE
                            # so we will write this as a Drug for first token
                            # and keep the rest as ADE
                            #print("ADE overlaps with Drug, keeping subset for ADE")
                            update_target = False
                        elif existing in ['B-ADE', 'B-Form'] and entity == 'Drug':
                            # this is same as the previous case
                            # for form its like Insulin Pen where the Insulin part is Drug
                            # and Pen part is Form
                            # so we will write this as a Drug for first token
                            # and keep the rest as is
                            #print("... overlaps with Drug, keeping subset ...")
                            update_target = True
                        elif existing in ['B-Drug'] and entity == 'Form':
                            # skip this case and put the I- when we loop
                            #print("... overlap with Drug 2, keeping subset ...")
                            update_target = False
                        elif existing in ['B-Reason', 'I-Reason'] and entity == 'Drug':
                            # here reason ends with drug name
                            #print("... overlap of drug with Reason, keeping subset ...")
                            update_target = True
                        elif existing in ['I-Drug'] and entity == 'Strength':
                            # here strength overlaps with Drug ...
                            #print("... overlap of strength with Drug, keeping subset ...")
                            update_target = True
                        elif entity == existing[2:]:
                            # this is fine they are same
                            update_target = True
                        else:
                            print("Skipping duplicate:")
                            print("\tExisting: " + my_dict['targets'][index])
                            print("\tNew: " + entity)
                    if update_target:
                        if (i == len(word_array)-1):
                            # my_dict['targets'][index] = "B-" + entity
                            my_dict['relation_label'][index].append(relation)
                            my_dict['object_label'][index].append(entity_dict[rel_index_end]['span'][-1])
                            # 当读取到当前实体的末尾时，如果有关系，则在末尾单词的位置分别填充关系与对应的客体实体编号（即T11之类的）
                            # 填写对应客体的时候，是否应该填充单词位置的信息，比如说起始位置而不是单词
                        else:
                            pass

                # found the word, but its in a compound word :|
                elif word_array[i] in my_dict['words'][index]:

                    # here we don't do the update_target check for now.
                    # try modifying the dict because the word is hidden in a compound word
                    new_dict, index = modifyDict(my_dict, word_array[i], index)

                    # we found the word in the modified dict, so update it
                    text_info[line_start + currentLine] = new_dict

                    continue

                # didn't find the word :(
                else:

                    # try moving along the dictionary to see if we can find it
                    index += 1

                    # if we've moved along the dictionary too far, raise an error
                    if (index == len(my_dict['words'])):
                        # raise "Error! Couldn't find " + word_array[i] + " within" + '\n' + str(my_dict['words'])
                        print(
                            "Uh oh, couldn't update data structure for this annotation")
                        print(word_array)
                        break
                    continue

                # if this word was the last in txt file line, and we know we have multiple lines in this annotation
                if (index == len(my_dict['words']) - 1) and (currentLine < extraLines):

                    # move to the next line
                    while (currentLine < extraLines):
                        currentLine += 1
                        my_dict = text_info[line_start + currentLine]

                        # skip empty lines, and stop jumping past lines once we reach a non-blank line
                        if len(my_dict['words']) != 0:
                            break

                    # make index -1, so it becomes 0 after incrementing below
                    index = -1

                # move onto next word
                index += 1
                i += 1
                # print(line_start)
                # print(rel_start)
    return text_info, relation_dict, relation_dict_with_line



def makeSentences_internal(text_info, new_tok_counter, sent_len_counter, entity_dict, relation_dict, max_sent_len=100, paragraphMode=False):
    # 采用的策略是，首先有句号时，采用句号进行断句，否则的话，考虑当前句子中的头实体位置对应的尾实体位置是否超过了
    # 当前句子末尾的位置，如果是，则加上下一句，且如果句子长度整体超过了100，以当前行为分割进行断句
    sentence_length = 0  # length of current words
    sentences = []
    sentence = defaultSentence()
    extralines = 0
    rel_extralines = 0
    hint = ['Medications', 'on', 'Admission', ':']
    write_sentence = True
    line_mode = False
    for line_num, line_dict in enumerate(text_info):
        if line_dict['words'] == hint:
            line_mode = True
        if line_mode == True and len(line_dict['words']) == 0:
            line_mode = False
        if line_mode == True:
            if extralines > 0:
                extralines -= 1
            # if this line is empty
            if len(line_dict['words']) == 0 and write_sentence == True:
                # 当当前行存在实体跨行的情况的时候
                if len(line_dict['words']) == 0:
                    # append the old sentence
                    if sentence_length > 0:
                        sentences.append(sentence)
                        sent_len_counter.update([sentence_length])

                        # initialize a new sentence
                        sentence = defaultSentence()
                        sentence_length = 0
            if len(line_dict['words']) != len(line_dict['normwords']):
                assert False
            # 读取relation_dict里的所有的key，即是所有的实体的line_number(数字)
            # entity_dict_key = entity_dict.keys()
            #
            # if line_num in entity_dict_key:
            #     if entity_dict[line_num]['extraLines'] != 0:
            #         extralines = entity_dict[line_num]['extraLines']
            #         write_sentence = False
            # if extralines == 0:
            #     write_sentence = True
            for i in range(0, len(line_dict['words'])):

                sentence['seq'].append(line_dict['sequences'][i])
                sentence['words'].append(line_dict['words'][i])
                sentence['normwords'].append(line_dict['normwords'][i])
                sentence['starts'].append(str(line_dict['starts'][i]))
                sentence['line_num'].append(str(line_num + 1))
                sentence['word_index'].append(str(i))
                sentence['relation_label'].append(line_dict['relation_label'][i])
                sentence['object_label'].append(line_dict['object_label'][i])

                # append the right entity + secondary entity info
                entity = line_dict['targets'][i]
                sentence['targets'].append(entity)

                # increment sentence length and update counter
                sentence_length += 1
                new_tok_counter.update([entity])

                # add a break either when we reach a period or the sentence is too long
                if i == len(line_dict['words']) - 1:
                    if sentence_length > 0:
                        # append the old sentence

                        sentences.append(sentence)
                        sent_len_counter.update([sentence_length])

                        # initialize a new sentence
                        sentence = defaultSentence()
                        sentence_length = 0
                        # write_sentence = False

        else:
            if extralines > 0:
                extralines -= 1
            # if this line is empty
            if len(line_dict['words']) == 0 and write_sentence == True:
            # 当当前行存在实体跨行的情况的时候
                if len(line_dict['words']) == 0:
                    # append the old sentence
                    if sentence_length > 0:
                        sentences.append(sentence)
                        sent_len_counter.update([sentence_length])

                        # initialize a new sentence
                        sentence = defaultSentence()
                        sentence_length = 0
            if len(line_dict['words']) != len(line_dict['normwords']):
                assert False
            # 读取entity_dict里的所有的key，即是所有的实体的line_number(数字)
            entity_dict_key = entity_dict.keys()
            if line_num in entity_dict_key:
                if entity_dict[line_num]['extraLines'] != 0:
                    extralines = entity_dict[line_num]['extraLines']
                    write_sentence = False
            if extralines == 0:
                write_sentence = True
            for i in range(0, len(line_dict['words'])):


                sentence['seq'].append(line_dict['sequences'][i])
                sentence['words'].append(line_dict['words'][i])
                sentence['normwords'].append(line_dict['normwords'][i])
                sentence['starts'].append(str(line_dict['starts'][i]))
                sentence['line_num'].append(str(line_num + 1))
                sentence['word_index'].append(str(i))
                sentence['relation_label'].append(line_dict['relation_label'][i])
                sentence['object_label'].append(line_dict['object_label'][i])

                # append the right entity + secondary entity info
                entity = line_dict['targets'][i]
                sentence['targets'].append(entity)

                # increment sentence length and update counter
                sentence_length += 1
                new_tok_counter.update([entity])

                # add a break either when we reach a period or the sentence is too long
                if (paragraphMode == False and line_dict['words'][i] == "." and write_sentence == True) or (write_sentence == True and
                    sentence_length > max_sent_len):
                    if sentence_length > 0:
                        # append the old sentence

                        sentences.append(sentence)
                        sent_len_counter.update([sentence_length])

                        # initialize a new sentence
                        sentence = defaultSentence()
                        sentence_length = 0
                        # write_sentence = False

        # append the last remaining sentence if any
    if sentence_length > 0:
        # append the old sentence

        sentences.append(sentence)
        sent_len_counter.update([sentence_length])

    return sentences


def makeSentences(text_info, new_tok_counter, sent_len_counter, entity_dict, relation_dict):

    global max_sentence_length
    sentences = makeSentences_internal(text_info, new_tok_counter, sent_len_counter, entity_dict, relation_dict, max_sentence_length, False)
    return sentences

def makeSentences_for_predict(text_info, new_tok_counter, sent_len_counter):

    global max_sentence_length
    sentences = makeSentences_internal(text_info, new_tok_counter, sent_len_counter, max_sentence_length*3, False)
    return sentences

def makeSentences_paragraph(text_info, new_tok_counter, sent_len_counter):

    # in paragraph mode, there is no max_sentence_length, so we pass 0
    sentences = makeSentences_internal(text_info, new_tok_counter, sent_len_counter, 0, True)
    return sentences

# writes unified tokens to a file


# modifies the dictionary to find a missing word
# suppose we are looking for "anthracycline", but the words list is ["anthracycline-induced", "cardiomyopathy", ...]
# this function modifies the list of words to be ["anthracycline", "-induced", "cardiomyopathy", ...], taking in index of 0

def modifyDict(line_dict, target_word, index):

    # compound_word contianing the target word
    compound_word = line_dict['words'][index]

    # split the compound word once to isolate the word
    new_words = re.split("(" + re.escape(target_word) + ")", compound_word, 1)

    # remove blank entries
    new_words = [word for word in new_words if (word != '')]
    norm_new_words = [normWord(word) for word in new_words if (word != '')]
    rel_label = [[] for word in new_words if (word != '') ]
    object_label = [[] for word in new_words if (word != '')]
    # the would be location of the target word in line_dict['words']
    targetLocation = new_words.index(target_word) + index

    # modify the list of words to remove the compound word and insert the new words
    line_dict['words'] = line_dict['words'][0:index] + \
        new_words + line_dict['words'][index+1:]

    line_dict['normwords'] = line_dict['normwords'][0:index] + \
        norm_new_words + line_dict['normwords'][index+1:]
    line_dict['relation_label'] = line_dict['relation_label'][0:index] + \
        rel_label + line_dict['relation_label'][index+1:]
    line_dict['object_label'] = line_dict['object_label'][0:index] + \
                                  object_label + line_dict['object_label'][index + 1:]

    # start indices for the new words
    new_starts = []

    # start of the compound word in the old list
    start = line_dict['starts'][index]

    # creating new starts
    for word in new_words:
        new_starts.append(start)
        start += len(word)

    # add new entries to sequences, targets, and starts
    line_dict['sequences'] = line_dict['sequences'][0:index] + \
        ['NA' for i in range(0, len(new_words))] + \
        line_dict['sequences'][index+1:]
    line_dict['targets'] = line_dict['targets'][0:index] + \
        ['O' for i in range(0, len(new_words))] + \
        line_dict['targets'][index+1:]
    line_dict['starts'] = line_dict['starts'][0: index] + \
        new_starts + line_dict['starts'][index+1:]

    return line_dict, targetLocation


# returns an empty default sentence

def defaultSentence():

    sent = {}
    sent.update({'seq': [], 'words': [], 'starts': [], 'line_num': [],
                 'word_index': [], 'normwords': [], 'targets': [], 'relation_label': [], 'object_label': []})

    sent.update({'rels': [], 'relspan': set()})

    return sent

# unpack the information from the line

def getAnnInfo(line_array):

    [sequence, entity, start] = line_array[0:3]  # unpack

    endIndex = 3  # index of the end token (in line_array)

    # figure out endIndex
    while ';' in line_array[endIndex]:
        endIndex += 1

    # the ending character of the annotation
    end = line_array[endIndex]

    # the remaining tokens on the annotation line is treated as a list of words
    word_array = line_array[endIndex + 1:]

    return [sequence, entity, start, end, word_array]

# converts a line to an array of words
# if we want to get indices at which each word starts, pass a starting index

def getRelInfo(line_array):

    [rel_sequence, relation, rel_start , rel_end] = line_array[0:4]  # unpack

    endIndex = 3  # index of the end token (in line_array)

    # figure out endIndex
    # while ';' in line_array[endIndex]:
    #     endIndex += 1
    #
    # # the ending character of the annotation
    # end = line_array[endIndex]
    #
    # # the remaining tokens on the annotation line is treated as a list of words
    # word_array = line_array[endIndex + 1:]

    return [rel_sequence, relation, rel_start , rel_end]

def getWordsArray(line, start=None):

    # replace \n at the end of the line with a space
    if line[-1:]=='\n':
        line = line[:-1] + " "

    # split the line into words (keeping punctuation)
    # for %, *, :, (, ), \,, and ; we can split no matter where they occur
    # for - and . we will split on word space boundaries
    # numeric is handled below
    words_array = re.split('(\s+|[\%\*\:\(\)\,\;]|[\-\.]\s+|[\-]+|[\#]+)', line) # 
        
    # if we want to get starting indices also
    if start != None:
        
        starts = []
        normwords = []
        
        # loop through the array, noting down start values
        for word in words_array:
            starts.append(start)
            start += len(word)
            #if len(word)==0:
            #    print("check")
            numeric, newword = isNumber(word)
            if numeric:
                normwords.append(newword)
            else:
                normwords.append(word)

        # remove blank elements, while also removing start indices that correspond to those elements
        try:
            words_array, starts, normwords = zip(
                *filter(lambda tuple: tuple[0].strip() not in '', zip(words_array, starts, normwords)))

        # filter receives an error when all entries are removed
        except:
            words_array, starts, normwords = ([], [], [])

        # remove extra whitespace from each element
        words_array = list(map(lambda x: x.strip(), words_array))
        normwords = list(map(lambda x: x.strip(), normwords))

        assert len(words_array)==len(starts)
        assert len(words_array)==len(normwords)
        return list(words_array), list(starts), list(normwords)

    # we just want the array
    else:

        # remove extra whitespace from each element
        words_array = list(map(lambda x: x.strip(), words_array))

        # remove blank elements
        words_array = [word for word in words_array if (
            word.strip() not in '')]

        return words_array

# returns true if the word contains a numerical digit or is a word number like "six"

def isNumber(word): #, old_method = False):
    
    # if it contains numerical values
    if not set('0123456789').isdisjoint(word):
        try:
            val = int(word)
            return True, "ORDINAL" # fully a number
        except:
            newword = []
            for i in word:
                # not a number or first token
                if set('0123456789').isdisjoint(i):
                    newword.append(i)
                elif len(newword)==0 or newword[len(newword)-1] != '0':
                    # first token or previous token is not a number
                    newword.append('0')
                # else skip this as we have already written the number
            return True, "".join(newword)
    else:
        # try converting the word to a number
        try:
            val = w2n.word_to_num(word)
        except:
            return False, word
        return True, "ORDINAL"

def normWord(word):
    num, newword = isNumber(word)
    if num:
        return newword
    else:
        return word
def fill_in(sentences, entity_dict):
    count_delete = 0
    for sent in range(0, len(sentences)):
        na = 0
        relation_should_be_delete = 0
        # find = 0 设置一个常数，当客体在文本中没找到时，说明句子分割有错误，将该句删除
        all_word_idx = {}
        for k in range(0, len(sentences[sent]['words'])):
            all_word_idx.update({sentences[sent]['words'][k]: k})
            if not sentences[sent]['relation_label'][k]:
                sentences[sent]['relation_label'][k].append('N')
            if sentences[sent]['relation_label'][k][0] != 'N':
                na = 1
        for s in range(0, len(sentences[sent]['words'])):
            if sentences[sent]['object_label'][s]:
                l = 0
                while l < len(sentences[sent]['object_label'][s]):
                    if sentences[sent]['object_label'][s][l] in all_word_idx.keys():
                        sentences[sent]['object_label'][s][l] = all_word_idx[sentences[sent]['object_label'][s][l]]
                    else:
                        relation_should_be_delete = 1
                        break
                        # 权宜之计：暂时将所有没有变成object号的句子删去
                    l += 1
            elif not sentences[sent]['object_label'][s]:
                sentences[sent]['object_label'][s].append(s)

        if na == 0 or relation_should_be_delete == 1:
            for r in range(0, len(sentences[sent]['words'])):
                sentences[sent]['relation_label'][r] = 'delete'
    return sentences
