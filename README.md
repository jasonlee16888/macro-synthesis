# Macro Synthesis — 6-Agent Trump Policy Radar × AI Regime Rotation

> **Bitget Track 3 · US Stock AI Trading**
>
> 别人的策略告诉你"金叉买入"。我们的策略先告诉你"特朗普和国会议员在买什么"，
> 再用 6 个 AI Agent 交叉验证，最后用量化 regime 引擎告诉你什么时候进场、什么时候离场。

---

## 🏆 一句话

**Policy → Stocks → Timing → Execution. Afterbell protects your positions. We find them.**

---

## 🧠 系统架构

```
Truth Social · 白宫简报 · 行政令
              │
              ▼
┌──────────────────────────────────────────┐
│  Agent 0: 🔭 Policy Radar                 │
│  Trump 政策声明 → 映射到具体股票            │
├──────────────────────────────────────────┤
│  Agent 1: 📊 标的池管家                    │
│  Trump Q1 OGE 披露 — 3,642 笔交易          │
├──────────────────────────────────────────┤
│  Agent 2: 🏛️ 政客追踪                      │
│  国会议员实时交易披露（Quiver/Capitol Trades）│
├──────────────────────────────────────────┤
│  Agent 3: 🔍 内部人监控                     │
│  SEC Form 4 — CEO/CFO/董事大额买入          │
├──────────────────────────────────────────┤
│  Agent 4: 📈 财报验证                       │
│  SEC 财报 / 8-K / 分析师预期                │
├──────────────────────────────────────────┤
│  Agent 5: ⚠️ 追高风险警报                    │
│  涨幅 / 估值 / RSI / 关键价位               │
└──────────────────┬───────────────────────┘
                   │ 精选 3–5 只标的
                   ▼
┌──────────────────────────────────────────┐
│  🎯 3-Layer Regime Rotation Engine         │
│  波动率结构 + 趋势方向 + 动量持续性           │
│  → Hysteresis · Regime Memory · Rate Cycle │
│  → Bitget RWA USDT 永续合约交易信号         │
└──────────────────────────────────────────┘
```

---

## 🔭 Policy Radar（核心差异化武器）

| 日期 | 政策事件 | 映射标的 | 方向 |
|---|---|---|---|
| 6/18 | Trump Truth Social: Apple-Intel-Nvidia 芯片合作 | NVDA↑ INTC↑ AAPL↑ | 🟢 |
| 6/18 | Musk TerraFab 建厂获 Trump 力挺 | TSLA↑ INTC↑ | 🟢 |
| 6/16 | Intel 18A-P 风险试产 + 政府 9.9% 持股 | INTC↑ | 🟢 |
| 6/中旬 | Section 301 关税提案（60 国 12.5%） | 宏观↓ | 🔴 |
| 6/中旬 | 中国 125% 报复关税 + 稀土限制 | 芯片设备↓ | 🔴 |

---

## 📋 当前精选标的池（2026-06-25）

| 排名 | 标的 | 综合分 | Policy | Trump | 政客 | 内部人 | 财报 | 追高 | 信号 |
|---|---|---|---|---|---|---|---|---|---|
| 🥇 | **NVDA** 英伟达 | **0.87** | 0.9 | 1.0 | 1.0 | 0.5 | 1.0 | 0.6 | 🟢 LONG |
| 🥈 | **AAPL** 苹果 | **0.68** | 0.7 | 0.6 | 0.5 | 0.5 | 0.7 | 0.9 | 🟡 WATCH |
| 🥉 | **TSLA** 特斯拉 | **0.62** | 0.8 | 0.5 | 0.5 | 0.5 | 0.6 | 0.6 | 🟡 WATCH |

---

## 📊 回测证据

| 指标 | 数值 |
|---|---|
| 净利润 | **+$119.26**（2.5 个月） |
| 账户回报率 | **2.38%** |
| 年化回报率 | **~11.4%** |
| 夏普比率 | **1.79** |
| 胜率 | **100%** |
| 交易次数 | 3 |
| 标的 | AAPLUSDT |
| 回测窗口 | 2026-04-06 → 2026-06-24 |
| K 线 | 4h × 470 |

> Playbook 已发布至 GetAgent Studio。回测记录可在 Playbook run history 中验证。

---

## 📁 项目结构

```
macro-synthesis/
├── README.md                         ← 本文
├── demo/
│   └── index.html                    ← 展示页面
├── trump-trades-squad/               ← 6 Agent 选股系统
│   ├── SKILL.md                      ← Claude Code 可运行 skill
│   ├── agents/
│   │   ├── policy-radar.md           ← Agent 0: 政策雷达
│   │   ├── position-pool.md          ← Agent 1: 标的池
│   │   ├── politician-tracker.md     ← Agent 2: 政客追踪
│   │   ├── insider-monitor.md        ← Agent 3: 内部人
│   │   ├── earnings-validator.md     ← Agent 4: 财报
│   │   └── chase-risk-alert.md       ← Agent 5: 追高风险
│   └── signal-output/
│       └── current-watchlist.md      ← 当前精选标的池
├── macro-regime-us-stocks/           ← GetAgent Playbook 策略
│   ├── manifest.yaml
│   ├── backtest.yaml
│   ├── src/
│   │   ├── strategy.py               ← 3-Layer Regime Rotation
│   │   ├── main.py
│   │   └── rate_regime.py            ← FRED 利率周期感知
│   └── README.md
└── paper-trading-log.md              ← 模拟交易记录
```

---

## 🔗 链接

- **Live Demo**: [demo/index.html](demo/index.html)
- **GetAgent Playbook**: `c06c60dd-3fbe-4b97-bb84-9a1e03d52051` @ Bitget Studio
- **TrumpTrades Dashboard**: http://trumpdash-bi5bu2dn.manus.space

---

## ⚠️ 风险声明

- 研究支持用途。不构成投资建议。
- 特朗普 OGE 披露有 45 天报告延迟。
- RWA 美股永续合约交易历史有限（<1 年）。
- 过往回测表现不代表未来实盘收益。
- 仅投入可承受亏损的资本。

---

## 📄 致谢

- 供应链分析方法论受 @aleabitoreddit 公开投研风格启发
- TrumpTrades 数据可视化来自 http://trumpdash-bi5bu2dn.manus.space
- Quiver Quantitative / Capitol Trades 提供政客交易数据
- SEC EDGAR 提供内部人交易和财报数据
