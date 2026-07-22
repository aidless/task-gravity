# GitHub 推送认证指南 — SSH vs HTTPS + Token

你大概率在 push 时会卡在认证环节。本指南帮你 5 分钟内搞定。

## 两条路速览

| | SSH | HTTPS + Token |
|---|-----|--------------|
| 优点 | 一次配置,长期免输 | 不需要 SSH agent,Windows 友好 |
| 缺点 | 需要 OpenSSH + 私钥管理 | 每次 push 都要 token(Git Credential Manager 可缓存) |
| 适合 | 多设备、长期使用 | 单台电脑、临时使用 |
| GitHub 推荐 | ✅ 推荐 | ✅ 仍然支持 |

---

## 路径 1 · SSH(推荐,一劳永逸)

### Step 1. 检查 OpenSSH(Windows 10/11 自带)

```powershell
ssh -V
```

应输出类似 `OpenSSH_for_Windows_8.1p1`。如果命令找不到,**用路径 2**。

### Step 2. 生成 SSH key

```powershell
ssh-keygen -t ed25519 -C "your_real_email@domain.com"
# 一路回车,不设 passphrase(测试用);生产环境建议设
```

### Step 3. 把公钥复制到 GitHub

```powershell
# 自动复制到剪贴板
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
```

然后:
1. 打开 <https://github.com/settings/keys>
2. **New SSH key**
3. Title: 任意(例如 "work-laptop")
4. Key type: Authentication Key
5. Key: 粘贴(`Ctrl+V`)
6. **Add SSH key**

### Step 4. 测试连接

```powershell
ssh -T git@github.com
```

首次会问 `Are you sure you want to continue connecting (yes/no/[fingerprint])?` —— 输 `yes`。

成功输出:
```
Hi <your-username>! You've successfully authenticated...
```

### Step 5. 推送(用 SSH URL)

仓库 URL 形如:
```
git@github.com:<your-username>/task-gravity.git
```

注意是 `git@` 开头,不是 `https://`。

---

## 路径 2 · HTTPS + Personal Access Token(Windows 简单)

### Step 1. 生成 PAT

1. 打开 <https://github.com/settings/tokens>
2. **Generate new token** → **Generate new token (classic)**
3. Note: `task-gravity-push`(任意)
4. Expiration: 90 days(或自定义)
5. **Select scopes**:
   - ☑ `repo`(完整)
   - ☑ `workflow`(如果要跑 GitHub Actions)
6. **Generate token**
7. **复制 token 并保存**(只显示一次!)

### Step 2. 用 credential manager 缓存

```powershell
# 第一次 push 时输入用户名 + token(代替密码)
git push -u origin main
# Username: <your-username>
# Password: <paste-token>
```

如果 Windows 安装了 **Git Credential Manager**(默认装 Git for Windows 时会带),以后 push 不会再问。

### Step 3. 想清缓存?

```powershell
git credential-manager erase https://github.com
```

---

## 路径 3 · GitHub Desktop(最简单,完全 GUI)

如果命令行怕怕:
1. 下载 <https://desktop.github.com>
2. 登录 GitHub 账号
3. **File → Add local repository** → 选本项目根目录
4. **Publish repository** → 推上去

但这种方式**不产生 CLI git 仓库的 remote 配置**,后续用 CLI push 会麻烦。**推荐 SSH + CLI**。

---

## 一键脚本

我们已为你写好 `push_to_github.ps1`,支持:

```powershell
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f59719ea42441f41e2578"

# SSH 路线(推荐)
.\paper\submission\push_to_github.ps1 -GenerateSshKey

# HTTPS + token 路线
.\paper\submission\push_to_github.ps1
```

---

## 常见报错

### `Permission denied (publickey)`

- 公钥没加对。检查 <https://github.com/settings/keys> 里有没有你刚才的 key
- 或者 `ssh-add` 一下:`ssh-add $env:USERPROFILE\.ssh\id_ed25519`

### `remote: Repository not found`

- 仓库 URL 写错了,或者 GitHub 上还没有这个空仓库
- 先去 <https://github.com/new> 创建一个空 repo(不要勾选 README/license/.gitignore)

### `Authentication failed`

- HTTPS 模式下用了密码而不是 token
- 或者 token 过期了,重新生成一个

### `Updates were rejected because the remote contains work...`

- 你本地不是从 origin clone 下来的,而是手动 `git init` 然后加的 origin
- 解决:`git pull origin main --rebase` 然后再 `git push`

---

## 推荐工作流

```powershell
# 一次性配置
ssh-keygen -t ed25519 -C "your@email.com"
# (把 .pub 加到 GitHub)

# 一次性推送(项目根目录)
cd "C:\Users\...\6a5f59719ea42441f41e2578"
.\paper\submission\push_to_github.ps1 -GenerateSshKey
# (脚本会引导你完成所有步骤)

# 之后日常更新
git add .
git commit -m "update"
git push
```

---

## 推送后的下一步(Zenodo + ChinaXiv)

拿到 GitHub 仓库 URL 后,见 `DOI.md` 走两条路获取 DOI。