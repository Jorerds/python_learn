import xlrd,xlwt
'''
使用xlwt模块来做一个excel生成类
'''
class Merge_excel():
    def __init__(self):
        pass
    # 创建xlwt配置函数
    def set_style(self, name, height, bold=False, horz=0x02, vert=0x01):
        '''
        xlwt文本样式配置函数
        :字体名称 name:
        :字体大小 height:
        :字体是否加粗 bold:
        :文本垂直对齐方式 horz:
        :文本左右对齐 vert:
        :return:
        '''
        style = xlwt.XFStyle()  # 初始化样式

        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1

        al = xlwt.Alignment()
        al.horz = horz
        al.vert = vert

        style.borders = borders
        style.font = font
        style.alignment = al

        return style
    
    def local_excel(self):
        '''
        生成excel文件函数
        获取数据id pkid:  由前端获取到的数据id值传输到客户端
        return:返回整个excel文件
        '''
        #   创建工作簿 
        f=xlwt.Workbook()
        #   创建sheet
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) 
        # 数据
        data=[[1,5,6,8],[6,4,8,9],[4,8,8,2]]

        for e in data:
            for i in range(len(e)):
                # write()为把数据写入上面所创建的excel工作簿
                sheet1.write(,0)
