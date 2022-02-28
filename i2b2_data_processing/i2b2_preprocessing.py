import glob
import os
import re
from typing import *
import pandas as pd
from tqdm import tqdm
from ast import literal_eval

# relation_data_path = 'concept_assertion_relation_training_data/beth/rel'
in_exp = 'in_exp'
out_exp = 'raw_data/in_out_exp'
train_inpath = 'i2b2_256_85_85_cased_reassign'
train_outpath = 'raw_data/i2b2_256_85_85_cased_reassign'
dev_inpath = 'i2b2_256_85_85_cased_reassign'
dev_outpath = 'raw_data/i2b2_256_85_85_cased_reassign'
test_inpath = 'i2b2_256_85_85_cased_reassign'
test_outpath = 'raw_data/i2b2_256_85_85_cased_reassign'
#in_path = 'i2b2data_divide'
SENTENCE_LENGTH = 1
N = 0
out_path = 'out_data'
relation_dict = {0: 'TrIP', 1: 'TrWP', 2: 'TrCP', 3: 'TrAP', 4: 'TrNAP', 5: 'TeRP', 6: 'TeCP', 7: 'PIP', 8: 'None'}

train_sent_Dict = {}
train_sentLabels_Dict = {}

# The test dict contain the sentences and the corresponding labels used in evaluation of the model
test_sent_Dict = {}
test_sentLabels_Dict = {}

dev_sent_Dict = {}
dev_sentLabels_Dict = {}
docNum = 0

if not os.path.exists(train_outpath):
    os.makedirs(train_outpath)
if not os.path.exists(dev_outpath):
    os.makedirs(dev_outpath)
if not os.path.exists(test_outpath):
    os.makedirs(test_outpath)
# relation_dict = {0: 'TrIP', 1: 'TrWP', 2: 'TrCP', 3: 'TrAP', 4: 'TrNAP', 5: 'TeRP', 6: 'TeCP', 7: 'PIP', 8: 'None'}
# rev_relation_dict = {'TrIP': 0, 'TrWP': 1, 'TrCP': 2, 'TrAP': 3, 'TrNAP': 4, 'TeRP': 5, 'TeCP': 6, 'PIP': 7,
#                     'TrP-None': 8, 'TeP-None': 8, 'PP-None': 8}


# rev_relation_dict = {val: key for key, val in relation_dict.items()}

# given a file path, just get the name of the file
def get_filename_with_extension(path):
    return os.path.basename(path)


# given the file name with an extension like filename.con, return the filename
# without the extension i.e. filename
def get_filename_without_extension(path):
    filename_with_extension = os.path.basename(path)
    return os.path.splitext(filename_with_extension)[0]


# given a string that looks like c="concept" extract the concept
def extract_concept_from_string(fullstring):
    return re.match(r'^c=\"(?P<concept>.*)\"$', fullstring).group('concept')


# given a string that looks like t="type" extract the type
def extract_concept_type_from_string(fullstring):
    return re.match(r'^t=\"(?P<type>.*)\"$', fullstring).group('type')


# given a string that looks like r="TrAP" extract the relation
def extract_relation_from_string(fullstring):
    return re.match(r'^r=\"(?P<relation>.*)\"$', fullstring).group('relation')


# given a concept that looks like c="his home regimen" 111:8 111:10, return the components
def get_concept_subparts(concept):
    concept_name = " ".join(concept.split(' ')[:-2])
    concept_name = extract_concept_from_string(concept_name)

    concept_pos1 = concept.split(' ')[-2]
    concept_pos2 = concept.split(' ')[-1]
    return concept_name, concept_pos1, concept_pos2


# given a position like 111:8 return the line number and word number
def get_line_number_and_word_number(position):
    split = position.split(':')
    return split[0], split[1]


