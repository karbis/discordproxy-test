from flask import Flask, redirect, request, make_response
import requests

app = Flask(__name__)

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
def proxy_request(path):
    discord_url = f'https://discord.com/api/{path}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    headers.update(request.headers)

    if request.method == 'GET':
        response = requests.get(discord_url, headers=headers)
    elif request.method == 'POST':
        response = requests.post(discord_url, headers=headers, data=request.get_data())
    elif request.method == 'PUT':
        response = requests.put(discord_url, headers=headers, data=request.get_data())
    elif request.method == 'PATCH':
        response = requests.patch(discord_url, headers=headers, data=request.get_data())
    elif request.method == 'DELETE':
        response = requests.delete(discord_url, headers=headers, data=request.get_data())
    elif request.method == 'OPTIONS':
        response = requests.options(discord_url, headers=headers)

    resp = make_response(response.content)
    resp.headers['Content-Type'] = response.headers['Content-Type']
    return resp

@app.route('/')
def index():
    return redirect('https://discord.com')

if __name__ == '__main__':
    app.run()