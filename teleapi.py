import requests
from pprint import pprint
from config import TOKEN, ADMIN_ID


class ApiWorker:
    base_url = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token

    def create_post_request(self, method_name : str, args: dict):
        listed = [str(key) + "=" + str(value) for key, value in args.items()]
        total = self.base_url + self.token + "/" + method_name + "?" + "&".join(listed)
        answer = requests.post(total)
        return answer.json()
    
    def send_message(self, reciever, text):
        method = "sendMessage"
        args = {
            "chat_id" : reciever,
            "text" : text,
            "parse_mode" : "markdown",
            "disable_web_page_preview": True
        }
        answer = self.create_post_request(method, args)
        return answer
        