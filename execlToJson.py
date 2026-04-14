# execl表格数据转json文件
import xlrd, xlwt, os, json, openpyxl, time, datetime
import csv
from decimal import Decimal


def xlsx_data_list(url, sheetNumber=0):
    """
    对xlsx后缀格式的execl进行数据获取
    :param url:文件路径
    :param sheetNumber:通过索引来获取工作表，默认为第一工作表
    :return: 将表格全部数据以列表形式输出
    """
    # 根据路径读取execl文件
    wb = openpyxl.load_workbook(url)

    sheet_list = wb.sheetnames
    # 读取execl文件中的第一个工作表

    sheet = wb[sheet_list[sheetNumber]]
    # 创建一个空列表，用来存放表格的全部数据
    rows = []

    # 按行迭代，将表格全部数据存入空列表中
    for row in sheet.iter_rows(values_only=True):
        rows.append(list(row))

    # 如果表格为空，则返回None
    if len(rows) == 0:
        rows = None

    # 关闭文件
    wb.close()

    return rows


def xls_data_list(url, sheetNumber=0):
    """
    对xls后缀格式的execl进行数据获取
    :param url:文件路径
    :param sheetNumber:通过索引来获取工作表，默认为第一工作表
    :return: 将表格全部数据以列表形式输出
    """
    # 根据路径读取execl文件
    wb = xlrd.open_workbook(url)

    # 通过索引来获取工作表对象
    sheet_list = wb.sheet_by_index(sheetNumber)

    # 创建一个空列表，用来存放表格的全部数据
    rows = []

    for row in sheet_list.get_rows():
        # 将列表中的数据对象抽出只获取它的值
        row_list = [obj.value for obj in row]
        rows.append(row_list)

    # 如果表格为空，则返回None
    if len(rows) == 0:
        rows = None

    # 关闭execl
    wb.release_resources()
    del wb

    return rows


def general_execl_data_json(url, sheetNumber=0):
    mssg = ""
    json_data = ""
    # 获取文件的拓展名
    file_name, file_extension = os.path.splitext(url)
    # 根据拓展名来匹配选择方法

    if file_extension == '.xlsx':
        data_list = xlsx_data_list(url, sheetNumber)
    elif file_extension == '.xls':
        data_list = xls_data_list(url, sheetNumber)
    else:
        data_list = None
    json_list = []
    for i in data_list[1:]:
        num = 0
        dirc_json = {}
        for r in i:
            top_title = data_list[0][num]
            dirc_json[f'{top_title}'] = r
            num += 1
        json_list.append(dirc_json)

    return json_list


def new_xlsx(url, data_list):
    """
    写入xlsx文件
    :param url: 文件路径
    :param data_list: 写入数据 类型为列表
    :return:
    """
    # 创建一个工作
    wb = openpyxl.Workbook()
    # 激活当前工作簿
    ws = wb.active

    for data in data_list:
        ws.append(data)

    # 保存文件
    wb.save(url)

    return "一共对%s行数据完成了处理！" % len(data_list)