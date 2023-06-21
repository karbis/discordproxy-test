from flask import Flask, redirect, request, make_response
import requests

app = Flask(__name__)

@app.route('/api/<path:path>', methods=['GET', 'POST'])
def proxy_request(path):
    discord_url = f'https://discord.com/api/{path}'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenAI-Chatbot/1.0)'}
    
    if request.method == 'GET':
        response = requests.get(discord_url, headers=headers)
    elif request.method == 'POST':
        response = requests.post(discord_url, headers=headers, data=request.get_data())
    
    resp = make_response(response.content)
    resp.headers['Content-Type'] = response.headers['Content-Type']
    return resp

@app.route('/')
def index():
    return redirect('https://discord.com')

if __name__ == '__main__':
    app.run()