# given a specific concept file path, generate a concept dictionary
def get_concept_dictionary(file_path):
    concept_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            concept = line.split('||')[0]  # line splitting
            type_of_concept = line.split('||')[1]

            type_of_concept = extract_concept_type_from_string(type_of_concept)  # getting useful info
            concept_name, concept_pos1, concept_pos2 = get_concept_subparts(concept)

            line1, _ = get_line_number_and_word_number(concept_pos1)
            line2, _ = get_line_number_and_word_number(concept_pos2)
            if line1 != line2:
                print("There is a problem! Concept spans multiple lines")

            from_to_positions = concept_pos1 + ";" + concept_pos2
            concept_dict[from_to_positions] = {
                'fromto': from_to_positions, 'word': concept_name, 'type': type_of_concept}
    return concept_dict


# given a line number and the concept dictionary, return all the concepts from the
# particular line #
def get_entity_replacement_dictionary(linenum, concept_dict):
    entity_replacement = {}
    for key, val in concept_dict.items():
        dict_linenum = key.split(';')[0].split(':')[0]
        if dict_linenum == linenum:
            fromword = key.split(';')[0].split(':')[1]
            toword = key.split(';')[1].split(':')[1]
            ent_repl_key = str(fromword) + ':' + str(toword)
            entity_replacement[ent_repl_key] = val['type']
    return entity_replacement  # returns a list of dictionaries i.e. from-to, word, type


# given a line in the relation file, return the concept1 word, spans, relation and concept 2 word, spans
def read_rel_line(inpath):
    rel_lines = open(inpath, 'r')
    rel_line = rel_lines.readlines()
    line_dict = dict()
    for line in rel_line:
        line = line.strip()
        concept1 = line.split('||')[0]
        relation = line.split('||')[1]
        concept2 = line.split('||')[2]

        concept1_name, concept1_pos1, concept1_pos2 = get_concept_subparts(concept1)
        concept2_name, concept2_pos1, concept2_pos2 = get_concept_subparts(concept2)
        relation = extract_relation_from_string(relation)

        line1_concept1, from_word_concept1 = get_line_number_and_word_number(concept1_pos1)
        line2_concept1, to_word_concept1 = get_line_number_and_word_number(concept1_pos2)

        line1_concept2, from_word_concept2 = get_line_number_and_word_number(concept2_pos1)
        line2_concept2, to_word_concept2 = get_line_number_and_word_number(concept2_pos2)

        if line1_concept1 != line2_concept1 or line1_concept2 != line2_concept2 or \
                line1_concept1 != line1_concept2:
            print("Concepts are in two different lines")
        # assuming that all the lines are the same
        if line1_concept1 in line_dict.keys():
            # append the new number to the existing array at this slot
            # print "Found duplicate line number....."
            line_dict[line1_concept1].append(
                concept1_name + "||" + from_word_concept1 + "||" + to_word_concept1 + "||" + \
                                  concept2_name + "||" + from_word_concept2 + "||" + to_word_concept2 + "||" + relation


            )
        else:
            # create a new array in this slot
            line_dict.update(
                {line1_concept1: [concept1_name + "||" + from_word_concept1 + "||" + to_word_concept1 + "||" + \
                                  concept2_name + "||" + from_word_concept2 + "||" + to_word_concept2 + "||" + relation
                                  ]
                 }
            )
    return line_dict


# *********************************************************


# *********************************************************
def computeConceptDict(conFilePath):
    cf = open(conFilePath, "r")
    cf_Lines = cf.readlines()
    line_dict = dict()
    # print('成功运行过')
    for cf_line in cf_Lines:
        # print cf_line
        # c="a workup" 27:2 27:3||t="test"
        concept = cf_line.split("||")

        iob_wordIdx = concept[0].split()
        # print concept[0]
        iob_class = concept[1].split("=")
        iob_class = iob_class[1].replace("\"", "")
        iob_class = iob_class.replace("\n", "")
        # test

        # print iob_wordIdx[len(iob_wordIdx)-2],iob_wordIdx[len(iob_wordIdx)-1]
        start_iobLineNo = iob_wordIdx[len(iob_wordIdx) - 2].split(":")
        end_iobLineNo = iob_wordIdx[len(iob_wordIdx) - 1].split(":")
        start_idx = start_iobLineNo[1]
        end_idx = end_iobLineNo[1]
        iobLineNo = start_iobLineNo[0]
        # print "start",start_idx
        # print "end",end_idx

        # print "line Number, start_idx,end_idx, iobclass",iobLineNo,start_idx,end_idx,iob_class
        # line_dict.update({iobLineNo:start_idx+"-"+end_idx+"-"+iob_class})

        if iobLineNo in line_dict.keys():
            # append the new number to the existing array at this slot
            # print "Found duplicate line number....."
            line_dict[iobLineNo].append(start_idx + "-" + end_idx + "-" + iob_class)
        else:
            # create a new array in this slot
            line_dict.update({iobLineNo: [start_idx + "-" + end_idx + "-" + iob_class]})

    #
    # for k,v in line_dict.iteritems():
    #     print k,v

    return line_dict


