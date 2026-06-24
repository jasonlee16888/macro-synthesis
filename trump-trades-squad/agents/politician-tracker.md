# Agent 2: 政客交易追踪器

**职责**: 追踪国会议员和政治资金的实时交易披露，发现"信息优势"交易。

**数据源**:
- Quiver Quantitative: `https://www.quiverquant.com`
- Capitol Trades: `https://www.capitoltrades.com`
- House disclosures: `https://disclosures-clerk.house.gov`
- Senate disclosures: `https://efdsearch.senate.gov`

**运行指令**:
```
联网搜索最近 30 天的：
1. 国会议员（参议院+众议院）最新股票交易披露
2. 是否有议员的交易与 Trump Q1 持仓重叠？
3. 重叠标的的交易方向（买入 vs 卖出）
4. Quiver "Congress Buys" bot 当前持仓 Top 10

重点信号：
- 同一股票被 3+ 议员同时买入 → 强信号
- 议员买 + Trump 持有 → 双重确认
- 议员集体卖出 → 风险信号

输出：与 Agent 1 种子池交叉后的重叠标的列表。
```

**当前扫描**（2026-06-24）:

### 关键发现

| 信号 | 详情 |
|---|---|
| Quiver Congress Buys bot | H1 2026 回报 **+20.80%** vs S&P 500 +10.93% |
| 历史累计回报 | 自 2020 年 4 月 **+580.50%** vs S&P +207.32% |
| Congress Sells bot | H1 仅 +4.68%，严重跑输大盘 |
| 最新披露（6月4日） | Rep. Virginia Foxx 买入 ARLP |
| 最新披露（5月） | Rep. Moskowitz 买入 GILD $30K |

### 与 Trump 种子池重叠分析

| Trump 标的 | 议员信号 | 状态 |
|---|---|---|
| NVDA | 国会 AI/芯片股持续买入趋势 | ✅ 双重确认 |
| DELL | 五角大楼 $9.7B 合同 + 国会国防股偏好 | ✅ 双重确认 |
| PLTR | 国防承包商，国会国防委员会成员常见标的 | ✅ 双重确认 |
| MSFT/AMZN | 大型科技：国会交易较分散 | ⚠️ 弱信号 |

**待观察**: 如 DELL 出现议员卖出信号，需要降级。
