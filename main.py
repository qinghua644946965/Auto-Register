# -*- coding: utf-8 -*-
import os
import string
import random
import re
import time
from curl_cffi import requests
# import requests

from urllib.parse import quote
from loguru import logger
import uvicorn
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 静态文件目录
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
cache = {}

cache["email_v"] = "ranguoxing456@gmail.com"

current_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Current Directory: {current_dir}")


@app.get("/", response_class=HTMLResponse)
async def get_form():
    example_string = "未获取到内容"
    timestamp = int(time.time())
    html_content = f"""
        <html>
            <head>
                <title>Image Form</title>
            </head>
            <body>
                <h1>Submit Your Data</h1>
                <form action="/submit" method="post">
                    <img src="/static/image.jpg?timestamp={timestamp}" alt="Sample Image" width="300"/>
                    <br><br>
                    <label for="input_email">输入邮箱id:</label>
                    <input type="text" id="input_email" name="input_email" value="1" oninput="saveInputValue('input_email')">
                    <br><br>
                    <label for="input_data">输入验证码:</label>
                    <input type="text" id="input_data" name="input_data" oninput="saveInputValue('input_data')">
                    <br><br>
                    <label for="display_string">自动处理验证码:</label>
                    <input type="text" id="display_string" name="display_string" value="{example_string}" readonly onclick="refreshDisplayString()">
                    <br><br>
                    <button type="submit">手动提交</button>
                    <button type="button" onclick="startTask()">开始任务</button>
                </form>
                <script>
                    // 在页面加载时恢复文本框内容
                    window.onload = function() {{
                        const inputId = document.getElementById('input_email');
                        const inputData = document.getElementById('input_data');
                        inputId.value = localStorage.getItem('input_email') || 'xxxxx@gmail.com';
                        inputData.value = localStorage.getItem('input_data') || '';
                    }};

                    // 保存文本框内容到本地存储
                    function saveInputValue(id) {{
                        const input = document.getElementById(id);
                        localStorage.setItem(id, input.value);
                    }}

                    function refreshDisplayString() {{
                        const inputId = document.getElementById('input_email').value;
                        fetch(`/refresh-display-string?input_email=${{inputId}}`)
                            .then(response => response.json())
                            .then(data => {{
                                document.getElementById('display_string').value = data.display_string;
                            }});
                    }}

                    function startTask() {{
                        fetch('/start-task', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{ data: document.getElementById('input_email').value }})
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            alert(data.message);
                        }});
                    }}
                </script>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)


@app.post("/submit")
async def handle_form(input_email: str = Form(...), input_data: str = Form(...)):
    cache["email_v"] = input_email
    if cache.get(input_email) and cache[input_email].get("auto"):
        cache[input_email].update({"sd": input_data})
        cache["email_v"] = input_email
    return {"message": f"You submitted: 邮箱id：{input_email} 输入内容：{input_data}"}


@app.get("/static/image.jpg")
async def get_image():
    try:
        return FileResponse("static/image.jpg", headers={
            "Cache-Control": "no-store"
        })
    except:
        return HTMLResponse("")


@app.get("/refresh-display-string")
async def refresh_display_string(input_email: str):
    ns = cache.get(input_email, {"auto": None, "sd": None})
    if ns.get('sd'):
        ns = f"手动：{ns.get('sd')}"
    elif ns.get('auto'):
        ns = f"自动：{ns.get('auto')}"
    else:
        ns = "未获取到内容"
    return {"display_string": ns}


@app.post("/start-task")
async def start_task(data: dict, background_tasks: BackgroundTasks):
    input_data = data.get("data")
    background_tasks.add_task(background_task, input_data)
    return {"message": "Task started"}


def get_user_name():
    url = "http://www.ivtool.com/random-name-generater/uinames/api/index.php?region=united states&gender=female&amount=5&="
    header = {
        "Host": "www.ivtool.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=1",
    }
    resp = requests.get(url, headers=header, verify=False)
    print(resp.status_code)
    if resp.status_code != 200:
        print(resp.status_code, resp.text)
        raise "获取名字出错"
    data = resp.json()
    return data


def generate_random_username():
    length = random.randint(7, 10)
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def background_task(input_email):
    url1 = "https://www.serv00.com/offer/create_new_account"
    # ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
