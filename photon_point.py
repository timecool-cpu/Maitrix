import pandas as pd

# --- 配置 ---
# 输入文件路径 (可以是 .xlsx 或 .csv)
input_file_path = 'data/photon.csv'
# 输出文件路径 (将保存结果的 Excel 文件名)
output_file_path = 'output/photon_point.xlsx'

# --- 列名配置 ---
# !! 请确保这些名称与你的 Excel/CSV 文件中的列标题完全匹配 !!
wallet_column = 'user'
volume_column = 'totalVolumeUSD'
pnl_column = 'netPnLUSD'
# --- 列名配置结束 ---

# --- 计算规则参数 ---
volume_threshold = 100.1 # 只计算 total_volume 大于此值的数据
VOLUME_WEIGHT = 0.6
PNL_WEIGHT = 0.4
VOLUME_DIVISOR = 46819347748.1
PNL_DIVISOR = 6747073669.32
POINT_MULTIPLIER = 5000000000
point_bonus = 3229.08553589
# --- 计算规则参数结束 ---

print("--- 开始处理脚本 ---")

try:
    # 1. 读取输入文件
    print(f"正在读取文件: {input_file_path}")
    if input_file_path.lower().endswith('.xlsx'):
        df = pd.read_excel(input_file_path, engine='openpyxl')
    elif input_file_path.lower().endswith('.csv'):
        df = pd.read_csv(input_file_path)
    else:
        print(f"错误：不支持的文件格式: {input_file_path}. 请提供 .xlsx 或 .csv 文件。")
        exit() # 退出程序

    print(f"成功读取文件，原始数据共有 {len(df)} 行。")

    # 2. 检查必要的列是否存在
    required_columns = [wallet_column, volume_column, pnl_column]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"错误：文件中缺少必要的列: {', '.join(missing_columns)}")
        print(f"可用的列: {list(df.columns)}")
        exit()
    print("所有必需的列都存在。")

    # 3. 数据类型转换与清洗
    print(f"正在将 '{volume_column}' 和 '{pnl_column}' 列转换为数值类型...")
    df[volume_column] = pd.to_numeric(df[volume_column], errors='coerce') # errors='coerce' 会将无法转换的值变为 NaN
    df[pnl_column] = pd.to_numeric(df[pnl_column], errors='coerce')

    # 移除包含 NaN 的行 (转换失败或原本为空)
    initial_rows = len(df)
    df.dropna(subset=[volume_column, pnl_column], inplace=True)
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        print(f"警告：移除了 {rows_dropped} 行，因为 '{volume_column}' 或 '{pnl_column}' 包含非数值数据或为空。")
    print(f"数据清洗后剩下 {len(df)} 行。")

    # 4. 筛选数据：total_volume > volume_threshold
    print(f"正在筛选 '{volume_column}' 大于 {volume_threshold} 的行...")
    filtered_df = df[df[volume_column] > volume_threshold].copy() # 使用 .copy() 避免 SettingWithCopyWarning
    print(f"筛选后剩下 {len(filtered_df)} 行符合条件。")

    # 5. 计算 point 分数 (如果筛选后有数据)
    if not filtered_df.empty:
        print("正在为符合条件的行计算 point 分数...")

        # 应用计算公式 (Pandas 的向量化操作，比逐行循环快得多)
        # 注意 .abs() 用于获取 net_pnl 的绝对值
        filtered_df['point'] = (
            (VOLUME_WEIGHT * filtered_df[volume_column] / VOLUME_DIVISOR) +
            (PNL_WEIGHT * filtered_df[pnl_column].abs() / PNL_DIVISOR)
        ) * POINT_MULTIPLIER

        print("Point 分数计算完成。")

        # 6. 创建输出 DataFrame (只包含 wallet_address 和 point)
        output_df = filtered_df[[wallet_column, 'point']].copy()
        output_df.rename(columns={wallet_column: 'wallet_address'}, inplace=True)
        output_df['point'] = output_df['point'] + point_bonus

        # 7. 保存结果到新的 Excel 文件
        print(f"正在将结果保存到: {output_file_path}")
        # index=False 表示不将 DataFrame 的索引写入 Excel 文件
        output_df.to_excel(output_file_path, index=False, engine='openpyxl')
        print("结果已成功保存。")

        # (可选) 打印输出结果的前几行看看
        print("\n--- 输出结果预览 (前 5 行) ---")
        print(output_df.head())
        print("--- --- ---")

    else:
        print("警告：没有数据行符合筛选条件 (total_volume > 100.1)，因此未生成输出文件。")

except FileNotFoundError:
    print(f"错误：文件未找到，请检查路径 '{input_file_path}' 是否正确。")
except Exception as e:
    print(f"处理文件时发生未知错误: {e}")
    # 如果需要更详细的错误信息进行调试，可以取消下面两行的注释
    # import traceback
    # traceback.print_exc()

print("--- 脚本执行完毕 ---")