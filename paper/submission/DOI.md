# 申请 DOI 的两条路 — Task Gravity

arXiv 在你的环境下用不了,但**获取 DOI 并不只有 arXiv 一条路**。本文推荐两条并行路径:

- **路线 A · Zenodo**(国际通用,15 分钟,绑定 GitHub)
- **路线 B · ChinaXiv**(国内合规,3 天,中科院主办)

两条路互不冲突,建议**两条都做**,一个拿国际 DOI,一个拿国内 DOI。

---

## 路线 A · Zenodo(首选,15 分钟搞定)

**前置条件**:GitHub 账号 + 能 push 仓库。

### Step 1. 准备 GitHub 仓库(10 分钟)

把整套项目推到 GitHub:

```bash
# 在 GitHub 上先建一个空仓库,例如:yourname/task-gravity
# 然后在本地:
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"

git init
git add .
git commit -m "Task Gravity: initial submission package"
git branch -M main
git remote add origin https://github.com/yourname/task-gravity.git
git push -u origin main
```

> **注意**:`.gitignore` 建议加上 `__pycache__/`、`*.pyc`、`checkpoints/`(PPO 模型太大,几百 MB)。
> 我已经为你准备好了 `CITATION.cff`,放仓库根目录。

### Step 2. 在 Zenodo 登录并联动 GitHub(2 分钟)

1. 打开 <https://zenodo.org>
2. 点右上角 **Log in** → 选 **GitHub**
3. 授权 Zenodo 访问你的 GitHub
4. 在右上角下拉菜单 → **GitHub** → 看到你刚推的 `task-gravity` 仓库
5. 点仓库右侧 **Enable** 按钮

> 一旦 enable,Zenodo 会**自动监听**这个仓库的每次 release。
> 每次你打 tag,Zenodo 自动生成一个 DOI 给你。

### Step 3. 手动触发第一次 release(2 分钟)

1. 在本地打一个 tag:
   ```bash
   git tag -a v1.0 -m "Initial submission"
   git push origin v1.0
   ```
2. 回到 Zenodo → **Upload** → **New upload** → **GitHub**
3. 选 `task-gravity` repo,选 `v1.0` tag
4. 填写元数据:
   - **Upload type**: Publication
   - **Publication type**: Preprint
   - **Title**: Task Gravity: Policy Attractors and Cross-Task Compulsivity in Reinforcement Learning Agents
   - **Authors**: 填你的名字、邮箱、ORCID(如有)
   - **Description**: 复制 paper.md 的 Abstract
   - **Keywords**: 复制 keywords.md 的英文关键词
   - **License**: MIT
   - **Communities**: 选 `reinforcement-learning`、`ai-safety`(如有)
5. 点 **Publish**

### Step 4. 获取 DOI(立即)

发布后 Zenodo 会显示一个 landing page,DOI 形如:

```
10.5281/zenodo.1234567
```

把这个 DOI 填进 `paper/submission/DOI.md` 的"D 当前 DOI"节,并替换 paper.md 里的 `__DOI__` 占位符。

### Zenodo 的额外好处

- 每次 git tag 都会生成**新 DOI**(永久有效,可分别引用)
- 直接被 **DataCite** 索引(全球 DOI 注册机构)
- 支持 GitHub Releases 与 Zenodo record 的双向跳转
- **完全免费**,无审核(上传内容需符合社区准则)

---

## 路线 B · ChinaXiv(国内合规,3 天)

