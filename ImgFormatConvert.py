# -*- coding:utf-8 -*-
import os
import sys, getopt
import glob
from PIL import Image

FILENAME = None
SUPPORT_FORMATS = ['bmp', 'eps', 'gif', 'icns', 'im', 'jpg', 'jpeg', 
        'msp', 'pcx', 'png', 'ppm', 'spider', 'tiff', 'webp', 'xbm']
VERSION = '0.2.0'
DATE = '2019-06-13'

def usage():
    print(
            """
            ========================================================
            实现%s格式图片之间的转换

            Usage: python %s [option]
            -h or --help    : 显示帮助信息
            -r or --recur   : 递归进行格式转换
            -p or --path=   : 原始图片绝对路径，若不指定则为当前路径
            -s or --save=   : 保存图片绝对路径，若不指定则在当前文件夹下创建目标格式名文件夹
            -f or --from=   : 原始图片格式，若不指定则为全部支持格式，传入列表，列表元素间不得存在空白符
            -t or --to=     : 保存图片格式，支持转换为多种格式，传入列表，列表元素间不得存在空白符
            -v or --version : 显示版本信息
            ========================================================
            """
            % (str(SUPPORT_FORMATS), FILENAME)
            )



def version():
    print(
            """
            ========================================================
            Name    : %s
            Author  : RuriApoka
            Date    : %s
            Version : %s
            ========================================================
            """
            % (FILENAME, DATE, VERSION)
            )



def formatPath(path):
    if path[-1] == '/':
        path = path[:-1]
    return path



def liststrToStrlist(list_str):
    list_str = list_str[1:-1]           # 由于输入的是字符串表示的列表，所以先将首尾的方括号去掉
    str_list = list_str.split(',')
    return str_list



def legalFormat(format_list):
    for i in range(len(format_list)):
        format_list[i] = format_list[i].lower()             # 统一将格式名转换为小写
        if format_list[i] not in SUPPORT_FORMATS:
            print('格式%s不受支持，请重新检查支持列表！' % format)
            return False
    return True



def convertFormat(source_path, dest_path, source_format, dest_format, recursion):
    s_paths = [source_path]
    d_paths = [dest_path]

    # 若指定递归转换，首先列出所有子文件夹，方便之后访问
    if recursion:
        for root, dirs, files in os.walk(source_path):
            if len(dirs) > 0:
                for name in dirs:
                    if name.lower() not in dest_format:
                        s_paths.append(os.path.join(root, name))
                        d_paths.append(os.path.join(d_paths[0] + root.split(s_paths[0])[1], name))      # 用来创建相同的目录结构

    # 针对每个文件夹下的文件进行格式转换
    for s_path, d_path in zip(s_paths, d_paths):
        for s_format in source_format:
            source_files = glob.glob('%s/*.%s' % (s_path, s_format))
            if len(source_files) > 0:
                for d_format in dest_format:
                    save_path = os.path.join(d_path, d_format.upper())
                    if not os.path.isdir(save_path):
                        os.makedirs(save_path)
                    for file in source_files:
                        with Image.open(file) as img:
                            if d_format in ['jpg', 'jpeg']:
                                img = img.convert('RGB')
                            filename = file.split('/')[-1]                      # 截取短文件名
                            filename = filename[:-len(s_format)] + d_format     # 更改文件后缀名
                            filename = os.path.join(save_path, filename)        # 将文件名加入到绝对路径
                            img.save(os.path.join(save_path, filename))
                            print('%s 已保存' % filename)



def main(argv):
    source_path = os.getcwd()
    dest_path = os.getcwd()

    source_format = SUPPORT_FORMATS
    dest_format = None

    recursion = False

    # 读入命令行参数
    opts, args = getopt.getopt(argv, 'hrp:s:f:t:v', ['help', 'recur', 'path=', 'save=', 'from=', 'to=', 'version'])

    # 如果用户想要读取帮助，则无需继续处理
    if ('-h', '') in opts or ('--help', '') in opts:
        usage()
        return

    # 如果用户想要查看版本信息，则无需继续处理
    if ('-v', '') in opts or ('--version', '') in opts:
        version()
        return

    # 处理命令行参数
    for option, value in opts:
        if option in ['-h', '--help']:
            pass
        elif option in ['-r', '--recur']:
            recursion = True
        elif option in ['-p', '--path']:
            source_path = formatPath(value)
        elif option in ['-s', '--save']:
            dest_path = formatPath(value)
        elif option in ['-f', '--from']:
            source_format = liststrToStrlist(value)
        elif option in ['-t', '--to']:
            dest_format = liststrToStrlist(value)
        elif option in ['-v', '--version']:
            pass

    if dest_format is None:
        print('目标格式不得缺省！')
        return

    if legalFormat(source_format) and legalFormat(dest_format):
        convertFormat(source_path, dest_path, source_format, dest_format, recursion)

if __name__ == "__main__":
    _, FILENAME = os.path.split(sys.argv[0])
    main(sys.argv[1:])
