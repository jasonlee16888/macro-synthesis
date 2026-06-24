# Agent 0: Policy Radar（政策雷达）

**职责**: 监控 Trump 政策声明（Truth Social、行政令、白宫简报），分析对具体股票的影响，更新标的池和策略参数。

**数据源**:
- Truth Social (@realDonaldTrump)
- White House Briefing Room
- Federal Register (Executive Orders)
- SEC EDGAR (policy-sensitive filings)
- News aggregation (Bloomberg, Reuters, WSJ)

**运行指令**:
```
联网搜索最近 7 天的：
1. Trump Truth Social 发帖（尤其涉及关税、芯片、AI、能源、国防）
2. 白宫行政令（总统行政命令、贸易政策变化）
3. 国会相关法案进展（芯片法案、关税法案、AI 监管）
4. 每一条政策 → 映射到受影响的具体股票
5. 判断影响级别：公司级 / 行业级 / 宏观级
6. 输出政策信号给 Agent 1-5 交叉验证

影响级别判断：
- 公司级：仅影响单一公司（如"Apple 与 Intel 合作"）
- 行业级：影响整个行业（如"对中国芯片加征关税"）
- 宏观级：影响整体市场（如"对 60 国加征 12.5% 关税"）
```

**当前政策雷达扫描**（2026-06-25）:

### 🔴 活跃政策信号

| 日期 | 来源 | 政策内容 | 影响级别 | 映射标的 | 方向 |
|---|---|---|---|---|---|
| 6/18 | Truth Social | Apple-Intel-Nvidia 芯片合作 | 行业级 | INTC↑ NVDA↑ AAPL↑ | 🟢 利多 |
| 6/18 | Truth Social | Elon Musk TerraFab 建厂 | 行业级 | TSLA↑ INTC↑ | 🟢 利多 |
| 6/16 | 行政令 | Intel 18A-P 风险试产 | 公司级 | INTC↑ | 🟢 利多 |
| 6/中旬 | 贸易政策 | 对 60 国 Section 301 关税提案 | 宏观级 | 整体市场↓ | 🔴 利空 |
| 6/中旬 | 贸易政策 | 对中国加征 100% 关税 | 行业级 | 芯片设备↓ AAPL↓ | 🔴 利空 |
| 6/中旬 | 中国反制 | 稀土出口限制 + 125% 报复关税 | 宏观级 | 稀土↑ 制造业↓ | 🔴 利空 |
| 6/4 | TSMC 股东会 | 董事长称"不担心 Intel 竞争" | 行业级 | TSMC↓ INTC↑ | 中性 |

### 📊 政策影响矩阵

| 标的 | 政策利好 | 政策利空 | 净政策方向 |
|---|---|---|---|
| **INTC** | Truth Social 力挺 + 政府 9.9% 持股 + 18A-P 试产 | 良率落后 TSMC | 🟢 强利多 |
| **NVDA** | Truth Social 提及合作 + 芯片国产化趋势 | 中国关税影响出口 | 🟢 利多 |
| **AAPL** | Trump 亲宣 Intel 合作 | 中国关税 + DOJ 反垄断 | 🟡 中性偏多 |
| **TSLA** | Musk TerraFab + 政府支持 | 中国市场份额下降 | 🟢 利多 |
| **DELL** | 五角大楼 $9.7B 合同 + 政府 IT 支出 | 关税影响硬件成本 | 🟢 利多 |
| **PLTR** | 国防支出增加 + $10B Army 合同 | — | 🟢 利多 |

### 🎯 政策优先标的（与 Agent 1-5 交叉验证前）

| 排名 | 标的 | 政策催化剂强度 | 预计持续期 |
|---|---|---|---|
| 1 | NVDA | 🔴🔴🔴🔴 | 多季度（芯片国产化） |
| 2 | INTC | 🔴🔴🔴🔴🔴 | 多年（国家战略资产） |
| 3 | DELL | 🔴🔴🔴 | 单次合同执行期 |
| 4 | AAPL | 🔴🔴 | 中长期（供应链迁移） |
| 5 | TSLA | 🔴🔴🔴 | 多年（Terafab 建设） |

> ⚠️ 注意：INTC 不在 Bitget RWA 标的列表，但可通过股票映射影响 NVDA/AAPL/TSLA 的 regime 判断。