def prepareIOB_wordList(wordList, lineNumber, IOBwordList, conceptDict, relationDict, dataType):
    # print "Line Number",lineNumber
    # print "Word- List ",wordList
    # print('成功运行过1')
    iobTagList = []

    if str(lineNumber) in conceptDict.keys():
        # print conceptDict[str(lineNumber)]

        # split the tag and get the index of word and tag
        for concept in conceptDict[str(lineNumber)]:
            concept = str(concept).split("-")
            # print "start_idx, end_idx",concept[0],concept[1]
            # if (start_idx - end_idx) is zero then only B- prefix is applicable

            getrange = list(range(int(concept[0]), int(concept[1])))
            getrange.append(int(concept[1]))
            # For all the idx not in getrange assign an O tag
            # print getrange

            if (len(getrange) > 1):

                for idx in range(0, len(getrange)):
                    # print getrange[idx]
                    iobTagList.append(int(getrange[idx]))
                    if (idx == 0):
                        IOBwordList[getrange[idx]] = "B-" + concept[2]
                    else:
                        IOBwordList[getrange[idx]] = "I-" + concept[2]

            else:

                idx = getrange[0]
                iobTagList.append(int(getrange[0]))
                # print idx
                IOBwordList[idx] = "B-" + concept[2]

            # Else for all the indices between start and end apply the I- prefix

        # For all the other words assign O tag
        # 当该行也有关系存在时，先正常设置
        if str(lineNumber) in relationDict.keys():
            for i in range(0, len(IOBwordList)):
                if i not in iobTagList:
                    IOBwordList[i] = "O"
        # # 当该行没有关系时，此时该行有实体存在
        # # 将这样的句子的三分之一设置为正常读取，剩下的设置为delete
        # else:
        #     global N
        #     N += 1
        #     if N % 4 == 0:
        #         for i in range(0, len(IOBwordList)):
        #             if i not in iobTagList:
        #                     IOBwordList[i] = "O"
        #     else:
        #
        #         for i in range(0, len(IOBwordList)):
        #             # if i not in iobTagList:
        #             IOBwordList[i] = "delete"
        for i in range(0, len(IOBwordList)):
            if i not in iobTagList:
                IOBwordList[i] = "O"
    else:
        for i in range(0, len(IOBwordList)):
            if i not in iobTagList:
                IOBwordList[i] = "delete"
        # print "IOB-  List ",IOBwordList
        # print "These Lines have ZERO IOB tags",IOBwordList
        # print "IOB Tag list ",iobTagList

    return IOBwordList


