---
name: trump-trades-squad
description: Trump policy & trades monitoring system — 7 agents: Policy Radar, Position Pool, Politician Tracker, Insider Monitor, Earnings Validator, Chase Risk Alert, and Night Watch Guard. Outputs a curated watchlist with cross-validated signals + overnight risk protection. Trigger on "run trump squad", "scan Trump trades", "check policy radar", "night watch", "update watchlist", "what should I buy based on Trump", or any request about Trump stock trades.
---

# TrumpTrades Squad

7 个 Agent 协同工作的美股跟单与政策监控系统——找机会 + 防风险。

## 使用方式

### 运行全部 Agent
```
run trump squad full scan
```
依次执行 Policy Radar → 标的池 → 政客追踪 → 内部人监控 → 财报验证 → 追高风险，输出精选标的池。

### 运行单个 Agent
```
run trump squad policy radar    # Agent 0: 政策雷达
run trump squad position pool   # Agent 1: 标的池
run trump squad politicians     # Agent 2: 政客追踪
run trump squad insiders        # Agent 3: 内部人监控
run trump squad earnings        # Agent 4: 财报验证
run trump squad chase risk      # Agent 5: 追高风险
```

### 交叉验证
```
run trump squad cross-validate NVDA
```
用 6 个 Agent 交叉验证单只标的。

## Agent 定义

所有 Agent 定义文件在 `agents/` 目录下。运行 Agent 时请 Read 对应的文件获取完整指令和数据源。

## 输出

精选标的池输出到 `signal-output/current-watchlist.md`。

## 策略衔接

精选标的池 → macro-regime-us-stocks/ Playbook 策略 → Bitget RWA 永续合约交易信号。
