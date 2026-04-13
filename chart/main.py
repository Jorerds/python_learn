# 主程序
import os
import sys
def resource_path(relative_path):
    """
    获取资源的绝对路径。
    PyInstaller 打包后会把文件解压到一个临时文件夹，需要用这个函数来定位。
    """
    try:
        # 当程序被打包时，_MEIPASS 是 PyInstaller 创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        # 当程序在开发环境中运行时
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
import re
import time
import builtins
import glob
from PyQt6.QtWidgets import (QApplication,QMainWindow,QLabel,QPushButton,
                             QVBoxLayout,QWidget,QHBoxLayout,QTextBrowser,
                             QLineEdit,QFileDialog,QMessageBox)
from PyQt6.QtCore import QThread,pyqtSignal,pyqtSlot
from PyQt6.QtGui import QIcon
from fixExcel import fix_and_extract_broken_excel
from monthlyWord import docx_work

# 定义一个工作线程
class WorkerThread(QThread):
    # 定义一个结果信号，用于通知主线程任务结束了
    finished_signal=pyqtSignal()

    def __init__(self,target_func,*args,**kwargs):
        """
        :param target_func: 执行函数（注意：不要加括号，传引用）
        :param args: 要传递给那个函数的参数
        :param kwargs:
        """
        super().__init__()
        self.target_func=target_func
        self.args=args
        self.kwargs=kwargs

    def run(self):
        """
        线程启动后，它会自动去执行指定的函数
        :return:
        """
        try:
            self.target_func(*self.args,**self.kwargs)
        except Exception as e:
            print(f"任务出错：{e}")
        finally:
            # 任务结束，发出信号
            self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 图标路径资源
        self.home_loge_icon_path = resource_path(os.path.join('icons', 'home-loge.ico'))
        self.warn_icon_path = resource_path(os.path.join('icons', 'bugreportlogo.ico'))

        self.setWindowTitle("发电机月报图表自动化工具")
        self.setGeometry(500,200,500,400)
        # 设置主窗口图标
        self.setWindowIcon(QIcon(self.home_loge_icon_path))


        # 创建中心部件和布局
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        # 创建主布局（垂直布局）
        main_layout=QVBoxLayout()
        # 子布局（按钮）（水平布局）
        button_layout = QHBoxLayout()

        # 使用容器将子布局存放起来
        h_container = QWidget()
        h_container.setLayout(button_layout)

        # 选择excel文件文件模块布局
        excel_path_layout=QHBoxLayout()
        # 使用容器将选择文件模块存放起来
        excel_path_container=QWidget()
        excel_path_container.setLayout(excel_path_layout)
        # 选择word文件模块布局
        word_path_layout=QHBoxLayout()
        # 使用容器将word模块存放起来
        word_path_container=QWidget()
        word_path_container.setLayout(word_path_layout)
        # 保存文件夹模块布局
        save_path_layout=QHBoxLayout()
        save_path_container=QWidget()
        save_path_container.setLayout(save_path_layout)


        # 创建组件
        # 创建文本
        self.text=QLabel("发电机月报图表自动写入文档")
        # 创建按钮
        self.excel_button=QPushButton("从Excel中提取图表")
        self.excel_button.setStyleSheet("""
            QPushButton{
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #57965c, 
                    stop: 1 #ccffff
                ); /* 渐变色背景颜色 */
                color:white;               /* 文字颜色 */
                border-radius:10px;       /* 圆角半径 */
                padding:10px;             /* 内边距 */
                border: 1.5px solid #ddd;
                border-radius:15px;
            }
            QPushButton:hover{
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #447548, 
                    stop: 1 #ccffff
                ); /* 鼠标悬停时变色 */
            }
            QPushButton:pressed{
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #365c39, 
                    stop: 1 #ccffff
                ); /* 按下时变得更深 */
            }
        """)
        # 创建按钮
        self.word_button=QPushButton("从模板生成月报文档")
        # 通过QSS设置CSS样式来达到改变按钮样式
        self.word_button.setStyleSheet("""
            QPushButton{
                background-color: #3498db; /* 背景颜色 */
                color:white;               /* 文字颜色 */
                border-radius:10px;       /* 圆角半径 */
                padding:10px;             /* 内边距 */
                border: 1.5px solid #ddd;
                border-radius:15px;
            }
            QPushButton:hover{
                background-color: #2980b9;   /* 鼠标悬停时变色 */
            }
            QPushButton:pressed{
                background-color: #1a5276;  /* 按下时变得更深 */
            }
        """)
        # 创建文本框
        self.excel_path_edit=QLineEdit()
        # 创建文字描述
        self.excel_path_text=QLabel("提取图表的Excel文件：")
        self.excel_path_button=QPushButton("...")
        self.excel_path_button.setFixedWidth(40)#调整按钮的宽，窄一点
        self.excel_path_edit.setPlaceholderText("请选择文件...")
        # 设置只读，防止误操作
        self.excel_path_edit.setReadOnly(True)

        self.word_path_edit=QLineEdit()
        self.word_path_text=QLabel("月报word文件模板：")
        self.word_path_button=QPushButton("...")
        self.word_path_button.setFixedWidth(40)
        self.word_path_edit.setPlaceholderText("请选择文件...")
        # 设置只读，防止误操作
        self.word_path_edit.setReadOnly(True)

        # 保存文件夹组件
        self.save_path_edit=QLineEdit()
        self.save_path_text=QLabel("保存的文件夹：")
        self.save_path_button=QPushButton("...")
        self.save_path_button.setFixedWidth(40)
        self.save_path_edit.setPlaceholderText("请选择保存文件夹...")
        # 设置只读，防止误操作
        self.save_path_edit.setReadOnly(True)

        # 将按钮的clicked（点击）信号连接到自定义的槽函数
        self.excel_button.clicked.connect(self.excel_button_clicked)
        self.word_button.clicked.connect(self.word_button_clicked)
        self.excel_path_button.clicked.connect(lambda :self.choose_file(self.excel_path_edit,"Excel文件(*.xlsx)"))
        self.word_path_button.clicked.connect(lambda :self.choose_file(self.word_path_edit,"Word文件(*.docx)"))
        self.save_path_button.clicked.connect(lambda :self.choose_file_dir(self.save_path_edit))


        # 创建文本浏览器（自带滚动条）
        self.log_browser = QTextBrowser()
        self.log_browser.setOpenExternalLinks(True)  # 允许打开链接


        # 添加组件到布局
        main_layout.addWidget(self.text)
        save_path_layout.addWidget(self.save_path_text)
        save_path_layout.addWidget(self.save_path_edit)
        save_path_layout.addWidget(self.save_path_button)
        excel_path_layout.addWidget(self.excel_path_text)
        excel_path_layout.addWidget(self.excel_path_edit)
        excel_path_layout.addWidget(self.excel_path_button)
        word_path_layout.addWidget(self.word_path_text)
        word_path_layout.addWidget(self.word_path_edit)
        word_path_layout.addWidget(self.word_path_button)
        button_layout.addWidget(self.excel_button)
        button_layout.addWidget(self.word_button)
        # 将容器添加到主布局中
        main_layout.addWidget(save_path_container)
        main_layout.addWidget(excel_path_container)
        main_layout.addWidget(word_path_container)
        main_layout.addWidget(h_container)
        main_layout.addWidget(self.log_browser)
        # 最后把主布局设置给窗口
        central_widget.setLayout(main_layout)
        #  --- 重定向 print ---
        self.redirect_print()

        # 创建自定义弹出消息框
        self.msg_box=QMessageBox()
        # 初始化消息框标题
        self.msg_box.setWindowTitle("消息框标题")
        # 初始化消息框内容
        self.msg_box.setText("消息框消息内容")
        # 初始化消息框的图标
        self.msg_box.setIcon(QMessageBox.Icon.Critical)
        on_btn = self.msg_box.addButton("关闭", QMessageBox.ButtonRole.RejectRole)


    def redirect_print(self):
        """
        重定向 print 函数到 GUI
        :return:
        """
        # 保存原始的 print
        old_print = print

        def new_print(*args, **kwargs):
            # 将内容转为字符串
            text = " ".join(map(str, args))
            # 1. 先输出到控制台（保留原功能）
            old_print(text)
            # 2. 发出信号，让主线程更新界面（线程安全的方式）
            # 注意：这里我们直接调用，但在复杂多线程下建议用信号
            # 这里为了简单，直接调用槽函数（或者你可以把 finished_signal 定义在 MainWindow）
            self.log_browser.append(text)

        # 替换全局 print
        builtins.print = new_print

    @pyqtSlot()
    def choose_file(self,path_edit,fi="所有文件(*)"):
        """
        文件选择对话框
        :return:
        """
        file_path,_=QFileDialog.getOpenFileName(
            self,"选择文件","",fi
        )
        if file_path:
            path_edit.setText(file_path)

    def choose_file_dir(self,path_edit):
        """
        选择文件夹
        :param path_edit:传入文件夹路径的对象
        :return:
        """
        folder_path=QFileDialog.getExistingDirectory(
            self,"选择文件夹",""
        )
        if folder_path:
            path_edit.setText(folder_path)

    def excel_button_clicked(self):
        # 获取需要抓取图表的文档路径
        file_path=self.excel_path_edit.text()
        # 获取保存路径
        save_path=self.save_path_edit.text()
        if save_path:
            save_path=re.sub(r'[/]',r'\\',save_path)
            # 判断是否选择了正确的路径
            if file_path:
                file_path=re.sub(r'[/]',r'\\',file_path)
                # 将按钮禁用，防止重复点击
                self.excel_button.setEnabled(False)
                # 创建线程，传入调用脚本和参数
                self.worker=WorkerThread(fix_and_extract_broken_excel,file_path,save_path)
                # 启动线程
                self.worker.start()
                # 连接线程结束信号，结束提示
                self.worker.finished_signal.connect(lambda:print("处理任务结束"))
                # 连接线程结束信号，用于恢复按钮
                self.worker.finished_signal.connect(lambda: self.excel_button.setEnabled(True))
            else:
                self.msg_box.setWindowTitle("提示消息")
                self.msg_box.setWindowIcon(QIcon(self.warn_icon_path))
                self.msg_box.setText("请先选择需要提取图表的Excel文件，再点击按钮提取！")
                self.msg_box.exec()
        else:
            self.msg_box.setWindowTitle("提示消息")
            self.msg_box.setWindowIcon(QIcon(self.warn_icon_path))
            self.msg_box.setText("请先选择保存文件夹！")
            self.msg_box.exec()


    def word_button_clicked(self):
        # 获取word模板文件
        file_path = self.word_path_edit.text()
        # 获取保存路径
        save_path = self.save_path_edit.text()
        if save_path:
            save_path = re.sub(r'[/]', r'\\', save_path)
            if file_path:
                file_path = re.sub(r'[/]', r'\\', file_path)
                img_path = os.path.join(save_path, 'img')
                # 查找图表生成的图片文件
                img_list = glob.glob(img_path + r'\*.png')
                # 将按钮禁用，防止重复点击
                self.word_button.setEnabled(False)
                # 创建线程，传入调用脚本和参数
                self.worker = WorkerThread(docx_work, file_path,img_list,save_path)
                # 启动线程
                self.worker.start()
                # 连接线程结束信号，结束提示
                self.worker.finished_signal.connect(lambda: print("处理任务结束"))
                # 连接线程结束信号，用于恢复按钮
                self.worker.finished_signal.connect(lambda: self.word_button.setEnabled(True))
            else:
                self.msg_box.setWindowTitle("提示消息")
                self.msg_box.setWindowIcon(QIcon(self.warn_icon_path))
                self.msg_box.setText("请先选择需要生成的Word模板文件，再点击按钮生成！")
                self.msg_box.exec()
        else:
            self.msg_box.setWindowTitle("提示消息")
            self.msg_box.setWindowIcon(QIcon(self.warn_icon_path))
            self.msg_box.setText("请先选择保存文件夹！")
            self.msg_box.exec()




if __name__ == '__main__':
    # 创建应用程序实例
    app=QApplication(sys.argv)

    # 创建主窗口
    window=MainWindow()

    # 显示窗口
    window.show()

    # 启动事件循环
    sys.exit(app.exec())