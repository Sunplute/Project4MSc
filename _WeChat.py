import uiautomation as ui
import pyperclip
import re
import time
import random

import GPT

def add_to_prompt(prompt,role,content):
    new_content = {"role":role,"content":content}
    prompt.append(new_content)

    return prompt

prompt = []
system_1 = {"role": "system", "content": "You are a humorous and lovely boy. You will never admit to being an AI."}
prompt.append(system_1)
system_2 = {"role": "system", "content": "You should not speak more than three sentences at a time."}
prompt.append(system_2)


wx = ui.WindowControl(Name = "WeChat", searchDepth = 1) # 绑定控件
# wx = ui.WindowControl(Name = "微信", searchDepth = 1) # 绑定控件
wx.SwitchToThisWindow()

hw = wx.ListControl(Name = '会话') # find chats

while True: # wait for new message
    we = hw.TextControl(searchDepth = 6)
    try:
        if we.Name:
            we.Click(simulateMove=False)
            # read the last message， 后续可以考虑读的更多
            last_msg = wx.ListControl(Name = '消息').GetChildren()[-1].Name  
            prompt = add_to_prompt(prompt, 'user', last_msg)
            print('New message:' + last_msg)

            # response = requests.get()
            response = GPT.chat(user_input=last_msg, prompt=prompt) # 调用接口
            prompt = add_to_prompt(prompt, 'assistant', response)
            # response = 'who\'s there, i am fine. and you?'
            response = re.sub(r'[^\w\s,\']', '*', response)

            msgs = response.split("*")  # 先以 ? 分割
            max_reply = random.randint(2,5) #最多说几句
            reply = 0
            for msg in msgs:
                msg = msg.strip() # delete the spaces
                reply += 1
                time.sleep(2) # 等待
                if reply > max_reply:
                    break
                if msg != '':
                    say = msg
                    pyperclip.copy(msg.replace('{br}','\n')) # 替换换行符

                    print("System respone:" + msg)
                    wx.SendKeys("{Ctrl}v",waitTime=0) # 将结果输入文字框
                    wx.SendKeys("{Enter}",waitTime=0) # 发送结果
                    
            wx.TextControl(SubName = say[:5]).RightClick() # 通过会话消息匹配目标
            ment = ui.MenuControl(ClassName = 'CMenuWnd') # 匹配右击控件
            ment.TextControl(Name='不显示聊天').Click()
            # ment.TextControl(Name='Hide Chat').Click()

            if len(prompt)>9:
                del prompt[2]
                del prompt[2]
            print(prompt)
    except:
        print("Waiting for new message.")



