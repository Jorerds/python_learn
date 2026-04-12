import re
from datetime import datetime
from execlToJson import xlsx_data_list,new_xlsx

def jiaohu():
    while True:
        print("欢迎使用时间戳转换工具！")
        input_path_find=input("请输入需要转换的文件完整路径（文件格式为xlsx）：")
        pattern=r'\.[a-zA-Z]*'
        matches=re.findall(pattern,input_path_find)
        if matches[0] != '.xlsx':
            print("输入的文件类型并非为xlsx文件,请重新输入！")
            break
        input_number=input("请输入要转换的时间戳所在列（如：第一列则输入1）：")

        if len(re.findall(r'\d',input_number)) ==0:
            print("输入的时间戳列并非为整型数字，请重新输入")
            break
        path_find=r''+input_path_find
        number=int(input_number)
        path_list=re.findall(r'[a-zA-Z][a-zA-Z0-9_:]*\\',path_find)
        path_str=''
        for i in path_list:
            path_str+=i
        unix_to(path_find,number,path_str)

def unix_to(path_find,number,path_str):
    """
    Unix时间戳转换
    """
    numbers=number-1
    data_list=xlsx_data_list(path_find)
    for i in data_list[1:]:
        excel_time = i[numbers]
        if isinstance(excel_time, (int, float)):
            try:
                dt = datetime.fromtimestamp(excel_time/1000)
                i[numbers]=dt
            except ValueError:
                print(f"Invalid timestamp: {excel_time}")
        else:
            print(f"Invalid data type for timestamp: {type(excel_time)}")
    path_url=r''+path_str+f'{datetime.now().strftime("%Y%m%d%H%M%S")}转换后.xlsx'
    mssg=new_xlsx(path_url,data_list)
    print(mssg)

if __name__=='__main__':
    jiaohu()