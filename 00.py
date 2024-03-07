import requests
import json
import time
import math
import sys

# 检查命令行参数
if len(sys.argv) != 3:
    print("Usage: python3 <script> <company> <pages>")
    sys.exit(1)

company = sys.argv[1]
pages = int(sys.argv[2])
url = "https://0.zone/api/data/"

emails = []  # 存储 email 的列表

# 创建 Session 对象
session = requests.Session()

try:
    # 请求前n页数据
    for page in range(1, pages + 1):
        data = {
            "title": company,
            "title_type": "email",
            "page": page,
            "pagesize": 40,
            "zone_key_id": ""
        }
        response = session.post(url, json=data)
        response.raise_for_status()  # 检查响应状态码

        time.sleep(2)  # 等待2秒
        json_data = response.json()  # 使用 .json() 方法自动解析 JSON

        total_emails = json_data.get('total', 0)
        max_pages = math.ceil(total_emails / 40)

        if pages > max_pages:
            print(f"警告: 请求的页数超过了最大页数({max_pages})。")
            break

        for item in json_data['data']:
            emails.append(item['email'])

except requests.exceptions.HTTPError as e:
    print(f"HTTP 请求错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    print(f"总共获取的 Email 数量为: {len(emails)}")
    for email in emails:
        print(email)
