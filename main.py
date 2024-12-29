# -*- coding: utf-8 -*-
import os
import string
import random
import re
import time
from curl_cffi import requests
import http.client
import json
# import requests

from urllib.parse import quote
from loguru import logger
import uvicorn
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import base64

app = FastAPI()

# 静态文件目录
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
cache = {}

cache["email_v"] = "ranguoxing456@gmail.com"
cache["proxy_data"] = "none"

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
                    <label for="input_email">输入邮箱:</label>
                    <input type="text" id="input_email" name="input_email" value="1" oninput="saveInputValue('input_email')">
                    <br><br>
                    <label for="input_data">代理地址:</label>
                    <input type="text" id="proxy_data" name="proxy_data" oninput="saveInputValue('proxy_data')">
                    <br><br>
                    <button type="submit">更新数据</button>
                    <button type="button" onclick="startTask()">开始任务</button>
                </form>
                <script>
                    // 在页面加载时恢复文本框内容
                    window.onload = function() {{
                        const inputId = document.getElementById('input_email');
                        const proxy_data = document.getElementById('proxy_data');
                        inputId.value = localStorage.getItem('input_email') || 'xxxxx@gmail.com';
                        proxy_data.value = localStorage.getItem('proxy_data') || '';
                    }};

                    // 保存文本框内容到本地存储
                    function saveInputValue(id) {{
                        const input = document.getElementById(id);
                        localStorage.setItem(id, input.value);
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
async def handle_form(input_email: str = Form(...),
                      proxy_data: str = Form(...)):
    cache["email_v"] = input_email
    cache["proxy_data"] = proxy_data
    return {"message": f"You submitted: 邮箱：{input_email} 代理地址：{proxy_data}"}


@app.get("/static/image.jpg")
async def get_image():
    try:
        return FileResponse("static/image.jpg",
                            headers={"Cache-Control": "no-store"})
    except:
        return HTMLResponse("")


@app.post("/start-task")
async def start_task(data: dict, background_tasks: BackgroundTasks):
    input_data = data.get("data")
    background_tasks.add_task(background_task, input_data)
    return {"message": "Task started"}


def get_user_name():
    url = "http://www.ivtool.com/random-name-generater/uinames/api/index.php?region=united states&gender=female&amount=5&="
    header = {
        "Host": "www.ivtool.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":
        "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
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

    header1 = {
        "Host": "www.serv00.com",
        "User-Agent": ua,
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":
        "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        # "Referer": "https://www.serv00.com/offer/create_new_account",
        "Referer": "https://www.serv00.com/offer",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=1",
    }

    captcha_url = "https://www.serv00.com/captcha/image/{}/"
    header2 = {
        "Host": "www.serv00.com",
        "User-Agent": ua,
        "Accept": "image/avif,image/webp,*/*",
        "Accept-Language":
        "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.serv00.com/offer/create_new_account",
        "Cookie": "csrftoken={}",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "TE": "trailers",
    }

    url3 = "https://www.serv00.com/offer/create_new_account.json"
    header3 = {
        "Host": "www.serv00.com",
        "User-Agent": ua,
        "Accept": "*/*",
        "Accept-Language":
        "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.serv00.com",
        "Connection": "keep-alive",
        "Referer": "https://www.serv00.com/offer/create_new_account",
        "Cookie": "csrftoken={}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
    }

    # 初始化变量
    outer_condition = True
    inner_condition = True

    while outer_condition:
        inner_condition = True
        with requests.Session() as session:
            logger.info("获取网页信息")
            proxy_data = cache["proxy_data"]
            print("proxy_data : " + proxy_data)
            print(proxy_data != "none" and proxy_data != "")
            proxies = {}
            if ((proxy_data != "none") and (proxy_data != "")):
                proxies = {"https": proxy_data}

            if "https" in proxies:
                print("proxy~~~~~~~")
                resp = session.get(url=url1,
                                   headers=header1,
                                   impersonate="chrome124",
                                   proxies=proxies)
            else:
                print("no proxy~~~~~~~")
                resp = session.get(url=url1,
                                   headers=header1,
                                   impersonate="chrome124")
            logger.info("~~~~~~~~")
            logger.info(resp)
            logger.info("++++++++++")
            print(resp.status_code)
            headers = resp.headers
            content = resp.text

            csrftoken = re.findall(r"csrftoken=(\w+);",
                                   headers.get("set-cookie"))[0]
            # csrftoken = csrftoken or re.findall(r"input type='hidden' name='csrfmiddlewaretoken' value='(\w+)'", content)[0]
            print("csrftoken", csrftoken)
            header2["Cookie"] = header2["Cookie"].format(csrftoken)
            header3["Cookie"] = header3["Cookie"].format(csrftoken)

            captcha_0 = re.findall(
                r'id=\"id_captcha_0\" name=\"captcha_0\" value=\"(\w+)\">',
                content)[0]
            while inner_condition:
                if proxy_data != cache["proxy_data"]:
                    print("代理地址发生变化,任务已经停止，请重新开启任务！！！！")
                    outer_condition = False
                    inner_condition = False
                    continue
                time.sleep(random.uniform(7.5, 30))
                usernames = get_user_name()
                _ = usernames.pop()
                first_name = _["name"]
                last_name = _["surname"]
                username = generate_random_username().lower()
                input_email = cache["email_v"]
                email = input_email
                logger.info(f"{email} {first_name} {last_name} {username}")

                logger.info("获取验证码")
                capt = {}
                if "https" in proxies:
                    resp = session.get(
                        url=captcha_url.format(captcha_0),
                        headers=dict(
                            header2,
                            **{"Cookie": header2["Cookie"].format(csrftoken)}),
                        impersonate="chrome124",
                        proxies=proxies)
                else:
                    resp = session.get(
                        url=captcha_url.format(captcha_0),
                        headers=dict(
                            header2,
                            **{"Cookie": header2["Cookie"].format(csrftoken)}),
                        impersonate="chrome124")

                content = resp.content

                with open(current_dir + "/static/image.jpg", "wb") as f:
                    f.write(content)

                base64_string = base64.b64encode(content).decode('utf-8')

                url = "https://uncertain-beitris-xiaoerje-6e06a8d9.koyeb.app/api"

                payload = json.dumps(
                    {"image": "data:image/png;base64," + base64_string})
                headers = {'Content-Type': 'application/json'}

                try:
                    response = requests.request("POST",
                                            url,
                                            headers=headers,
                                            data=payload)
                except Exception:
                    print("验证码识别接口调用失败~~~~")
                    continue
                    
                response_text = response.text

                print(response_text)

                # 将响应数据转换为 JSON 对象
                try:
                    json_response = json.loads(response_text)
                    print("识别验证码成功 Response JSON:", json_response)
                    captcha_1 = json_response["data"]
                except json.JSONDecodeError:
                    print("Response is not valid JSON:", response_text)
                    print("识别验证码失败")
                    continue

                print("captcha_0", captcha_0)

                print({
                    first_name, last_name, username, email, captcha_0,
                    captcha_1
                })
                data = f"csrfmiddlewaretoken={csrftoken}&first_name={first_name}&last_name={last_name}&username={username}&email={quote(email)}&captcha_0={captcha_0}&captcha_1={captcha_1}&question=0&tos=on"
                time.sleep(random.uniform(0.5, 1.2))
                logger.info("请求信息")
                if "https" in proxies:
                    resp = session.post(
                        url=url3,
                        headers=dict(
                            header3,
                            **{"Cookie": header3["Cookie"].format(csrftoken)}),
                        data=data,
                        impersonate="chrome124",
                        proxies=proxies)
                else:
                    resp = session.post(
                        url=url3,
                        headers=dict(
                            header3,
                            **{"Cookie": header3["Cookie"].format(csrftoken)}),
                        data=data,
                        impersonate="chrome124")
                print(resp.status_code)
                print(resp.text)
                try:
                    content = resp.json()
                except json.JSONDecodeError:
                    print("提交注册失败~~~~")
                    continue
                if content.get("captcha") and content["captcha"][
                        0] == "Invalid CAPTCHA":
                    captcha_0 = content["__captcha_key"]
                    logger.warning("验证码错误，正在重新获取")
                    time.sleep(random.uniform(0.5, 1.2))
                    continue
                elif content["username"][
                        0] == "Maintenance time. Try again later.":
                    captcha_0 = content["__captcha_key"]
                    logger.warning("Maintenance time. Try again later....")
                    time.sleep(random.uniform(0.5, 1.2))
                    continue
                else:
                    logger.warning("貌似注册成功了~~~~~....")
                    outer_condition = False
                    inner_condition = False
                    break

    os.remove("static/image.jpg")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
