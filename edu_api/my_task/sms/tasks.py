
from edu_api.settings import constanst
from my_task.main import app
from edu_api.utils.send_msg import Message


@app.task(name="send_sms")
def send_sms(phone, code):
    print("这是发送短信的方法")
    message = Message(constanst.API_KEY)
    res = message.send_message(phone, code)
    print(res)
# def send_sms():
#     print('123456789')
#     return "hello"