[chinaxiv.org](http://www.chinaxiv.org) —— 中国科学院文献情报中心主办,科技部认可的中文预印本平台。

### Step 1. 注册账号(5 分钟)

1. 打开 <http://www.chinaxiv.org>
2. 点右上角 **注册**
3. 选 **作者注册**
4. 需要:
   - 真实姓名
   - 单位(高校/科研院所/企业)
   - 身份证号(用于实名认证)
   - 邮箱 + 手机号
5. 等待 1 个工作日审核

### Step 2. 准备投稿材料(15 分钟)

需要:
- **PDF 全文**:用我们现有的 `paper/position/paper.html` 浏览器打印为 PDF 即可,或把 paper.md 转 Word 后导出 PDF
- **中文摘要**:200–300 字,从 paper.md 摘要翻译
- **英文摘要**:从 paper.md 摘要原文
- **关键词**:从 keywords.md 复制
- **作者信息**:姓名、单位、邮箱、ORCID
- **基金项目**:无(填"自筹"或"无")

### Step 3. 在线提交(10 分钟)

1. 登录 chinaxiv.org
2. 左侧菜单 → **我的投稿** → **新投稿**
3. 按表单填写上述材料
4. 上传 PDF
5. 选择学科分类:人工智能 / 机器学习
6. 提交

### Step 4. 等审核(1–3 天)

- 通过后会在 ChinaXiv 首页"最新提交"出现
- 系统自动分配 **中文 DOI**,形如:
  ```
  10.12074/YYYYMMDD.NNNNNN
  ```
- 也会有一个永久 URL:`https://chinaxiv.org/abs/YYYYMMDD.NNNNNN`

### ChinaXiv 的额外好处

- 国内会议评审、项目结题、职称评审**都认**
- 中文 DOI 符合国内学术规范
- 完全免费
- 论文被中科院系统检索

---

## 当前 DOI 占位符(待替换)

在 paper.md 里,目前所有 DOI 引用都是占位符 `__DOI_ZENODO__` 和 `__DOI_CHINAXIV__`。拿到 DOI 后,用以下命令替换:

```bash
# 在 Linux/Mac/Git Bash
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"
sed -i 's/__DOI_ZENODO__/10.5281\/zenodo.XXXXXXX/g' paper/position/paper.md
sed -i 's/__DOI_CHINAXIV__/10.12074\/YYYYMMDD.NNNNNN/g' paper/position/paper.md

# 在 PowerShell
(Get-Content paper/position/paper.md) -replace '__DOI_ZENODO__','10.5281/zenodo.XXXXXXX' | Set-Content paper/position/paper.md
(Get-Content paper/position/paper.md) -replace '__DOI_CHINAXIV__','10.12074/YYYYMMDD.NNNNNN' | Set-Content paper/position/paper.md
```

---

## ⚡ 当前 DOI

> **Zenodo**:`__DOI_ZENODO__`(待 Zenodo 发布后填入)
> **ChinaXiv**:`__DOI_CHINAXIV__`(待 ChinaXiv 审核通过后填入)

---

## 为什么不推荐别的方案

| 方案 | 不推荐的理由 |
|------|------------|
| **arXiv** | 你已确认用不了 |
| **FigShare** | 没有 GitHub 联动,版本管理麻烦 |
| **OSF** | 国内访问慢,审稿系统偶发不兼容 |
| **SSRN** | 偏社科,AI 圈引用率不高 |
| **ResearchGate** | 私信发请求才能下载全文,正式评审不便 |

---

## 提交后的下一步

拿到 DOI 后:

1. **更新 paper.md** —— 替换 DOI 占位符
2. **更新 BibTeX**(在 paper/theory/task_gravity_theory.tex 里加 `doi={...}`)
3. **更新 README.md** —— 在标题下加 DOI 行
4. **更新 venues.md** —— 在每个 venue 后面标注"已 DOI"
5. **在会议 cover letter 里引用 DOI** —— 增强可信度

---

## 时间预算(全流程)

| 步骤 | 时间 |
|------|------|
| GitHub 推仓库 | 10 分钟 |
| Zenodo 发布 | 5 分钟 |
| ChinaXiv 实名注册 | 5 分钟 |
| ChinaXiv 投稿 | 15 分钟 |
| 等 ChinaXiv 审核 | 1–3 天(被动等待) |
| 替换 DOI 占位符 | 2 分钟 |

**总主动操作时间:约 40 分钟**(ChinaXiv 审核期间你可以做别的)。