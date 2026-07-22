# ChinaXiv 中文摘要 + 投稿材料

## 📌 一、ChinaXiv 投稿专用中文摘要(200–300 字)

### 版本 A · 标准学术摘要(推荐,~280 字)

> 在长时程运行的强化学习智能体中,长期存在一种未被命名、形式化与
> 可测量的失败现象:智能体一旦学会某个高奖励的(状态,动作,奖励)
> 模式,即使当前任务已不再奖励该模式,其策略仍反复回到该模式。
> 我们将这一现象命名为"任务引力"(Task Gravity),并证明它是
> 策略参数空间上朗之万随机微分方程(SDE)的吸引盆。进而,我们定义
> 可计算的"引力算子"G(θ),并提出两个轻量、轨迹级、无需修改智能体
> 的度量指标——轨迹回访率(TRR)与跨任务回归率(CTRR)。TRR 与
> CTRR 共同构成黑盒部署场景下的早期预警信号。形式上,我们证明任务
> 引力与人类强迫行为(成瘾、强迫症、抑郁反刍)是形式同构——批评
> 网络在功能上等价于基底神经节多巴胺通路。在两套独立实验环境
> (NumPy 表格基线与 Stable-Baselines3 PPO 深度复现)中,CTRR 在
> 任务嵌入信号不可靠时显著上升并伴随状态覆盖度塌缩,验证了任务
> 引力作为独立现象的实证存在。

---

### 版本 B · 简短版(180 字,如果 ChinaXiv 限制字数)

> 长时程强化学习智能体常表现出一种失败现象:一旦学会某个高奖励
> 模式,即使该模式不再被当前任务奖励,其策略仍反复回到该模式。
> 我们将此命名为"任务引力",证明它是策略参数空间上朗之万随机
> 微分方程的吸引盆。我们定义可计算的引力算子 G(θ),并提出两个
> 轨迹级黑盒度量指标——轨迹回访率(TRR)与跨任务回归率(CTRR)。
> 进一步,任务引力与人类强迫行为是形式同构。在两套独立实验环境中
> 的实证表明,CTRR 在任务嵌入信号不可靠时显著上升,验证了该现象
> 的可测量性。

---

## 📌 二、中文关键词(从正文抽取)

```
任务引力;策略吸引子;跨任务回归率;轨迹回访率;
强化学习;多任务学习;元学习锁定;人工智能安全;强迫行为
```

---

## 📌 三、英文摘要(ChinaXiv 也要求)

(直接复用 paper.md 里的英文摘要):

> Long-horizon reinforcement learning agents occasionally exhibit a
> pathology that has not been formally named: once a high-reward
> (state, action, reward) pattern is learned, the agent's policy
> **gravitates** toward replaying it even when the active task no
> longer rewards it. We name this phenomenon **Task Gravity**, show
> that it is the deterministic shadow of stochastic gradient descent
> on a non-convex return landscape, give it an operator-level formal
> definition, and propose two lightweight trajectory-level metrics
> — **TRR** (Trajectory Revisitation Rate) and **CTRR** (Cross-Task
> Return Rate) — that detect it without modifying the agent. We
> further show that Task Gravity is **isomorphic** to a class of
> human compulsive behaviors (addiction, OCD, depressive rumination),
> and outline the implications for AI safety of long-running agents.

---

## 📌 四、英文关键词(8 个,符合 ChinaXiv 数量上限)

```
Task Gravity; Policy Attractor; Reinforcement Learning;
Multi-Task Learning; AI Safety; Compulsive Behavior;
Trajectory Revisitation Rate; Cross-Task Return Rate
```

---

## 📌 五、ChinaXiv 投稿检查表

### 提交前(T-3 天)

- [ ] 在 <http://www.chinaxiv.org> 注册账号
- [ ] 实名认证(姓名 + 单位 + 身份证号)—— 通常 1 个工作日通过
- [ ] 在 GitHub 上传 PDF 版本(用浏览器把 paper.html 打印为 PDF)
- [ ] 在 GitHub 上传 Word 版本(可选,有些会议偏好 .docx)
- [ ] 准备中文摘要(版本 A,见上)
- [ ] 准备英文摘要(见上)
- [ ] 准备中英文关键词
- [ ] 准备作者信息(姓名、单位、邮箱、ORCID 可选)

