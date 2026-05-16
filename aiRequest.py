"""
一个调用大模型AIP的案例
"""
import asyncio
import os
from openai import AsyncOpenAI


async def main():
    client = AsyncOpenAI(
        api_key=os.environ.get('DEEPSEEK_AIP_KEY') # API KEY
        ,base_url='https://api.deepseek.com' # 默认地址
    )
    response = await client.chat.completions.create(
        model="deepseek-v4-pro", # 模型名称
        messages=[
            {"role": "system", "content": "你是一名资深的软件开发工程师"},# 系统角色
            {"role": "user", "content": "python用在rpa上有什么好的工具或者库呢？"}  # 用户角色
        ]
        ,stream=True # 流式返回
        ,reasoning_effort="low" # 理解努力程度
        ,extra_body={"thinking": {"type":"enabled"}} # 添加理解努力程度
    )
    # print(response.choices[0].message.content) # 普通方式输出结果

    async for chunk in response: # 异步流式输出结果
        delta =chunk.choices[0].delta
        if delta.content is not None:
            print(delta.content,end="",flush=True)

if __name__ == '__main__':
    asyncio.run(main())
