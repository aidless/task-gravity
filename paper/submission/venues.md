# 投递目标(Venues)——基于 2026-07-22 实时信息

> **重要背景**:中国自动化学会(CAA)已于 2026 年 3 月正式将 NeurIPS
> 从推荐会议目录中除名,理由是该会议推行的涉华投稿限制。
> 因此本表**优先国内会议**,国际会议作为次选并附说明。

## 第一优先级:国内会议(CAA / CAAI / CCF 推荐)

| 会议 | 主办 | 典型时间 | 投稿窗口 | 推荐理由 |
|------|-----|---------|---------|---------|
| **CICAI 2026**(中国人工智能学术大会) | CAAI | 11月底–12月初 | 8月–9月 | CAAI 主会,接收综述/position,影响力大 |
| **GAITC 2026 全球人工智能技术大会** | CAAI | 已闭幕(5月) | 已过 | 错过,可投 2027 |
| **CEAI 2026 中国具身智能大会** | CAAI | 已闭幕(2026) | 已过 | 错过,可投 2027 |
| **CICAI 2027**(下一代) | CAAI | 预计 11–12 月 | 预计 8–9 月 2027 | 首选,长投稿周期 |
| **中国机器学习大会(CCF 推荐)** | CCF | 8 月底–10 月初 | 6 月–8 月 | 滚动截止,部分分论坛接受 short paper |
| **CSAI 智能科学大会** | 智能科学学会 | 10–11 月 | 7 月–9 月 | 跨学科友好 |

> 注意:本表的截止时间为典型值,**实际以 CFP 为准**。投递前请
> 重新核对。

## 第二优先级:国际会议(IEEE / ACM 系)

| 会议 | 截止 | 适合度 | 备注 |
|------|------|--------|------|
| **IEEE ICAIIC 2027**(2 月,韩国) | 8 月 | ★★★★ | 接收 short paper |
| **ACM K-CAP 2027**(6 月) | 1–2 月 | ★★★ | 知识表征专会 |
| **IEEE ICDM workshop 2026**(12 月) | 8–9 月 | ★★★ | 接收 position paper |
| **AAAI 2027** | 8 月 | ★★ | 主会太卷;Spring Symposium 更适合 |
| **AAAI Spring Symposium 2027** | 11–12 月 | ★★★★ | position paper 友好 |

> ICML / NeurIPS / ICLR 2027 主会投稿期在 2027 年 1–5 月,
> 仍可准备。CAA 除名 NeurIPS 仅影响国内推荐,**不影响个人投稿**,
> 但需自行评估合作者政策。

## 第三优先级:arXiv 抢先发(配合上述任何投递)

| 动作 | 时间 | 价值 |
|------|------|------|
| 把 paper.md 转 arXiv 格式(`\documentclass{article}`) | 立即 | 占坑 + 可被引用 |
| 申请 arXiv:cs.LG / cs.AI | 1–2 周 | 锁定时间戳 |

> arXiv 不审稿,可立即发;但需**用真名实机构署名**(匿名 arXiv
> 在某些 workshop 政策下不可作为正式发表)。

## 建议的投稿顺序

1. **本周**:把现有 paper.md 转成 arXiv 格式,挂 arXiv(占坑 + 锁定作者身份)。
2. **8 月**:把中文版 cover letter + 投稿包投 CICAI 2026 / 类似的
   国内 11 月大会。
3. **9–10 月**:基于国内审稿意见修稿,投 AAAI Spring Symposium 2027。
4. **12 月–1 月**:扩成 8 页 main paper,投 ICML 2027 workshop。
5. **2027 春**:有结果后转投 NeurIPS / ICLR workshop(若届时政策
   改善)或国内旗舰会。

## 防御性话术(对抗 reviewer 的常见反对)

> **"这不就是 reward hacking 换个名字吗?"**

回应三件套(对应到本文):

1. **形式化更强**:Langevin SDE + 引力算子 G(θ) 是严格刻画,不是观察分类。
2. **可观测指标**:CTRR 不需要访问奖励函数,只看轨迹,可在黑盒部署下测量。
3. **跨学科桥**:与人类强迫症的同构生成可证伪预测(参见 Open Problem OP-4),这是 reward hacking 完全没有的。

> **"实验规模太小,只有 3 个任务。"**

回应:

1. 这是 **workshop position paper** 的标准规模;参考 Open Problem OP-3 的 64 任务扩展计划。
2. 关键效应在 3 任务下已显现,且 tabular + PPO 两套独立实现相互印证。
3. 我们正在邀请社区贡献 MiniGrid/Procgen 基准,见 README "How to extend"。

> **"和已有概念重名了。"**

回应:

1. 我们在 Appendix B 已经做了术语映射表,确认 Task Gravity 与 Reward Hacking / Behavioral Sink / Engagement Loop / Mode Collapse 互不等价。
2. 命名一个新概念是 position paper 的合法贡献。
3. 指标(TRR/CTRR)是首次提出,不存在重名问题。

## 提交前最终检查

- [ ] 论文 word count 在 venue 上限内
- [ ] 作者信息完整,机构准确
- [ ] 引用格式符合 venue 要求(IEEE / ACM / LNCS)
- [ ] 代码仓库公开(README 已写)
- [ ] 数据可用性声明已附
- [ ] 利益冲突声明已附
- [ ] 中英文版本各一份

---

> 本表为投前路线图,具体截止日期以各 CFP 为准。
> 如需对某 venue 进一步调整策略(例如加页数、改格式),
> 告诉我 venue 名称即可。