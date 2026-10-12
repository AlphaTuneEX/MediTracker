import os

def DEBUG(obj, function, key, key_value):
    print("=" * 40)
    print("[DEBUG]", "当前类为", obj.__class__.__name__, "，执行模块为", function, "，步进成功")
    print("[DEBUG]", "关键值", key, "=", key_value)

def ERROR_MSG(code):
    print("=" * 40)
    message = ERROR_LIST.get(code, "UNKNOWN ERROR")
    print(f"[ERROR] {code}: {message}")

def ECHO(text):
    print("=" * 40)
    print("[DEBUG]", text)
    print("=" * 40)

def ADG():
    print(os.getcwd())
    
ERROR_LIST = {
    # 1: 程序内部错误
    10: "引用的值不存在。",
    # 2: 配置错误
    29: "引擎未能在给定的列表中匹配。",
    # 3: 前端错误
    # 4: 文件错误
    40: "指定文件未找到。",
    # 9: 其他错误
    99: "未知错误",
}