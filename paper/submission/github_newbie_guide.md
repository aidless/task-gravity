# GitHub 新手指南 — 从 0 到第一个 push(Task Gravity 用)

> 假设你从来没建过 GitHub 仓库。这份指南带你一步步走完。
> 大约需要 5–10 分钟。

---

## Step 0 · 你需要什么

| 东西 | 检查方式 | 没有怎么办 |
|------|---------|----------|
| GitHub 账号 | 登录 <https://github.com> | <https://github.com/signup> 免费注册 |
| git 命令行工具 | PowerShell 跑 `git --version` | <https://git-scm.com/download/win> 下载安装 |
| 已配 git 用户名/邮箱 | `git config --global user.name` | 见下方 |

> **当前状态**(已检测):
> - ✅ git 已装(git version 2.55.0)
> - ✅ 身份已配:`aidless <101927025+aidless@users.noreply.github.com>`
> - ✅ SSH key 已存在(`C:\Users\Administrator\.ssh\id_ed25519.pub`)
> - ⚠️ 但你需要在 GitHub 上有一个 **`aidless` 账号**(如果还没有,先注册)

---

## Step 1 · 注册/登录 GitHub(2 分钟)

1. 打开 <https://github.com>
2. 如果没账号,点右上角 **Sign up**,跟着提示走
   - 建议用户名就用 `aidless`(因为我们检测到的 git 身份是这个,后续 DOI 会带)
   - 邮箱用一个真实的(找回密码用,不会公开)
3. 登录后,右上角应该是你的头像

---

## Step 2 · 创建空仓库(2 分钟)

1. 打开 <https://github.com/new>
2. 填表:

   | 字段 | 填什么 |
   |------|------|
   | **Owner** | `aidless`(选你自己) |
   | **Repository name** | `task-gravity` |
   | **Description** | `Task Gravity: Policy Attractors and Cross-Task Compulsivity in Reinforcement Learning Agents` |
   | **Visibility** | `Public` ⚠️ 必须 Public,否则 Zenodo 无法 mint DOI |
   | **Initialize** | ⚠️ **全部不要勾**——README、license、.gitignore 都不加(我们自己有) |

3. 点 **Create repository**
4. 创建成功后,你会看到一页提示 "Quick setup",里面有三种 URL:
   ```
   https://github.com/aidless/task-gravity.git
   git@github.com:aidless/task-gravity.git
   aidless/task-gravity
   ```
   - 第一个是 HTTPS,带 token 用
   - 第二个是 SSH,我们这个用这个(因为已有 SSH key)
   - 第三个只是名字

---

## Step 3 · (一次性)把 SSH 公钥加到 GitHub(1 分钟)

> 这步**只在你新设备/首次配置时**需要。已有 SSH key 的设备一般不需要重复做。

1. 打开 <https://github.com/settings/keys>
2. 点 **New SSH key**
3. 填表:
   - Title: 任意(例如 `work-laptop-2026`)
   - Key type: `Authentication Key`
   - Key: 粘贴下面的内容
4. 获取公钥:
   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
   ```
   然后 `Ctrl+V` 粘贴到 Key 框
5. 点 **Add SSH key**

---

## Step 4 · 测试 SSH 连接(30 秒)

```powershell
ssh -T git@github.com
```

第一次会问:
```
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
输 `yes`。

成功的话输出:
```
Hi aidless! You've successfully authenticated, but GitHub does not provide shell access.
```

> ⚠️ "does not provide shell access" 是正常的!不是错误。
> 关键标志是 `Hi <username>!`。

---

## Step 5 · 跑 push 脚本(2 分钟)

```powershell
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"

.\paper\submission\push_to_github.ps1
```

脚本会问你:
1. Repo URL —— 直接粘贴 `git@github.com:aidless/task-gravity.git`
2. 其他都已经检测到,会自动用

跑完会输出:
```
===> Tagging v1.0 (triggers Zenodo DOI)
     tag v1.0 pushed
```

**这就成功了!**

---

## Step 6 · 在 GitHub 上确认(30 秒)

打开 <https://github.com/aidless/task-gravity>,你应该看到:

- ✅ 所有文件(README.md, paper/, experiment/ 等)
- ✅ `v1.0` tag(左边 Releases)
- ✅ 右上角显示 "Cite this repository" 按钮(我们 CITATION.cff 生效)

---

## Step 7 · 申请 Zenodo DOI(5 分钟)

1. 打开 <https://zenodo.org>
2. 右上角 **Log in** → **Sign in with GitHub**
3. 授权 Zenodo 读你的 GitHub
4. 右上角下拉菜单 → **GitHub**
5. 找到 `task-gravity` 仓库,点右侧 **Enable** 按钮
6. 然后点 **+ New upload** → **GitHub**
7. 选 `task-gravity` 仓库 → 选 `v1.0` tag
8. 填元数据(Zenodo 会自动从 `.zenodo.json` 读):
   - Title、Authors、Description、Keywords 等已经预填
9. 点 **Publish**

**几秒钟后,Zenodo 会给你一个 DOI**:
```
10.5281/zenodo.NNNNNNN
```

---

## Step 8 · 把 DOI 填回项目(1 分钟)

```powershell
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"

$zenodo = '10.5281/zenodo.XXXXXXX'   # 替换成真实 DOI
$chinaxiv = '__DOI_CHINAXIV__'         # 等 ChinaXiv 审核后再填

$files = @(
    'paper\position\paper.md',
    'paper\theory\task_gravity_theory.tex',
    'paper\submission\CITATION.cff',
    'paper\submission\DOI.md',
    'paper\submission\.zenodo.json'
)
foreach ($f in $files) {
    (Get-Content $f) -replace '__DOI_ZENODO__',$zenodo -replace '__DOI_CHINAXIV__',$chinaxiv | Set-Content $f
}

# 提交到 GitHub
git add .
git commit -m "mint Zenodo DOI: $zenodo"
git push
git tag -a v1.1 -m "DOI minted"
git push origin v1.1
```

---

## 🆘 出错了?

### `git push` 报错 `Permission denied (publickey)`

- 没把公钥加到 GitHub,见 Step 3
- 加完后重试:`ssh -T git@github.com` 先确认能连

### 报错 `Repository not found`

- GitHub 上还没建这个仓库,见 Step 2
- 或者仓库名拼错了(应该是 `task-gravity`,不是 `task_gravity` 或 `taskgravity`)

### 报错 `Authentication failed`

- HTTPS 模式下用了密码而不是 token
- 切回 SSH(用 `git@github.com:...` 的 URL)

### 报错 `Updates were rejected because the remote contains work`

- GitHub 上你勾了 README/license/.gitignore 之一
- 解决:GitHub 上删除仓库重建,这次不要勾任何东西
- 或者:`git pull origin main --rebase --allow-unrelated-histories`,但麻烦

### `ssh -T git@github.com` 提示 "Host key verification failed"

- GitHub 的 host key 没加进 known_hosts
- 解决:用 yes 接受一次,或者手动加:
  ```powershell
  ssh-keyscan -t ed25519 github.com >> $env:USERPROFILE\.ssh\known_hosts
  ```

### 脚本报 "git NOT found in PATH"

- 安装 Git for Windows:<https://git-scm.com/download/win>
- 安装完重启 PowerShell

### `aidless` 不是你的 GitHub 用户名

如果你想用别的账号:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```
然后把 `aidless` 替换成你的真实用户名。

---

## ✅ 全流程检查清单

- [ ] GitHub 账号 `aidless` 注册成功
- [ ] 创建空仓库 `task-gravity`(不勾任何初始化选项)
- [ ] SSH 公钥已加到 GitHub
- [ ] `ssh -T git@github.com` 输出 `Hi aidless!`
- [ ] 跑 `push_to_github.ps1`,成功
- [ ] GitHub 网页上能看到 `v1.0` tag
- [ ] Zenodo 拿到 DOI(形如 `10.5281/zenodo.XXXXXXX`)
- [ ] 把 DOI 替换进所有占位符
- [ ] 再 push 一次新版本
- [ ] ChinaXiv 投稿(同步)

---

## 还需要 help?

任何一步卡住,把错误信息粘回来,我帮你 debug。