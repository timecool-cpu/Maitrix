import pandas as pd
import os # 导入 os 模块用于检查文件是否存在

# --- 配置 ---
# <<< 重要：请设置这个路径 >>>
# 设置包含 'point' 列的 CSV 文件路径
input_csv_file = 'result/merged_wallets.csv' # 请修改为你的实际 CSV 文件路径

# 要计算总和的列名 (根据你的描述，应该是 'point')
point_column_name = 'point'
# --- 配置结束 ---

print("--- 开始计算 Point 总和脚本 (从 CSV 文件) ---")

# --- 检查文件是否存在 ---
if not os.path.exists(input_csv_file):
    print(f"错误：文件未找到: {input_csv_file}")
    print("请确保 'input_csv_file' 变量设置正确。")
    exit() # 停止脚本

# --- 读取并处理 CSV 文件 ---
try:
    print(f"正在读取 CSV 文件: {input_csv_file}")
    # 使用 pandas 读取 CSV 文件
    # 常见的可选参数：
    # sep=',' : 指定分隔符，默认是逗号，如果你的不是逗号（比如是制表符 '\t' 或分号 ';')，需要修改
    # encoding='utf-8' : 指定文件编码，'utf-8' 很常用，如果遇到编码错误可以尝试 'gbk' 或 'utf-8-sig'
    df = pd.read_csv(input_csv_file)
    print(f"成功读取文件，共有 {len(df)} 行数据。")

    # 检查 'point' 列是否存在
    if point_column_name in df.columns:
        print(f"正在计算 '{point_column_name}' 列的总和...")

        # 尝试将 'point' 列转换为数值类型，非数值会变成 NaN (Not a Number)
        # errors='coerce' 参数是关键，它使得无法转换的值变为 NaN 而不是报错
        numeric_points = pd.to_numeric(df[point_column_name], errors='coerce')

        # 检查是否有数据无法转换（可选但有用）
        invalid_count = numeric_points.isnull().sum()
        if invalid_count > 0:
            # 如果 point 列中存在非数字或空单元格，这里会给出提示
            print(f"警告：在 '{point_column_name}' 列中发现 {invalid_count} 个非数值或空值，这些值在求和时将被忽略。")

        # 计算总和 (pandas 的 sum() 方法默认会忽略 NaN 值)
        total_sum = numeric_points.sum()

        # 打印结果，使用 f-string 格式化输出
        print("-" * 20)
        # : ,.4f 表示使用千位分隔符，并保留 4 位小数
        print(f"'{point_column_name}' 列的总和为: {total_sum:,.4f}")
        print("-" * 20)

    else:
        # 如果列不存在，打印错误信息和可用的列名
        print(f"错误：文件中未找到名为 '{point_column_name}' 的列。")
        print(f"文件中可用的列有: {list(df.columns)}")

except FileNotFoundError:
    # 这个异常理论上被 os.path.exists 捕获了，但保留以防万一
    print(f"错误：无法找到文件 '{input_csv_file}'。")
except ImportError:
    # 虽然读 CSV 不直接需要 openpyxl 或 xlrd，但 pandas 仍然是必需的
    print("错误：缺少 pandas 库。请确保已安装 pandas。")
    print("运行: pip install pandas")
except pd.errors.EmptyDataError:
     print(f"错误：文件 '{input_csv_file}' 是空的。")
except Exception as e:
    # 捕获其他可能的错误，例如文件编码问题或权限问题
    print(f"处理文件时发生未知错误: {e}")
    # 如果遇到编码错误，可以尝试在 read_csv 中添加 encoding='utf-8' 或其他编码

print("--- 脚本执行完毕 ---")