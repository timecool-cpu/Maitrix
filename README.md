# Maitrix 数据处理项目

## 项目概述

这是一个用于处理多个数据源（BullX、Axiom、gmgn、photon）的数据处理项目。项目主要功能是计算用户的积分（points），基于用户的交易量（volume）和净盈亏（PnL）数据。

## 环境要求

- Python 3.x
- pandas
- openpyxl（用于Excel文件处理）

可以通过以下命令安装依赖：
```bash
pip install pandas openpyxl
```

## 文件结构

```
├── data/                  # 输入数据目录
│   ├── BullX.csv         # BullX平台数据
│   ├── Axiom.csv         # Axiom平台数据
│   ├── gmgn.csv          # gmgn平台数据
│   └── photon.csv        # photon平台数据
├── output/               # 输出结果目录
│   ├── BullX_point.xlsx  # BullX积分结果
│   ├── Axiom_point.xlsx  # Axiom积分结果
│   ├── gmgn_point.xlsx   # gmgn积分结果
│   └── photon_point.xlsx # photon积分结果
├── result/               # 最终合并结果目录
│   └── final_points.xlsx # 所有平台积分合并结果
├── BullX.py             # BullX数据处理脚本
├── Axiom.py             # Axiom数据处理脚本
├── gmgn.py              # gmgn数据处理脚本
├── photon.py            # photon数据处理脚本
├── BullX_point.py       # BullX积分计算脚本
├── Axiom_point.py       # Axiom积分计算脚本
├── gmgn_point.py        # gmgn积分计算脚本
├── photon_point.py      # photon积分计算脚本
└── merge_result.py      # 结果合并脚本
```

## 使用说明

### 数据要求

各平台的输入数据文件（CSV或Excel）必须包含以下列：

- BullX: address（钱包地址）, total_volume（交易量）, net_pnl（净盈亏）
- Axiom: wallet_address, total_volume, net_pnl
- gmgn: user（钱包地址）, totalVolumeUSD（交易量）, netPnLUSD（净盈亏）
- photon: user（钱包地址）, totalVolumeUSD（交易量）, netPnLUSD（净盈亏）

### 积分计算规则

积分计算采用以下公式：
```
point = ((VOLUME_WEIGHT * volume / VOLUME_DIVISOR) + 
         (PNL_WEIGHT * |net_pnl| / PNL_DIVISOR)) * POINT_MULTIPLIER + point_bonus
```

其中：
- VOLUME_WEIGHT = 0.6
- PNL_WEIGHT = 0.4
- VOLUME_DIVISOR = 46819347748.1
- PNL_DIVISOR = 6747073669.32
- POINT_MULTIPLIER = 5000000000
- point_bonus = 3229.08553589

### 运行步骤

1. 准备数据文件
   - 将各平台的数据文件放入 `data` 目录
   - 确保文件名和格式正确（.csv 或 .xlsx）

2. 运行积分计算脚本
   ```bash
   python BullX_point.py
   python Axiom_point.py
   python gmgn_point.py
   python photon_point.py
   ```

3. 查看结果
   - 处理后的结果将保存在 `output` 目录下
   - 每个文件包含 wallet_address（钱包地址）和 point（积分）两列

4. 合并结果
   ```bash
   python merge_result.py
   ```
   
5. 查看最终结果
   - 合并后的结果将保存在 `result` 目录下
   - 文件名为 final_points.xlsx

### 注意事项

- 只计算交易量大于 100.1 的用户数据
- 输入数据中的非数值或空值会被自动过滤
- 所有积分计算结果都会加上固定的 point_bonus
- 确保输入文件的列名与配置中的列名完全匹配