def preparerelationList(relationwords, lineNumber, relationList, relationDict, dataType):
    relationTagList = []
    if str(lineNumber) in relationDict.keys():
        for relation in relationDict[str(lineNumber)]:
            relation = str(relation).split("||")
            # print "start_idx, end_idx",concept[0],concept[1]
            # if (start_idx - end_idx) is zero then only B- prefix is applicable

            getrange = list(range(int(relation[1]), int(relation[2])))
            getrange.append(int(relation[2]))
            # For all the idx not in getrange assign an O tag
            # print getrange

            if (len(getrange) > 1):

                for idx in range(0, len(getrange)):
                    # print getrange[idx]
                    relationTagList.append(int(getrange[idx]))
                    if (idx == len(getrange) - 1):
                        relationList[getrange[idx]].append((relation[6]))
                    else:
                        relationList[getrange[idx]] = "['N']"

            else:

                idx = getrange[0]
                relationTagList.append(int(getrange[0]))
                relationList[idx].append((relation[6]))

            # Else for all the indices between start and end apply the I- prefix

            # For all the other words assign O tag
        for i in range(0, len(relationList)):
            if i not in relationTagList:
                relationList[i] = "['N']"
            # print "IOB- WordList ",IOBwordList
    else:
        # print ""
        for i in range(0, len(relationList)):
            if i not in relationTagList:
                # relationList[i] = "['N']"
                relationList[i] = "delete"

    return relationList


def prepareobjectList(objectwords, lineNumber, objectList, relationDict, dataType):
    objectTagList = []
    if str(lineNumber) in relationDict.keys():
        for relation in relationDict[str(lineNumber)]:
            relation = str(relation).split("||")
            # print "start_idx, end_idx",concept[0],concept[1]
            # if (start_idx - end_idx) is zero then only B- prefix is applicable

            getrange = list(range(int(relation[1]), int(relation[2])))
            getrange.append(int(relation[2]))
            # For all the idx not in getrange assign an O tag
            # print getrange

            if (len(getrange) > 1):

                for idx in range(0, len(getrange)):
                    # print getrange[idx]
                    objectTagList.append(int(getrange[idx]))
                    if (idx == len(getrange) - 1):
                        objectList[getrange[idx]].append(int(relation[5]))
                        # objectList[getrange[idx]] = '[' + str(relation[5]) + ']'
                    else:
                        objectList[getrange[idx]] = '[' + str(getrange[idx]) + ']'


            else:

                idx = getrange[0]
                objectTagList.append(int(getrange[0]))
                # print idx
                objectList[idx].append(int(relation[5]))
                # objectList[idx] = '[' + str(relation[5]) + ']'

            # Else for all the indices between start and end apply the I- prefix

            # For all the other words assign O tag
        for i in range(0, len(objectList)):
            if i not in objectTagList:
                objectList[i] = '[' + str(i) + ']'
                # objectList[i].append(int(i))
            # print "IOB- WordList ",IOBwordList
    else:
        # print ""
        for i in range(0, len(objectList)):
            if i not in objectTagList:
                objectList[i] = '[' + str(i) + ']'
                # objectList[i].append(int(i))
    return objectList


