import pandas as pd

# --- 配置 ---
# 将 'your_file_v2.xlsx' 替换成你的实际文件名 (可以是 .xlsx 或 .csv)
file_path = 'data/gmgn.csv'
# 或者 file_path = 'your_file_v2.csv'

# --- 列名配置 ---
# 根据你的 Excel 文件，确认这些列名是正确的
volume_column = 'totalVolumeUSD'
pnl_column = 'netPnLUSD'
# --- 列名配置结束 ---

volume_threshold = 100.1 # totalVolumeUSD 的阈值
# --- 配置结束 ---

total_net_pnl = 0.0
total_total_volume = 0.0
try:
    # 根据文件扩展名选择读取函数
    if file_path.lower().endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        print(f"错误：不支持的文件格式: {file_path}. 请提供 .xlsx 或 .csv 文件。")
        exit() # 退出程序

    print(f"成功读取文件: {file_path}")
    print(f"原始数据共有 {len(df)} 行。")

    # 检查必要的列是否存在
    required_columns = [volume_column, pnl_column]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"错误：文件中缺少必要的列: {', '.join(missing_columns)}")
        print(f"可用的列: {list(df.columns)}")
        exit()

    # 确保相关列是数值类型
    df[volume_column] = pd.to_numeric(df[volume_column], errors='coerce')
    df[pnl_column] = pd.to_numeric(df[pnl_column], errors='coerce')

    # 移除相关列中转换失败(值为NaN)的行
    initial_rows = len(df)
    df.dropna(subset=[volume_column, pnl_column], inplace=True)
    if initial_rows > len(df):
        print(f"警告：移除了 {initial_rows - len(df)} 行，因为 '{volume_column}' 或 '{pnl_column}' 包含非数值数据。")

    # 筛选：选择 volume_column 大于等于阈值的行
    filtered_df = df[df[volume_column] > volume_threshold].copy()

    print(f"筛选后剩下 {len(filtered_df)} 行 ({volume_column} >= {volume_threshold})。")

    # 计算筛选后数据的总和
    if not filtered_df.empty:
        # --- 修改点：计算 PnL 列的绝对值之和 ---
        total_absolute_net_pnl = filtered_df[pnl_column].abs().sum()
        # -----------------------------------------
        total_total_volume = filtered_df[volume_column].sum() # Total Volume 计算不变
    else:
        print("警告：筛选后没有符合条件的数据行。")
        total_absolute_net_pnl = 0.0
        total_total_volume = 0.0

    # 打印结果，格式化为两位小数
    print("\n--- 统计结果 ---")
    # 更新打印标签以反映计算的是绝对值之和
    print(f"符合条件的地址总 {pnl_column} (绝对值之和): {total_absolute_net_pnl:,.2f}")
    print(f"符合条件的地址总 {volume_column}: {total_total_volume:,.2f}")

except FileNotFoundError:
    print(f"错误：文件未找到，请检查路径 '{file_path}' 是否正确。")
except Exception as e:
    print(f"处理文件时发生未知错误: {e}")
    # 如果需要更详细的错误信息，可以取消下面两行的注释
    # import traceback
    # traceback.print_exc()