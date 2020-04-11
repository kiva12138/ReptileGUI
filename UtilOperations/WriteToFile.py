import os


def writeToFile(content, number, context_name, path):
    if not os.path.isdir(str(path) + '\\' + str(context_name)):
        os.mkdir(str(path) + '\\' + str(context_name))
    with open(str(path) + '\\' + str(context_name) + '\\' + str(number) + '.jpg', 'wb') as f:
        try:
            f.write(content)
        except:
            print('淦!鬼知道为什么文件写入失败！可能搜的东西有问题或者网站改了。')
