# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:32:30 2024

@author: TXCF
"""



url = "https://api.qqsuu.cn/api/dm-caipu"
params = {"word":"辣子鸡","num":3}  
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.get(url=url, params=params, headers=headers,timeout=2)

json_data = response.json()

print(json_data)


content = "搜菜谱 辣子鸡"
params = {"num":3, "word":content.replace(" ", "")[3:]}            
headers = {'Content-Type': "application/x-www-form-urlencoded"}

response = requests.get(url=url, params=params, headers=headers,timeout=2)
if response.status_code == 200:
    json_data = response.json()
    if json_data.get('code') == 200 and json_data['data']['list']:
        data = json_data['data']['list'][:10]
        # logger.info(json_data)
                            
        formatted_output = []
        i = 0
        # text = ("周公解梦结果：\n" "--------------------")                    
        while i < len(data):
            basic_info = (
                f"⌛ 菜谱ID: {data[i]['id']}\n",
                f"⌛ 类型名称: {data[i]['type_name']}\n",
                f"⌛ 菜肴名称: {data[i]['cp_name']}\n",
                f"⌛ 做法:  {data[i]['zuofa']}\n",
                f"⌛ 特性:  {data[i]['texing']}\n",
                f"⌛ 提示:  {data[i]['tishi']}\n",
                f"⌛ 调料:  {data[i]['tiaoliao']}\n",
                f"⌛ 原料:  {data[i]['yuanliao']}\n"
            )
            formatted_output.append(basic_info)
            i+=1                  

        return '\n'.join(['\n'.join(item) for item in formatted_output])
