import re
from datetime import datetime
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from execlToJson import xlsx_data_list,new_xlsx

def list_files_recursive(directory,extension='*'):
    """
    递归读取目录里的文件
    :param directory: 目录路径
    :param extension: 可选读取指定扩展名文件
    :return:
    """
    path=Path(directory)
    return [f for f in path.rglob(extension) if f.is_file()]


def xlsx_unix_to(path_find,number):
    """
    xlsx文件类型时间戳转化方法
    :param path_find: 文件路径
    :param number: 时间戳所在的列
    :return:
    """
    numbers=number-1
    data_list=xlsx_data_list(path_find)
    for i in data_list[1:]:
        excel_time = int(i[numbers])
        if isinstance(excel_time, (int, float)):
            try:
                if len(str(excel_time))==10:
                    # 秒级
                    dt = datetime.fromtimestamp(excel_time)
                elif len(str(excel_time))==13:
                    # 毫秒级
                    dt = datetime.fromtimestamp(excel_time/1000)
                elif len(str(excel_time)) == 16:
                    # 微秒级
                    dt = datetime.fromtimestamp(excel_time/1e6)
                elif len(str(excel_time)) == 19:
                    # 纳秒级
                    dt = datetime.fromtimestamp(excel_time/1e9)
                # i[numbers]=dt
                i.append(dt)
            except ValueError:
                print(f"Invalid timestamp: {excel_time}")
        # else:
        #     print(f"Invalid data type for timestamp: {type(excel_time)}")
    # path_url=r''+path_str+f'{datetime.now().strftime("%Y%m%d%H%M%S")}转换后.xlsx'
    mssg=new_xlsx(path_find,data_list)
    # print(mssg)

def validate_unix_time(unix_time):
    """
    根据时间戳判断秒级、毫秒级、微秒级以及纳秒级进行转换处理
    :param unix_time: 时间戳数据
    :return: 返回datetime类型数据
    """
    data_time=''
    if len(str(unix_time)) < 13:
        # 秒级 标记utc时区，然后再转中国时区
        data_time=pd.to_datetime(unix_time,unit='s',utc=True).tz_convert('Asia/Shanghai')
    elif len(str(unix_time)) == 13:
        # 毫秒级
        data_time=pd.to_datetime(unix_time,unit='ms',utc=True).tz_convert('Asia/Shanghai')
    elif len(str(unix_time)) == 16:
        # 微秒级
        data_time=pd.to_datetime(unix_time,unit='us',utc=True).tz_convert('Asia/Shanghai')
    elif len(str(unix_time)) == 19:
        # 纳秒级
        data_time=pd.to_datetime(unix_time,unit='ns',utc=True).tz_convert('Asia/Shanghai')
    return data_time


def unix_csv(file_path,number):
    """
    cvs文件类型时间戳转换方法
    :param file_path: 文件路径
    :param number: 时间戳数据所在列
    :return:
    """
    # 读取cvs文件内容
    try:
        number=number-1
        df = pd.read_csv(file_path, encoding='utf-8')
        # 根据列位置获取列名
        column_name =df.columns[number]
        # 判断是否存在空值
        if df[column_name].count()==df[column_name].shape[0]:
            # 判断数据类型
            if df[column_name].dtypes==int:
                # 向量化操作，对整列数据进行操作
                df['data_time']=df[column_name].apply(validate_unix_time)
        df.to_csv(file_path, index=False)
        # print(str(file_path)+"完成")
    except Exception as e:
        print(e)

def file_to(file_path,number):
    """
    根据不同的文件类型来进行处理
    :param file_path:
    :param number:
    :return:
    """
    pattern = r'\.[a-zA-Z]*'
    matches = re.findall(pattern, str(file_path))
    if matches[0] == '.xlsx':
        xlsx_unix_to(file_path, int(number))
    elif matches[0] == '.csv':
        unix_csv(file_path, int(number))
    else:
        print(str(file_path) + "并非为csv或xlsx文件，跳过此次操作！")

def main():
    """
    主程序，创建任务和线程
    :return:
    """
    # 状态
    state=1
    print("欢迎使用时间戳转换工具！")
    while True:
        if state==1:
            input_path_find = input("请输入需要转换的文件所在的目录（完整目录）：")
            state=2
            if not Path(input_path_find).exists():
                print("目录不存在，请检查后再执行！")
                break
        elif state==2:
            input_number = input("请输入要转换的时间戳所在列（如：第一列则输入1）：")
            state=3
            if len(re.findall(r'\d', input_number)) == 0:
                print("输入的时间戳列并非为整型数字，请重新输入")
                state=2
                continue
        elif state==3:
            path_url=input_path_find
            file_list=list_files_recursive(path_url,'*.csv')
            file_list+=list_files_recursive(path_url,'*.xlsx')
            # 创建多线程，用线程池来控制并发
            with ThreadPoolExecutor(max_workers=10) as executor:
                list(tqdm(executor.map(lambda f:file_to(f,input_number),file_list),total=len(file_list),desc='数据转换中'))
            # for file in file_list:
            #     pattern = r'\.[a-zA-Z]*'
            #     matches = re.findall(pattern, str(file))
            #     if matches[0] == '.xlsx':
            #         xlsx_unix_to(file, int(input_number))
            #     elif matches[0] == '.csv':
            #         unix_cvs(file,int(input_number))
            #     else:
            #         print(file+"并非为csv或xlsx文件，跳过此次操作！")
            break



if __name__=='__main__':
    main()