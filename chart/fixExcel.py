# 读取excel里面的所有图表，生成文件保存到本地
import re
from spire.xls import *
from spire.xls.common import *
from PIL import Image as pilImage


def fix_and_extract_broken_excel(excel_path,save_path):
    """
    获取excel里面的图表，转化为图片文件
    :param excel_path:excel文件路径
    :param save_path:图片保存路径
    :return:
    """
    # 创建workbook对象
    workbook = Workbook()
    # 加载文件（Spire的容错性通常比openpyxl高）
    workbook.LoadFromFile(excel_path)
    # 获取保存目录
    current_dir = save_path
    full_path = os.path.join(current_dir, 'img')
    # 没有则创建一个img目录
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    # 遍历所有工作表
    for i in range(workbook.Worksheets.Count):
        sheet = workbook.Worksheets[i]
        # 遍历该工作表所有图表
        for j in range(sheet.Charts.Count):
            chart = sheet.Charts[j]
            temp_img_path = "temp_chart.png"
            try:
                # 将图表转图片并且保存为临时文件
                chart.SaveToImage().Save(temp_img_path)

                with pilImage.open(temp_img_path) as pil_img:
                    # 获取图表的标题
                    chart_title = chart.ChartTitle
                    # 用正则来对标题字符进行过滤
                    sub_chart_title = re.sub(r'[<>:"|?*\\/\x00-\x1f]', '', chart_title)
                    # 用标题来作为文件名
                    img_name = f"{full_path}\\{sub_chart_title}.png"
                    # 重置一下dpi，让图片看起来清晰一些
                    pil_img.save(img_name, dpi=(300, 300), quality=95)

                print(f"成功提取：{img_name}")
            except Exception as e:
                print(f"跳过损坏图表 Sheet:{sheet.Name} Index:{j}，错误：{e}")
            finally:
                # 清理临时文件
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)
    workbook.Dispose()
    return "全部提取完成！"