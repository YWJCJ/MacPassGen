import hashlib
import uuid
import random
import string


def get_mac_address():
    """获取设备MAC地址"""
    try:
        # 获取本机MAC地址
        mac = uuid.getnode()
        # 转换为标准MAC地址格式
        mac_address = ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
        return mac_address
    except Exception:
        # 如果获取失败，使用随机生成的MAC地址作为后备
        return "00:11:22:33:44:55"


def extract_mac_suffix(mac_address):
    """提取MAC地址后6位"""
    # 移除冒号并取后6位
    mac_digits = mac_address.replace(':', '')
    return mac_digits[-6:].upper()


def generate_password(mac_suffix):
    """基于MAC地址后6位生成16位随机密码"""
    # 使用MAC后6位作为种子
    seed_str = mac_suffix + "_secret_salt"
    seed_hash = hashlib.sha256(seed_str.encode()).hexdigest()
    
    # 设置随机种子
    random.seed(int(seed_hash[:16], 16))
    
    # 定义密码字符集（仅数字和字母）
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    
    # 合并字符集
    all_chars = lowercase + uppercase + digits
    
    # 生成16位随机密码
    password = ''.join(random.choice(all_chars) for _ in range(16))
    
    return password


def get_user_mac_suffix():
    """获取用户输入的MAC地址后6位"""
    while True:
        user_input = input("请输入设备MAC地址后6位 (或直接按回车使用本机MAC地址): ").strip()
        
        if not user_input:
            # 使用本机MAC地址
            mac_address = get_mac_address()
            print(f"使用本机MAC地址: {mac_address}")
            return extract_mac_suffix(mac_address)
        
        # 验证输入格式
        user_input = user_input.upper().replace(':', '').replace('-', '')
        if len(user_input) == 6 and all(c in '0123456789ABCDEF' for c in user_input):
            return user_input
        else:
            print("输入格式错误！请输入6位十六进制字符（如：A1B2C3）")


def main():
    """主函数"""
    print("=== 基于MAC地址的密码生成器 ===")
    print("支持两种模式：")
    print("1. 自动获取本机MAC地址")
    print("2. 手动输入设备MAC地址后6位")
    print()
    
    # 获取MAC地址后6位
    mac_suffix = get_user_mac_suffix()
    print(f"使用的MAC地址后6位: {mac_suffix}")
    
    # 生成密码
    password = generate_password(mac_suffix)
    print(f"生成的16位随机密码: {password}")
    
    return password


if __name__ == "__main__":
    main()
