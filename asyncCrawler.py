"""
异步请求爬虫
"""
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup


async def fetch(url,sem,session):
    """
    异步请求
    :param url: 地址
    :param sem: 最大并发数
    :param session: 请求头等设置
    :return:
    """
    async with sem:
        try:
            async with session.get(url,timeout=15) as response:
                if response.status==200:
                    html=await response.text()
                    return url,html
                else:
                    print(f'状态码异常{response.status}:{url}')
                    return url,None
        except Exception as e:
            print(f'请求失败{url}:{e}')
            return url,None

async def main():
    desc_list=['张三','李四','王五','赵六','孙七','周八','吴九','郑十']

    urls=[f'http://www.myurl.com/system/tys/WebForms/frmPhoneQuery.aspx?sType=all&sKeyword={i}&ftype=on' for i in desc_list]

    sem=asyncio.Semaphore(20) # 最大并发数

    async with aiohttp.ClientSession(
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;',
        }
    ) as session:
        tasks=[fetch(url,sem,session) for url in urls]
        results=await asyncio.gather(*tasks)

    excel_data=[]
    for url,html in results:
        # 转成lxml
        soup=BeautifulSoup(html,'lxml')
        # 获取属性id为DataGrid1的元素
        table=soup.find(id='DataGrid1')
        # 获取table元素下的子元素tr标签
        tr_list=table.select('tr')
        if len(tr_list)>1:
            # 获取第二个tr标签下面的子元素td
            td_list=tr_list[1].select('td')
            # 获取到工号
            user_numb=td_list[1].select('a>font')[0].text.strip()
            # 获取名字
            user_name=td_list[2].select('a>font')[0].text.strip()
            # 获取部门
            depa_name=td_list[8].select('a>font')[0].text.strip()
            # 名字分割
            user_name=user_name.split()[0]

            excel_data.append([user_numb,user_name,depa_name])




if __name__ == '__main__':
    asyncio.run(main())