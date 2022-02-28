import os
import shutil
import glob

inpath = 'reference_standard_for_test_data'
outpath = 'i2b2_256_85_85_cased'

data_merge_inpath1 = 'concept_assertion_relation_training_data/beth'
data_merge_inpath2 = 'concept_assertion_relation_training_data/partners'
data_merge_inpath3 = 'reference_standard_for_test_data'
data_total_path = 'data_total_path'
data_total_path_test = 'data_total_path_test'

data_merge_outpath = 'reference_standard_for_test_data'

data_merge_outpath1 = 'i2b2_170_256/train'
data_merge_outpath2= 'i2b2_170_256/test'

data_merge_outpath3 = 'i2b2_256_85_85/train'
data_merge_outpath4 = 'i2b2_256_85_85/test'
data_merge_outpath5 = 'i2b2_256_85_85/dev'
count = 0
def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def data_merge(inpath , outpath):
    txtpath = inpath + '/txt'
    conpath = inpath + '/concept'
    relpath = inpath + '/rel'
    filecount = 0
    filenamelist = [os.path.basename(x) for x in glob.iglob(txtpath + '/*txt')]
    makedir(outpath + '/txt')
    makedir(outpath + '/concept')
    makedir(outpath + '/rel')
    #可以用os.walk（）来代替
    for filename in filenamelist:
        head = filename.split('.')[0]
        confilename = head + '.con'
        relfilename = head + '.rel'
        shutil.copy2(inpath + '/txt/' + filename, outpath + '/txt')
        shutil.copy2(inpath + '/concept/' + confilename, outpath + '/concept')
        shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/rel')

def divide_data(inpath , outpath):
    txtpath = inpath + '/txt'
    conpath = inpath + '/concept'
    relpath = inpath + '/rel'
    filecount = 0
    filenamelist_txt = [os.path.basename(x) for x in glob.iglob(txtpath + '/*txt')]
    filenamelist_con = [os.path.basename(x) for x in glob.iglob(conpath + '/*con')]
    filenamelist_rel = [os.path.basename(x) for x in glob.iglob(relpath + '/*rel')]
    print(len(filenamelist_txt))

    makedir(outpath + '/train/txt/')
    makedir(outpath + '/train/concept/')
    makedir(outpath + '/train/rel/')
    makedir(outpath + '/dev/txt/')
    makedir(outpath + '/dev/concept/')
    makedir(outpath + '/dev/rel/')
    makedir(outpath + '/test/txt/')
    makedir(outpath + '/test/concept/')
    makedir(outpath + '/test/rel/')

    for filename in filenamelist_txt:  # 遍历文件名

        #rint([filenamelist[filecount], filenamelist.index(filename)])
        head = filename.split('.')[0]
        confilename = head + '.con'
        relfilename = head + '.rel'
        global count
        count += 1

        test_count = int(0.2 * len(filenamelist_txt))
        dev_count = int(0.2 * len(filenamelist_txt))
        train_count = int(len(filenamelist_txt))-test_count-dev_count


        if count % 5 == 2:
            shutil.copy2(inpath + '/txt/' + filename, outpath + '/dev/txt/')
            shutil.copy2(inpath + '/concept/' + confilename, outpath + '/dev/concept/')
            shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/dev/rel/')
        elif count % 5 == 3:
            shutil.copy2(inpath + '/txt/' + filename, outpath + '/test/txt/')
            shutil.copy2(inpath + '/concept/' + confilename, outpath + '/test/concept/')
            shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/test/rel/')
        else:
            shutil.copy2(inpath + '/txt/' + filename, outpath + '/train/txt/')
            shutil.copy2(inpath + '/concept/' + confilename, outpath + '/train/concept/')
            shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/train/rel/')

        filecount += 1

def divide_data1(inpath , outpath):
    txtpath = inpath + '/txt'
    conpath = inpath + '/concept'
    relpath = inpath + '/rel'
    filecount = 0
    filenamelist = [os.path.basename(x) for x in glob.iglob(txtpath + '/*txt')]
    print(len(filenamelist))
    print(int(0.6 * len(filenamelist)))
    makedir(outpath + '/train/txt/')
    makedir(outpath + '/train/concept/')
    makedir(outpath + '/train/rel/')
    makedir(outpath + '/dev/txt/')
    makedir(outpath + '/dev/concept/')
    makedir(outpath + '/dev/rel/')
    makedir(outpath + '/test/txt/')
    makedir(outpath + '/test/concept/')
    makedir(outpath + '/test/rel/')

    for filename in filenamelist:  # 遍历文件名

        #rint([filenamelist[filecount], filenamelist.index(filename)])
        head = filename.split('.')[0]
        confilename = head + '.con'
        relfilename = head + '.rel'
        #train_count = int(0.6*len(filenamelist))
        dev_count = int(0.5*len(filenamelist))
        test_count = int(len(filenamelist))-dev_count
        print(dev_count)
        print(test_count)
        if filecount <= dev_count:
            shutil.copy2(inpath + '/txt/' + filename, outpath + '/dev/txt/')
            shutil.copy2(inpath + '/concept/' + confilename, outpath + '/dev/concept/')
            shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/dev/rel/')
        else :
            shutil.copy2(inpath + '/txt/' + filename, outpath + '/test/txt/')
            shutil.copy2(inpath + '/concept/' + confilename, outpath + '/test/concept/')
            shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/test/rel/')

        filecount += 1

def divide_data2(inpath , outpath):
    txtpath = inpath + '/txt'
    conpath = inpath + '/concept'
    relpath = inpath + '/rel'
    filecount = 0
    filenamelist = [os.path.basename(x) for x in glob.iglob(txtpath + '/*txt')]
    #print(len(filenamelist))
    #print(int(0.6 * len(filenamelist)))
    makedir(outpath + '/train/txt/')
    makedir(outpath + '/train/concept/')
    makedir(outpath + '/train/rel/')
    makedir(outpath + '/dev/txt/')
    makedir(outpath + '/dev/concept/')
    makedir(outpath + '/dev/rel/')
    makedir(outpath + '/test/txt/')
    makedir(outpath + '/test/concept/')
    makedir(outpath + '/test/rel/')

    for filename in filenamelist:  # 遍历文件名

        #rint([filenamelist[filecount], filenamelist.index(filename)])
        head = filename.split('.')[0]
        confilename = head + '.con'
        relfilename = head + '.rel'
        # train_count = int(0.6*len(filenamelist))
        # dev_count = int(0.2*len(filenamelist))
        # test_count = int(len(filenamelist))-train_count-dev_count

       # if filecount <= train_count:
        shutil.copy2(inpath + '/txt/' + filename, outpath + '/train/txt/')
        shutil.copy2(inpath + '/concept/' + confilename, outpath + '/train/concept/')
        shutil.copy2(inpath + '/rel/' + relfilename, outpath + '/train/rel/')
        filecount += 1

divide_data(data_total_path , outpath)


