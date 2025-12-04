import requests
import json
import time


def get_bilibili_user_info_requests(mid: str):
    """使用requests库获取B站用户信息（推荐）"""
    try:
        url = "https://api.bilibili.com/x/web-interface/card"
        params = {"mid": mid, "photo": "false"}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://space.bilibili.com/",
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误

        result = response.json()

        if result.get("code") == 0:
            data = result.get("data")
            user_info = {
                "mid": data["card"]["mid"],
                "name": data["card"]["name"],
                "fans": data["card"]["fans"],
            }
            return user_info
        else:
            print(f"API错误: {result.get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    return None


if __name__ == "__main__":
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info_173276266 = get_bilibili_user_info_requests("173276266")
    info_640584333 = get_bilibili_user_info_requests("640584333")
    if info_173276266:
        print(f"用户信息: {info_173276266},抓取时间: {current_time}")
    if info_640584333:
        print(f"用户信息: {info_640584333},抓取时间: {current_time}")
