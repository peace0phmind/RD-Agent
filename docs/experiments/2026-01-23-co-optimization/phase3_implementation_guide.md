# Phase 3 实施指南

**目标**: 解决IC高但收益低的问题
**预计时间**: 2-3小时
**难度**: 中等（需要修改配置和代码）

---

## 方案概述

基于深度分析，问题的根本原因是：

```
Risk_Adj_Momentum = Return / Volatility
                      ↑
                 除以波动率导致：
                 - 高波动股票（高收益）被过滤
                 - 选出低波动、低收益的股票
                 - IC高（排序对）但收益低
```

**解决策略**: 修改因子公式、损失函数和仓位管理

---

## 实施步骤

### 步骤1: 创建优化因子（15分钟）

#### 1.1 创建因子文件

创建 `rdagent/scenarios/qlib/factor_custom.py`:

```python
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.strategy import TopkDropoutStrategy

def calculate_momentum_moderate_risk(df, window=20, penalty_factor=0.3):
    """
    优化版风险调整动量

    Args:
        df: 包含$close的数据
        window: 时间窗口（默认20日）
        penalty_factor: 波动率惩罚系数（0-1，默认0.3）

    Returns:
        Series: 因子值
    """
    # 计算动量
    momentum = (df['$close'] - df['$close'].shift(window)) / df['$close'].shift(window)

    # 计算波动率
    returns = df['$close'].pct_change()
    volatility = returns.rolling(window).std()

    # 计算波动率排名（相对值）
    vol_rank = volatility.rolling(window*3).rank(pct=True)

    # 优化版：减少惩罚而非除法
    factor = momentum * (1 - penalty_factor * vol_rank)

    return factor

# Qlib因子接口
class MomentumModerateRisk:
    """优化版风险调整动量因子"""

    def __init__(self, window=20, penalty_factor=0.3):
        self.window = window
        self.penalty_factor = penalty_factor

    def __call__(self, df):
        return calculate_momentum_moderate_risk(
            df,
            window=self.window,
            penalty_factor=self.penalty_factor
        )
```

#### 1.2 注册因子

修改 `rdagent/scenarios/qlib/__init__.py`，添加：

```python
from .factor_custom import MomentumModerateRisk

# 在factor_registry中添加
FACTOR_REGISTRY['momentum_moderate_risk'] = MomentumModerateRisk
```

---

### 步骤2: 修改损失函数（30分钟）

#### 2.1 创建自定义损失函数

创建 `rdagent/scenarios/qlib/loss_return.py`:

```python
import torch
import torch.nn as nn

class ReturnOptimizedLoss(nn.Module):
    """
    直接优化收益的损失函数

    原版: IC = corr(rank(pred), rank(return))
    改进: Loss = -Σ(position * return) + penalties
    """

    def __init__(self, turnover_penalty=0.01, concentration_penalty=0.01):
        super().__init__()
        self.turnover_penalty = turnover_penalty
        self.concentration_penalty = concentration_penalty

    def forward(self, pred, target):
        """
        Args:
            pred: 模型预测值 (batch_size, n_stocks)
            target: 真实收益 (batch_size, n_stocks)
        """
        # 将预测值转换为仓位（Top 20%）
        # pred_rank = pred.argsort(dim=1).argsort(dim=1)
        # position = (pred_rank >= pred.shape[1] * 0.8).float()

        # 简化：直接使用预测值的softmax作为仓位
        position = torch.softmax(pred * 2, dim=1)  # 温度参数2，增加区分度

        # 计算portfolio return
        portfolio_return = (position * target).mean(dim=1)

        # 换手率惩罚（简化版）
        turnover_penalty = 0  # 需要前一期的仓位

        # 集中度惩罚（避免过度集中）
        concentration_penalty = (position ** 2).mean(dim=1)

        # 总损失 = -收益 + 惩罚
        loss = -portfolio_return.mean() + \
                self.concentration_penalty * concentration_penalty.mean()

        return loss
```

#### 2.2 修改RD-Agent配置

创建 `rdagent/app/qlib_rd_loop/conf_phase3_custom.yaml`:

