# Agent 3: 内部人监控器

**职责**: 监控 SEC Form 4 披露，发现 CEO/CFO/董事的大额买入和集体买入。

**数据源**:
- OpenInsider: `http://openinsider.com`
- SEC EDGAR Form 4: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent`
- Quiver Quantitative Insider Trading

**运行指令**:
```
联网搜索最近 30 天的 SEC Form 4 披露：
1. CEO/CFO 大额公开市场买入（Code P，非期权行权）
2. 多名高管同时买入同一只股票（集体买入信号）
3. 内部人买入金额 Top 10
4. 与 Agent 1 种子池重叠的标的，内部人是在买还是卖？

过滤规则：
- 只看 Code P（公开市场买入），排除 Code A（授予）、Code F（税售）
- 金额 > $100K 才关注
- 集体买入 > 单人买入 > 单人卖出
```

**当前扫描**（2026-06-24）:

### 近期重大内部人买入

| 日期 | 标的 | 内部人 | 角色 | 金额 | 信号强度 |
|---|---|---|---|---|---|
| 6/10-11 | CNTM | Bhaskar Panigrahi | CEO | **$40.9M** | 🔴 极大但需验证 |
| 6/17 | FISV | Paul Todd | CFO | $500K | 🟡 中等 |
| 6/17 | FISV | 4 位董事 | 董事会 | $1.22M | 🟠 集体买入 |
| 6/22 | MSTR | Le Phong | CEO | $999K | 🟡 中等 |
| 6/5-8 | BZUN | Wenbin Qiu | CEO | $54K | 🟢 小 |

### 与 Trump 种子池重叠分析

| Trump 标的 | 内部人信号 | 评分 |
|---|---|---|
| MSTR | CEO 买入 $999K（6月22日） | ✅ +1 |
| DELL | 无近期 Form 4 买入 | 0 |
| NVDA | 无近期 Form 4 买入（内部人静默期？） | 0 |
| ORCL | 待查 | ? |

**关键观察**:
- MSTR 在 Trump Q1 建仓 + CEO 近日买入 ≈ $1M → 双重信号
- NVDA 内部人静默可能是财报前 blackout period
- DELL 无内部人买入，但五角大楼合同是更强的催化剂
