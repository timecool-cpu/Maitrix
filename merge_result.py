import pandas as pd
import glob # 用于查找符合特定模式的文件路径
import os   # 用于处理文件和目录路径

# --- 配置 ---
# <<< 重要：请设置这些路径 >>>
# 1. 设置包含所有 Excel 文件的文件夹路径
#    例如：如果你的所有 Excel 文件都在一个名为 'data' 的文件夹里，就写 'data'
input_folder_path = 'output'  # 请修改此项为你实际的文件夹路径

# 2. 设置合并后输出的 Excel 文件路径和文件名
#    例如：如果你想把结果保存在 output 文件夹下的 merged_wallets.xlsx 文件中，就写 'output/merged_wallets.xlsx'
output_file_path_csv = 'result/merged_wallets.csv' # 请修改此项（可选，但建议指定一个输出文件路径）
# <<< 配置结束 >>>

print("--- 开始合并脚本 ---")

# --- 验证输入文件夹 ---
if not os.path.isdir(input_folder_path):
    print(f"错误：输入的文件夹未找到: {input_folder_path}")
    print("请确保 'input_folder_path' 变量设置正确，并且该文件夹存在。")
    exit() # 停止脚本执行

# --- 查找 Excel 文件 ---
# 使用 os.path.join 确保路径在不同操作系统下兼容
# 搜索指定文件夹下所有以 .xlsx 结尾的文件
search_pattern = os.path.join(input_folder_path, '*.xlsx')
excel_files = glob.glob(search_pattern)

if not excel_files:
    print(f"在指定的文件夹中未找到任何 .xlsx 文件: {input_folder_path}")
    print("请检查文件夹路径和文件扩展名是否正确。")
    exit() # 如果没有找到文件则停止

print(f"找到 {len(excel_files)} 个 Excel 文件准备处理:")
# 可选：打印找到的文件名以供确认
# for f in excel_files:
#    print(f"  - {os.path.basename(f)}")


# --- 读取文件并收集数据帧 ---
# 创建一个空列表用于存储从每个文件读取的数据帧 (DataFrame)
all_data_frames = []
# 我们期望每个文件中都包含的列名，用于验证和选取
expected_columns = ['wallet_address', 'point']

print("\n--- 正在读取文件 ---")
for file_path in excel_files:
    file_name = os.path.basename(file_path) # 获取文件名（不包含路径）
    print(f"正在处理文件: {file_name} ...")
    try:
        # 读取当前的 Excel 文件
        # 推荐使用 engine='openpyxl' 读取 .xlsx 文件
        df = pd.read_excel(file_path, engine='openpyxl')

        # 基本验证：检查必需的列是否存在于当前文件中
        # all() 检查 expected_columns 列表中的所有列名是否都在 df.columns 中
        if all(col in df.columns for col in expected_columns):
            # 如果列都存在，只选择期望的列并添加到列表中，以防文件中有额外的列
            all_data_frames.append(df[expected_columns])
            print(f"  > 读取成功 ({len(df)} 行数据).")
        else:
            # 如果缺少必需的列，找出缺少的列名并打印警告信息
            missing = [col for col in expected_columns if col not in df.columns]
            print(f"  > 警告：跳过文件 '{file_name}'。缺少必需的列: {missing}。找到的列有: {list(df.columns)}")

    except Exception as e:
        # 捕获读取文件时可能发生的其他错误（例如，文件格式问题，文件损坏等）
        print(f"  > 读取文件 '{file_name}' 时发生错误: {e}")
        print(f"  > 跳过此文件。")

# --- 合并数据 ---
if not all_data_frames:
    # 如果 all_data_frames 列表是空的，说明没有成功读取到任何有效数据
    print("\n--- 未能从 Excel 文件中读取到任何有效数据。---")
    print("不会创建合并后的文件。")
else:
    print(f"\n--- 正在合并来自 {len(all_data_frames)} 个有效文件的数据 ---")
    merged_df = pd.concat(all_data_frames, ignore_index=True)
    print(f"合并后的数据总共有: {len(merged_df)} 行。")

    # --- 准备输出目录 (如果需要) ---
    output_dir = os.path.dirname(output_file_path_csv)  # 使用 CSV 的路径
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"创建了输出目录: {output_dir}")
        except OSError as e:
            print(f"创建输出目录 '{output_dir}' 时发生错误: {e}")
            exit()

    # --- 保存合并后的数据到 CSV ---
    print(f"\n--- 正在保存合并后的数据 ---")
    print(f"数据量较大，将保存为 CSV 文件: {output_file_path_csv}")
    try:
        # 将合并后的数据帧保存到新的 CSV 文件
        # index=False 防止写入索引列
        # encoding='utf-8-sig' 推荐用于确保 Excel 正确识别 UTF-8 编码（特别是包含中文或特殊字符时）
        merged_df.to_csv(output_file_path_csv, index=False, encoding='utf-8-sig')
        print(f"成功将数据保存到 CSV 文件: {output_file_path_csv}")
    except Exception as e:
        print(f"保存 CSV 文件时发生错误: {e}")
        print("请检查文件路径、权限或是否有足够的磁盘空间。")

print("\n--- 合并脚本执行完毕 ---")