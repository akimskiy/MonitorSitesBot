import requests

class Telegram:
    token = None

    def __init__(self, token):
        self.token = token

    def setWebhook (self, url):
        url = 'https://api.telegram.org/bot'+self.token+'/setWebhook'
        files = {'certificate': open('/etc/nginx/ssl/nginx.crt', 'rb')}
        data = {'url': url}
        r = requests.post(url, files=files, data=data)
        return r.json()

    def sendMessage (self, mes):
        url = 'https://api.telegram.org/bot'+self.token+'/sendMessage'
        r = requests.post(url, data=mes)
        return r.json()