```yaml
# Phase 3: 自定义损失函数配置

experiment:
  name: "phase3_return_optimization"
  description: "Optimize returns directly instead of IC"

# 损失函数配置
loss_function:
  type: "return_optimized"
  class: "ReturnOptimizedLoss"
  module: "rdagent.scenarios.qlib.loss_return"

  # 损失函数参数
  turnover_penalty: 0.01
  concentration_penalty: 0.01

# 模型配置
model:
  type: "lightgbm"
  class: "LGBModel"

  # 关键修改：使用自定义损失
  objective: "regression"
  # 注意: LightGBM可能需要自定义objective
  # 或者使用wrapper在训练时应用自定义损失

  # 超参数
  learning_rate: 0.03
  num_leaves: 63
  max_depth: 7
  feature_fraction: 0.8
  bagging_fraction: 0.8
  bagging_freq: 5

# 因子配置
factors:
  - name: "momentum_moderate_risk"
    class: "MomentumModerateRisk"
    window: 20
    penalty_factor: 0.3

# 执行器配置
executor:
  type: "port_exec"
  class: "port_executor"

  # 仓位管理配置
  target_position: 0.8  # 目标暴露度80%（vs 原来的30-40%）

  # 交易策略
  strategy:
    type: "TopkDropoutStrategy"
    topk: 0.2  # 只做多Top 20%
    n_drop: 5  # 每次换仓时避免N个最相似的股票

  # 风险管理
  risk_control:
    max_drawdown: 0.10  # 最大回撤10%
    stop_loss: 0.05     # 止损5%
```

---

### 步骤3: 运行优化回测（20分钟）

#### 3.1 创建执行脚本

创建 `run_phase3_backtest.sh`:

```bash
#!/bin/bash
# Phase 3 优化回测

echo "=========================================="
echo "Phase 3: 优化策略回测"
echo "=========================================="

# 激活环境
source ~/conda/etc/profile.d/conda.sh
conda activate quant

# 方法A: 使用RD-Agent自定义配置（如果支持）
rdagent fin_model \
  --loop-n 1 \
  --config rdagent/app/qlib_rd_loop/conf_phase3_custom.yaml

# 方法B: 直接用Qlib API
python -c "
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord

# 定义工作流
workflow = R(
    experiment_id='phase3_optimization',
    executor={
        'class': 'port_executor',
        'module_path': 'qlib.contrib.evaluate.strategy.executor',
        'kwargs': {
            'time_series': '2020-01-01 2020-12-31',
            'generator': {
                'class': 'TopkDropoutStrategy',
                'module_path': 'qlib.contrib.strategy.signal_strategy',
                'kwargs': {
                    'signal': '<PRED>',
                    'topk': 0.2,
                    'n_drop': 5,
                }
            }
        }
    }
)

# 运行回测
workflow.generate()

# 分析结果
print('Phase 3 回测完成！')
"

echo "回测完成！结果保存在: mlruns/..."
```

#### 3.2 提取和对比结果

创建 `analyze_phase3_results.py`:

```python
import pandas as pd
import pickle

def analyze_results():
    """分析Phase 3结果并与baseline对比"""

    print("="*80)
    print("Phase 3 结果分析")
    print("="*80)

    # Baseline结果（Phase 1 Loop 3）
    baseline = {
        'IC': 0.104,
        'Return': -2.42,
        'Drawdown': 0.00,
    }

    # Phase 3结果（从回测文件中提取）
    # TODO: 实际执行后填充
    phase3 = {
        'IC': 'PENDING',
        'Return': 'PENDING',
        'Drawdown': 'PENDING',
    }

    # 对比表
    comparison = pd.DataFrame({
        'Metric': ['IC', 'Ann Return (%)', 'Max Drawdown (%)'],
        'Baseline': [baseline['IC'], baseline['Return'], baseline['Drawdown']],
        'Phase 3': [phase3['IC'], phase3['Return'], phase3['Drawdown']],
        'Improvement': [
            f"{(phase3['IC'] - baseline['IC']) / baseline['IC'] * 100:+.1f}%",
            f"{phase3['Return'] - baseline['Return']:+.2f}%",
            f"{phase3['Drawdown'] - baseline['Drawdown']:+.2f}%"
        ]
    })

    print("\n结果对比:")
    print(comparison)

    print("\n预期改善:")
    print("  IC: 0.104 → 0.09-0.10 (略降，可接受)")
    print("  Return: -2.42% → > 0% (转正)")
    print("  Drawdown: 0% → 5-10% (合理风险)")

if __name__ == "__main__":
    analyze_results()
```

---

