import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.qqsuu.cn/api/dm-caipu" #https://api.qqsuu.cn/

@plugins.register(name="caipu",
                  desc="搜菜谱",
                  version="1.0",
                  author="wyh",
                  desire_priority=100)




class caipu(Plugin):

    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【搜菜谱 菜名/食材】 获取 菜名/食材相关菜谱"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()

        if self.content.startswith("搜菜谱"):
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.caipu()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️ "
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS


    def caipu(self):
        url = BASE_URL_DM
        params = {"num":3, "word":self.content.replace(" ", "")[3:]}
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            # 主接口
            response = requests.get(url=url, params=params, headers=headers,timeout=2)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('code') == 200 and json_data['data']['list']:
                    data = json_data['data']['list'][:3]
                    logger.info(json_data)

                    formatted_output = []
                    i = 0
                    while i < len(data):
                        basic_info = (
                            f"☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆\n"
                            f"⌛  菜谱ID: {data[i]['id']}\n",
                            f"⌛  类型名称: {data[i]['type_name']}\n",
                            f"⌛  菜肴名称: {data[i]['cp_name']}\n",
                            f"⌛  做法:  {data[i]['zuofa']}\n",
                            f"⌛  特性:  {data[i]['texing']}\n",
                            f"⌛  提示:  {data[i]['tishi']}\n",
                            f"⌛  调料:  {data[i]['tiaoliao']}\n",
                            f"⌛  原料:  {data[i]['yuanliao']}\n"
                        )
                        formatted_output.append(basic_info)
                        i+=1

                    return '\n'.join(['\n'.join(item) for item in formatted_output])
                else:
                    logger.error(f"主接口返回值异常:{json_data}")
                    raise ValueError('not found')
            else:
                logger.error(f"主接口请求失败:{response.text}")
                raise Exception('request failed')
        except Exception as e:
            logger.error(f"接口异常：{e}")

        logger.error("所有接口都挂了,无法获取")
        return None                                                                                                                                                                                                                                                                                                                  
