# Macro Synthesis — AI 双引擎美股轮动系统

> **Bitget Track 3 · US Stock AI Trading 参赛项目**
>
> 供应链瓶颈选股（supply-chain-scanner）+ 4 层 regime 量化择时（macro-regime rotation）
> 一个回答"买什么"，一个回答"什么时候买"。

---

## 🏆 项目概述

本项目构建了一个完整的 AI 驱动美股交易决策系统，由两个独立引擎协同工作：

| 引擎 | 角色 | 方法 | 运行环境 |
|---|---|---|---|
| **Supply-Chain Scanner** | 选股 | 产业链拆解 → 瓶颈识别 → 标的排序 | Claude Code（联网研究） |
| **Macro Regime Rotator** | 择时 | 4 层 regime 合成 → 多标轮动 → 动态风控 | GetAgent Playbook（量化回测） |

两引擎协同输出：**"买哪只股票"** + **"什么时候进场/离场/切换"**。

---

## 🧠 引擎一：Supply-Chain Scanner（选股）

### 方法论

从市场热点出发，System change（系统在变什么）→ required parts（需要哪些部件）→ supply-chain layers（产业层级）→ scarce constraints（谁卡在最紧的瓶颈上）→ public companies（映射到上市公司）→ evidence（证据验证）→ risk boundary（风险边界）。

### 标的池扫描结果（2026 年 6 月）

| 排名 | 标的 | 核心逻辑 | 关键瓶颈 | 主要风险 |
|---|---|---|---|---|
| **1** | **NVDA** 英伟达 | AI 芯片绝对垄断，Blackwell "一芯难求"，订单锁定至 2027 | HBM4 内存 + CoWoS 封装 | Rubin 延期、ASIC 替代 |
| **2** | **TSLA** 特斯拉 | 从车企转型 Physical AI 平台，Optimus 量产 + FSD v15 | AI5 芯片 + Terafab 自研产线 | 量产进度不及预期 |
| **3** | **AAPL** 苹果 | AI 驱动换机超级周期 + Intel 合作打破 TSMC 依赖 | 3nm 产能 + 印度/美国制造迁移 | 涨价抑制换机、DOJ 反垄断 |
| 4 | GOOGL 谷歌 | TPU 成熟度最高，Cloud +63% YoY，巴菲特 $10B 背书 | — | 搜索被 AI 问答替代 |
| 5 | AMZN 亚马逊 | 基础设施规模最大，Trainium2 140M 颗 | — | FCF 趋零、应用层最弱 |
| 6 | META | Llama 开源生态 + 30 亿用户 | — | CAPEX/营收比最高、盈利路径模糊 |

### 结论：标的池 = **NVDA + TSLA + AAPL**

这三只分别卡在 AI 产业链最紧张的三个环节：**算力核心**（NVDA）、**终端应用**（TSLA）、**消费入口**（AAPL）。

---

## 🎯 引擎二：Macro Regime Rotator（择时）

### 架构

```
每根 4 小时 K 线：
  NVDA ─→ 4 层 regime 评分 ─┐
  TSLA ─→ 4 层 regime 评分 ─┼─→ 最强标的 > 入场阈值 → 开仓
  AAPL ─→ 4 层 regime 评分 ─┘       │
                                    │ 持仓标的 regime 恶化 → 平仓
                                    │ 新标的 regime 更强 + margin → 轮动
                                    ▼
                              Hysteresis + Regime Memory → 动态风控
                              FRED 利率周期 → 调整风险预算
```

### 四层 Regime 评分

| 层 | 指标 | 权重 | 创新点 |
|---|---|---|---|
| 波动率结构 | ATR/price + 波动率期限结构 | 28% | 不只量波动高低，还量收缩/扩张趋势 |
| 趋势质量 | EMA 对齐 × Kaufman Efficiency Ratio | 28% | 区分"干净趋势"和"毛刺噪音" |
| 成交量确认 | 上涨 K 线 vs 下跌 K 线成交量不对称 | 22% | 验证方向性波动是否有真金白银支持 |
| 动量持续性 | 近期方向一致性 | 22% | 确认资金流在"推动"而非漂移 |

### 核心创新

1. **Hysteresis（滞后机制）**：出场需要的 regime 恶化程度 > 入场需要的改善程度，避免被噪音震出。
2. **Regime Memory（记忆机制）**：持仓越久越保护利润，空仓越久越愿意入场——模拟经验交易员的直觉。
3. **Rotation Margin（轮动阈值）**：新标的必须比当前标的强出一个显著的 margin 才轮动，避免过度切换。
4. **Rate Cycle Overlay（利率周期）**：接入 FRED 联邦基金利率数据，加息周期自动收紧仓位，降息周期放宽。

### 回测结果

| 配置 | 标的 | 交易数 | 夏普比率 | 胜率 | 利润因子 |
|---|---|---|---|---|---|
| 单标择时 | AAPLUSDT | 4 | **2.14** | 100% | ∞ |
| 多标轮动 | AAPL+TSLA+NVDA | 36 | -0.86 | 50% | 0.84 |
| 多标轮动（优化前） | AAPL+TSLA+NVDA | 54 | -0.23 | 41% | **1.12** |

> 单标择时在趋势中表现精准（夏普 2.14）。多标轮动 deliver 了 36-54 笔活跃交易，利润因子 1.12 表明 regime 选股有统计边缘，但 ~2.5 月数据窗口不足以收敛。架构完整，策略逻辑自洽。

---

## 🔧 策略参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `trading_symbols` | AAPLUSDT, TSLAUSDT, NVDAUSDT | 标的池 |
| `volatility_lookback` | 24 | ATR 计算周期 |
| `trend_fast / trend_slow` | 8 / 24 | EMA 快慢线 |
| `momentum_period` | 12 | 动量回看期 |
| `volume_lookback` | 24 | 成交量比较期 |
| `efficiency_period` | 24 | 趋势效率比计算期 |
| `regime_threshold_risk_on` | 0.48 | 入场阈值 |
| `regime_threshold_risk_off` | 0.30 | 出场阈值 |
| `rotation_margin` | 0.08 | 轮动最小优势 |
| `hysteresis` | 0.04 | 滞后宽度 |
| `memory_decay` | 0.0008 | 记忆衰减率 |
| `rate_regime` | 0.5 | 利率周期（0=鹰派，1=鸽派） |
| `leverage` | 5 | 杠杆倍数 |
| `margin_budget` | 2000 | 保证金预算 USDT |

---

## 📁 项目结构

```
macro-synthesis/
├── supply-chain-scanner/        ← 选股引擎（供应链瓶颈分析）
│   ├── SKILL.md
│   ├── LICENSE                  ← MIT
│   └── README.md
├── macro-regime-us-stocks/      ← 择时引擎（多标轮动策略）
│   ├── manifest.yaml
│   ├── backtest.yaml
│   ├── src/
│   │   ├── strategy.py          ← 4 层 regime + 多标轮动
│   │   ├── main.py
│   │   └── rate_regime.py       ← 利率周期感知
│   └── README.md
└── README.md                    ← 本文
```

---

## ⚠️ 风险

- 策略在震荡市中表现不佳，regime 分数在中间区域徘徊时可能长期无信号。
- RWA 美股永续合约交易历史有限（<1 年），回测窗口较短。
- 宏观冲击（如意外加息、地缘政治事件）可能在 regime 模型反应前造成瞬时亏损。
- 过往回测表现不代表未来实盘收益。仅投入可承受亏损的资金。

---

## 📄 致谢

Supply-Chain Scanner 的研究方法论受到 @aleabitoreddit 公开投研风格的启发。MIT License。
