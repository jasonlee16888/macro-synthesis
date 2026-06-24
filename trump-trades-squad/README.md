# TrumpTrades 多 Agent 美股跟单小队

> 5 个独立 Agent 协同工作，把 TrumpTrades 静态数据库变成一个会自动更新、自动交叉验证、自动提醒风险的美股观察系统。

---

## 架构

```
TrumpTrades Dashboard (Q1 2026 种子池, 3,642 笔交易)
              │
              ▼
┌─────────────────────────────────────────┐
│  Agent 1: 标的池管家                      │
│  Trump Q1 行业分布 + Top 标的 + 方向频率    │
│  源: trumpstrades.com, capitoltrades.com  │
├─────────────────────────────────────────┤
│  Agent 2: 政客交易追踪器                    │
│  国会议员 / 政治资金最新买入                 │
│  源: Quiver Quantitative, Capitol Trades  │
├─────────────────────────────────────────┤
│  Agent 3: 内部人监控器                      │
│  CEO/CFO/董事大额买入 & 集体买入             │
│  源: OpenInsider, SEC Form 4              │
├─────────────────────────────────────────┤
│  Agent 4: 财报验证器                        │
│  财报/8-K/电话会 → 基本面支撑               │
│  源: SEC EDGAR, analyst estimates         │
├─────────────────────────────────────────┤
│  Agent 5: 追高风险警报                      │
│  涨幅/估值/成交量/关键价位 → 不适合追的标志    │
│  源: Finviz, TradingView                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         精选标的池 (3-5 只，动态更新)
                   │
                   ▼
     GetAgent Playbook — 4 层 regime 量化择时
```

---

## 使用方式

### 手动运行全部 5 个 Agent

在 Claude Code 中发送：
```
运行 trump-trades-squad 全部 5 个 Agent，输出当前精选标的池
```

### 运行单个 Agent

```
运行 Agent 3（内部人监控器），只看最近 7 天的 CEO/CFO 大额买入
```

### 定时自动运行（推荐）

```
设置每天早上 9:00 自动运行 Agent 2 + Agent 3，有异常时提醒我
```

---

## Agent 说明

| Agent | 职责 | 更新频率 | 关键数据源 |
|---|---|---|---|
| [Agent 1](agents/position-pool.md) | 标的池管家 | 每周（Q1 种子池稳定） | trumpstrades.com, capitoltrades.com |
| [Agent 2](agents/politician-tracker.md) | 政客交易追踪 | 每日 | Quiver Quantitative, Capitol Trades |
| [Agent 3](agents/insider-monitor.md) | 内部人监控 | 每日 | OpenInsider, SEC Form 4 |
| [Agent 4](agents/earnings-validator.md) | 财报验证 | 每周（财报季每日） | SEC EDGAR, analyst estimates |
| [Agent 5](agents/chase-risk-alert.md) | 追高风险警报 | 每日 | Finviz, TradingView |

---

## 信号优先级

每只候选标的由 5 个 Agent 独立打分（0-1），加权合成综合信号：

| 信号来源 | 权重 | 含义 |
|---|---|---|
| Trump 持仓 | 30% | 总统实际资金布局 |
| 政客跟单 | 20% | 国会信息优势 |
| 内部人买入 | 25% | 管理层信心 |
| 财报支撑 | 15% | 基本面验证 |
| 追高风险 | 10%（负向） | 过热警告 |

**精选标的池 = 综合得分 Top 3-5**

---

## 当前精选标的池

见 [signal-output/current-watchlist.md](signal-output/current-watchlist.md)

---

## 风险声明

研究支持用途。不构成投资建议。特朗普持仓数据来自公开的 OGE Form 278-T 披露，存在 45 天报告延迟。历史表现不代表未来收益。