### 提交时(T-0)

- [ ] 登录 chinaxiv.org
- [ ] "我的投稿" → "新投稿"
- [ ] 上传 PDF(主文件,**< 10 MB**)
- [ ] 填入中文摘要(版本 A)
- [ ] 填入英文摘要
- [ ] 填入中文关键词
- [ ] 填入英文关键词
- [ ] 选择学科分类:**人工智能 / 机器学习**
- [ ] 选择研究类型:**Preprint(预印本)**
- [ ] 填写作者列表(注意排序)
- [ ] 填写通讯作者邮箱
- [ ] 基金项目:**无** 或 **自筹**
- [ ] 利益冲突声明:**无**
- [ ] 同意 ChinaXiv 协议
- [ ] 点"提交"

### 提交后(T+1~3 天)

- [ ] 查收邮件,看是否通过初审
- [ ] 通过后 → 拿到 ChinaXiv DOI(形如 `10.12074/YYYYMMDD.NNNNNN`)
- [ ] 把 DOI 填入 paper.md 的 `__DOI_CHINAXIV__` 占位符
- [ ] 把 DOI 加到 GitHub README
- [ ] 把 DOI 加到 venues.md / cover_letter_zh.md
- [ ] 在 CICAI 等会议投稿时引用该 DOI

---

## 📌 六、推荐:同时挂 GitHub + ChinaXiv 的版本说明

> **Zenodo DOI**(国际,15 分钟) ↔ GitHub 仓库
> **ChinaXiv DOI**(国内,3 天) ↔ PDF 全文

两者**互相独立**,任何一个先拿到都可以先用。
建议优先 Zenodo(快),同时启动 ChinaXiv(国内合规)。

---

## 📌 七、稿件 PDF 的准备建议

### 方案 A · 直接打印 paper.html(最快)

1. 在浏览器打开 `paper/position/paper.html`
2. `Ctrl+P` → 选 "另存为 PDF"
3. 纸张 A4,边距默认
4. 包含背景图形:是(让 CSS 渲染)

### 方案 B · 用 Pandoc 转(更专业)

```powershell
# 安装 pandoc: https://github.com/jgm/pandoc/releases
pandoc paper/position/paper.md `
  -o submission/manuscript.pdf `
  --pdf-engine=xelatex `
  -V geometry:margin=1in `
  -V fontsize=11pt `
  -V mainfont="Times New Roman" `
  -V CJKmainfont="SimSun" `
  --citeproc
```

如果 xelatex 没装,用 `wkhtmltopdf` 或浏览器打印也行。

### 方案 C · 直接用现成的 paper.md 复制粘贴到 Word

- 把 paper.md 内容复制到 Word
- 在 Word 里加标题层级(Heading 1/2/3)
- 插入 figure 图片(从 `experiment/results/*.png`)
- 导出 PDF

---

## 📌 八、ChinaXiv 评审尺度(经验值)

| 因素 | 评判 |
|------|------|
| 文章质量 | 预印本宽松,主要看格式 |
| 中文摘要 | 必须通顺、突出创新点 |
| 作者实名 | 必须 + 单位必须真实 |
| 学科分类 | 必须正确(否则会被退回重选) |
| PDF 文件大小 | ≤ 10 MB |
| 页数 | ≤ 20 页(超过要拆分) |
| DOI 申请 | 通过后自动生成,无需手动 |

如果被拒,通常因为格式问题(字体、页边距、字号),质量本身几乎不会被拒。

---

## 📌 九、ChinaXiv 拿到 DOI 后的引用示范

```bibtex
@misc{task_gravity_2026_chinaxiv,
  title        = {任务引力:强化学习智能体中的策略吸引子与跨任务强迫性},
  author       = {{Task Gravity Authors}},
  year         = {2026},
  month        = jul,
  howpublished = {ChinaXiv preprint},
  note         = {DOI: __DOI_CHINAXIV__},
  url          = {https://chinaxiv.org/abs/__DOI_CHINAXIV__}
}
```

填上真实 DOI 后可直接在会议 cover letter 里引用。