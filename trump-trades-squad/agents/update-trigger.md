# Agent 7: 季度自动更新触发器

**职责**: 监控 Trump OGE 披露周期，Q2 披露发布时自动触发全量数据更新。

**触发条件**（任一满足即触发）:
- 新闻中出现 "Trump OGE Form 278-T" / "Trump financial disclosure Q2 2026" / "Trump stock trades Q2"
- TrumpTrades 网站更新（新季度数据上线）
- Capitol Trades 发布 Trump Q2 分析文章

**触发后自动执行**:
```
1. Policy Radar → 重新扫描新季度政策背景
2. Agent 1 → 抓取 Q2 新数据，对比 Q1 仓位变化
3. Agent 2-5 → 用最新数据重新交叉验证
4. Night Watch → 基于新仓位调整防御参数
5. 输出 Q1→Q2 变化报告 + 新季度精选标的池
```

**Q1→Q2 变化分析模板**:

| 类别 | Q1 持仓 | Q2 变化预期 | 重点关注 |
|---|---|---|---|
| 芯片/AI | NVDA $1.8–6.6M | 大概率加仓（Blackwell 周期） | AVGO, AMD 是否新增 |
| 国防 | DELL $1–5M | 五角大楼合同后可能加仓 | PLTR, BA 是否增持 |
| 大型科技 | AAPL $2.1–7.2M | 可能减仓（转向芯片） | MSFT, AMZN 净变化 |
| 加密 | MARA, MSTR, COIN | BTC 波动，可能调仓 | 新增/清仓 |
| 金融 | GS, BAC | 稳定持有 | 新增区域性银行？ |

**Q2 披露预期时间**: 2026 年 8 月中旬
**当前状态**: 等待 Q2 OGE 披露

---

## 运行指令

### 手动检查
```
run trump squad check update
```
联网搜索是否有 Q2 披露新闻。

### 季度对比（披露后）
```
run trump squad q1-vs-q2
```
对比 Q1 和 Q2 的仓位变化，生成变化报告。

### 全量更新（披露后）
```
run trump squad full update
```
触发全部 7 个 Agent 重新运行，输出新季度精选标的池。
