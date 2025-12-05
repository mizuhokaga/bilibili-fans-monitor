import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone


def get_bilibili_user_info_requests(mid: str):
    """使用requests库获取B站用户信息"""
    try:
        url = "https://api.bilibili.com/x/web-interface/card"
        params = {"mid": mid, "photo": "false"}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://space.bilibili.com/",
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

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
            return f"API错误: {result.get('message')}"

    except requests.exceptions.RequestException as e:
        return f"请求错误: {e}"
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"
    except Exception as e:
        return f"未知错误: {e}"


def append_to_file(content: str, filename: str = "bilibili_data_log.txt"):
    """追加内容到文件"""
    try:
        # 检查文件是否存在，如果不存在则创建并添加标题
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("B站用户数据抓取日志\n")
                f.write("=" * 50 + "\n\n")

        # 追加内容
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")

        print(f"✓ 结果已追加到文件: {filename}")
        return filename
    except Exception as e:
        print(f"✗ 保存文件失败: {e}")
        return None


def get_file_summary(filename: str = "bilibili_data_log.txt"):
    """获取文件摘要信息"""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return len(lines)
        except:
            return 0
    return 0


# 获取东八区时间（北京时间）
def get_beijing_time():
    # 获取当前UTC时间
    utc_now = datetime.now(timezone.utc)
    # 转换为东八区（UTC+8）
    beijing_time = utc_now + timedelta(hours=8)
    return beijing_time.strftime("%Y-%m-%d %H:%M:%S")


def main():
    """主函数：抓取数据并追加到文件"""
    print("=" * 50)
    print("B站用户信息抓取工具")
    print("=" * 50)

    current_time = get_beijing_time()  # 使用北京时间
    # date_today = time.strftime("%Y-%m-%d", time.localtime())

    # 要抓取的UP主ID列表
    user_ids = ["640584333", "173276266"]

    print(f"抓取时间: {current_time}")
    print(f"目标用户: {', '.join(user_ids)}")
    print("-" * 50)

    # 构建本次抓取的内容
    log_entry = []
    log_entry.append(f"\n【抓取记录】{current_time}")
    log_entry.append("-" * 40)

    all_success = True

    for mid in user_ids:
        print(f"正在抓取用户 {mid}...")
        info = get_bilibili_user_info_requests(mid)

        if isinstance(info, dict):
            result_line = f"用户名: {info['name']} | 粉丝数: {info['fans']} | 用户ID: {info['mid']}"
            print(f"  ✓ 成功: {result_line}")
            log_entry.append(result_line)
        else:
            error_line = f"用户 {mid} 抓取失败: {info}"
            print(f"  ✗ {error_line}")
            log_entry.append(error_line)
            all_success = False

    # 添加状态和分隔符
    status = "✓ 全部成功" if all_success else "⚠ 部分失败"
    log_entry.append(f"状态: {status}")
    log_entry.append("=" * 40)

    # 转换为字符串
    log_content = "\n".join(log_entry)

    # 追加到日志文件
    log_file = "bilibili_data_log.txt"
    append_to_file(log_content, log_file)

    # 显示摘要
    # total_entries = get_file_summary(log_file)
    # print("-" * 50)
    # print(f"数据抓取完成！")
    # print(f"日志文件: {log_file}")
    # print(f"总记录数: {total_entries} 行")
    # print("=" * 50)

    # 同时保存一份每日备份（可选）
    # daily_file = f"bilibili_data_{date_today}.txt"
    # if not os.path.exists(daily_file):
    #     # 如果是今天第一次运行，创建日备份文件
    #     with open(daily_file, "w", encoding="utf-8") as f:
    #         f.write(f"B站用户数据 - {date_today}\n")
    #         f.write("=" * 50 + "\n\n")

    # 追加到日备份文件
    # with open(daily_file, "a", encoding="utf-8") as f:
    #     f.write(log_content + "\n")

    return log_file


if __name__ == "__main__":
    main()