def createData(inpath, outpath, dataType):
    # Make sure you have deleted all the old output files
    if (dataType == 'train'):
        txtPath = inpath + "/train/txt"
        conPath = inpath + "/train/concept"
        relationPath = inpath + "/train/rel"
    elif(dataType == 'test'):
        #txtPath = inpath + "/txt_try"
        #conPath = inpath + "/concept_try"
        #relationPath = inpath + "/rel_try"
        txtPath = inpath + "/test/txt"

        conPath = inpath + "/test/concept"

        relationPath = inpath + "/test/rel"
    elif(dataType == 'dev'):
        txtPath = inpath + "/dev/txt"

        conPath = inpath + "/dev/concept"

        relationPath = inpath + "/dev/rel"


    # remove all the *.txt files present in the path and rewrite it
    # removefilesInDirectoryPath(outpath)

    if (dataType == "train"):

        train_Outfile = open(outpath + "/train.txt", "w+")
    elif(dataType == 'test'):

        test_Outfile = open(outpath + "/test.txt", "w+")
    elif(dataType == 'dev'):
        dev_Outfile = open(outpath + "/dev.txt", "w+")

    conllfileContent = ""
    filecounter = 0
    linecounter = 0
    # get all the list of file names only into the filenames list
    filenamesList = [os.path.basename(x) for x in glob.iglob(txtPath + '/*.txt')]

    for filename in filenamesList:
        # global docNum
        # docNum += 1
        # filecounter += 1

        # print"The number of files processed are ",filecounter,(filename)
        f = open(txtPath + "/" + filename, 'r')
        lines = f.readlines()
        # print "Number of Lines are : " ,len(lines)
        confileName = filename.split(".")
        confileName = confileName[0]

        conceptDict = computeConceptDict(conPath + "/" + confileName + ".con")
        relationDict = read_rel_line(relationPath + "/" + confileName + ".rel")
        filename = filename.split('.')[0]
        # print conceptDict
        # print lines
        for line in range(0, len(lines)):
            words = str(lines[line]).split()
            relationwords = str(lines[line]).split()
            relationwords = [[] for i in range(len(relationwords))]
            objectwords = str(lines[line]).split()
            objectwords = [[] for i in range(len(objectwords))]
            orginial_wordsList = str(lines[line]).split()
            linecounter += 1

            IOBwordList = words
            relationList = relationwords
            objectList = objectwords
            # print words
            lineNumber = line + 1  # Line number starts with 1

            # Prepare the IOB word list
            IOBwordList = prepareIOB_wordList(words, lineNumber, IOBwordList, conceptDict, relationDict, dataType)
            relationList = preparerelationList(relationwords, lineNumber, relationList, relationDict, dataType)
            objectList = prepareobjectList(objectwords, lineNumber, objectList, relationDict, dataType)

            # Merge the words and IOB words list in conll-2003 format
            if dataType == "train":
                if (len(relationList) > 0):
                    if (relationList[0] != 'delete'):
                        train_Outfile.write("#doc" + filename + "\n")
            elif dataType == 'test':
                if (len(relationList) > 0):
                    if (relationList[0] != 'delete'):
                        test_Outfile.write("#doc" + filename + "\n")
                        print(filename)
                        #print(filecounter)
                        print(linecounter)

            elif dataType == 'dev':
                if (len(relationList) > 0):
                    if (relationList[0] != 'delete'):
                        dev_Outfile.write("#doc" + filename + "\n")
            else:
                print('please input "train","test" or "dev",mistake with opening file')
            for w in range(0, len(words)):
                conllfileContent = str(w) + "\t" + orginial_wordsList[w] + "\t" + IOBwordList[w] \
                                   + "\t" + str(relationList[w]) + "\t" + str(objectList[w]) + "\n"
                # print conllfileContent
                if dataType == "train":
                    if(relationList[0] != 'delete'):
                        train_Outfile.write(conllfileContent)


                elif dataType == "test":
                    if(relationList[0] != 'delete'):
                        test_Outfile.write(conllfileContent)
                elif dataType == "dev":
                    if(relationList[0] != 'delete'):
                        dev_Outfile.write(conllfileContent)

            # add an Empty Line after each sentence conll 2003 format


            if dataType == "train":
                if len(orginial_wordsList) == SENTENCE_LENGTH:
                    orginial_wordsList.append("PAD-WORD")
                    IOBwordList.append("O")

                # print "The total number of sentences added untill now",linecounter,orginial_wordsList,IOBwordList
                train_sent_Dict.update({linecounter: orginial_wordsList})
                train_sentLabels_Dict.update({linecounter: IOBwordList})

            elif dataType == 'test':
                if len(orginial_wordsList) == SENTENCE_LENGTH:
                    orginial_wordsList.append("PAD-WORD")
                    IOBwordList.append("O")
                test_sent_Dict.update({linecounter: orginial_wordsList})
                test_sentLabels_Dict.update({linecounter: IOBwordList})
            elif dataType == 'dev':
                if len(orginial_wordsList) == SENTENCE_LENGTH:
                    orginial_wordsList.append("PAD-WORD")
                    IOBwordList.append("O")
                dev_sent_Dict.update({linecounter: orginial_wordsList})
                dev_sentLabels_Dict.update({linecounter: IOBwordList})

    return linecounter

# train_data = createData(in_exp, out_exp, dataType='train')
train_data = createData(train_inpath, train_outpath, dataType='train')
dev_data = createData(dev_inpath, dev_outpath,dataType='dev')
test_data = createData(test_inpath, test_outpath, dataType='test')
