import os
import shutil
import glob

inpath = 'test'
inpath_train = 'training_20180910'

outdata = 'data'
data_total_path_test = 'data/test'
data_total_path_dev = 'data/dev'
data_total_path_train = 'data_new_0622/train'

count = 0

def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def data_merge(inpath , outpath):
    txtpath = inpath + '/txt'
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
    txtpath = inpath
    filecount = 0
    dev_count1 = 0
    filenamelist = [os.path.basename(x) for x in glob.iglob(txtpath + '/*txt')]
    #print(len(filenamelist))
    # print(int(0.8 * len(filenamelist)))
    makedir(outpath + '/dev')
    makedir(outpath + '/train')
    for filename in filenamelist:  # 遍历文件名
        global count
        count += 1
        head = filename.split('.')[0]
        confilename = head + '.ann'

        if count % 5 == 1:
            shutil.copy2(inpath + '/' + filename, outpath + '/dev')
            shutil.copy2(inpath + '/' + confilename, outpath + '/dev')
            dev_count1 += 1
        else:
            shutil.copy2(inpath + '/' + filename, outpath + '/train')
            shutil.copy2(inpath + '/' + confilename, outpath + '/train')

# merge the training data and test data
makedir(data_total_path_test )

# run the divide_data function to divide data into train data, test data, dev data

# divide_data(inpath_train,outdata)