## 步骤4: 验证和调试（30分钟）

### 4.1 检查清单

运行以下检查：

```bash
# 1. 检查因子计算
python -c "
from rdagent.scenarios.qlib.factor_custom import MomentumModerateRisk
import pandas as pd

# 测试因子
df = pd.read_hdf('data.h5')
factor_calculator = MomentumModerateRisk()
factor_values = factor_calculator(df)

print('因子计算成功！')
print(f'均值: {factor_values.mean():.6f}')
print(f'标准差: {factor_values.std():.6f}')
"

# 2. 检查损失函数
python -c "
from rdagent.scenarios.qlib.loss_return import ReturnOptimizedLoss
import torch

# 测试损失函数
loss_fn = ReturnOptimizedLoss()
pred = torch.randn(10, 100)
target = torch.randn(10, 100) * 0.02

loss = loss_fn(pred, target)
print(f'Loss: {loss.item():.6f}')
print('损失函数正常！')
"

# 3. 小规模回测测试
python -m qlib.workflow.R \
  experiment_id=phase3_test \
  executor_config='test_config.yaml'
```

### 4.2 常见问题排查

**问题1**: 因子计算错误
```bash
# 检查因子分布
python -c "
import pandas as pd
factor = pd.read_hdf('result.h5')
print(factor.describe())
print('\n检查是否有NaN:', factor.isna().sum())
print('检查是否有Inf:', (factor.abs() == float('inf')).sum())
"
```

**问题2**: 损失函数不收敛
```bash
# 调整学习率
# 在配置文件中修改 learning_rate: 0.03 → 0.01

# 添加梯度裁剪
# 在训练代码中添加
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

**问题3**: 回测失败
```bash
# 检查Qlib版本
python -c "import qlib; print(qlib.__version__)"

# 检查数据完整性
python -m qlib.cli.data get_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

---

## 预期结果

### 成功标准

| 指标 | Baseline | Phase 3目标 | 改善 |
|------|----------|-------------|------|
| IC | 0.104 | > 0.09 | -10%可接受 |
| 年化收益 | -2.42% | **> 0%** | **转正** |
| 最大回撤 | 0.00% | 5-10% | 合理风险 |

### 如果未达目标

**调试方案**:

1. **如果收益仍为负**:
   - 进一步降低penalty_factor (0.3 → 0.1)
   - 提高target_position (0.8 → 1.0)
   - 或者完全移除波动率惩罚

2. **如果回撤过大**:
   - 降低target_position
   - 增加stop_loss阈值
   - 提高topk阈值（0.2 → 0.15）

3. **如果IC下降太多**:
   - 混合原版和优化版因子
   - 因子权重: 0.7 * 新版 + 0.3 * 旧版

---

## 快速开始（最简化版本）

如果上述步骤太复杂，可以先用最简单的方式验证：

```python
# quick_test_phase3.py

from qlib.data import D
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.strategy import TopkDropoutStrategy

# 1. 准备数据
ds = D.features(['$close', '$volume'], start_time='2017-01-01', end_time='2020-12-31')

# 2. 计算优化因子
def calc_moderate_risk_factor(df):
    momentum = df['$close'].pct_change(20)
    vol = df['$close'].pct_change().rolling(20).std()
    vol_rank = vol.rolling(60).rank(pct=True)
    return momentum * (1 - 0.3 * vol_rank)

factor = calc_moderate_risk_factor(ds)

# 3. 创建预测（使用因子本身作为预测）
pred = factor

# 4. 回测
strategy = TopkDropoutStrategy(
    signal=pred,
    topk=0.2,
    n_drop=5,
    risk_degree=0.8  # 80%暴露度
)

# 5. 运行
portfolio = strategy()
analysis = risk_analysis(portfolio)

print("IC:", analysis['ic'])
print("年化收益:", analysis['annual_return'] * 100, "%")
print("最大回撤:", analysis['max_drawdown'] * 100, "%")
```

运行：
```bash
python quick_test_phase3.py
```

---

## 下一步

实施完成后：

1. **分析结果** - 对比Phase 1和Phase 3
2. **记录发现** - 更新lessons_learned.md
3. **决定方向** -
   - 如果成功：部署或进一步优化
   - 如果失败：分析原因，尝试其他方案

---

*创建时间: 2026-01-23 23:15*
*预计完成时间: 2-3小时*
*难度: 中等*
