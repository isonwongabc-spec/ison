# GitHub Triage 自动化配置

## 仓库信息
- 当前仓库: isonwongabc-spec/ison
- 配置时间: 2026-03-02

## 自动化设置

### 1. 定期 Triage（Cron Job）
每小时检查一次仓库的 Issues 和 PRs：

```bash
# 添加 cron job
openclaw cron add --name "github-triage-hourly" \
  --schedule "0 * * * *" \
  --command "cd C:\Users\USER\.openclaw\workspace && gh triage"
```

### 2. 手动触发命令

```bash
# 对所有 Issues 和 PRs 进行 triage
gh triage

# 仅 triage Issues
gh triage issues

# 仅 triage PRs
gh triage prs
```

### 3. Webhook 触发（实时）

在 GitHub 仓库设置 webhook：
- Payload URL: http://your-server:port/github-webhook
- Content type: application/json
- Events: Issues, Pull requests

### 4. 子代理分类规则

| 类型 | 检测条件 | 处理方式 |
|------|----------|----------|
| ISSUE_QUESTION | 标题包含 [Question], ?, how to | 自动回答并关闭 |
| ISSUE_BUG | 标题包含 [Bug], Bug:, 错误描述 | 分析根因，评论但不关闭 |
| ISSUE_FEATURE | 标题包含 [Feature], Feature Request | 评估可行性 |
| PR_BUGFIX | 标题以 fix 开头，分支含 fix/ | 符合条件时自动合并 |
| PR_OTHER | 其他 PR | 分析并给出建议 |

### 5. 自动合并条件（PR_BUGFIX）

必须满足以下所有条件才会自动合并：
- ✅ CI 检查全部通过
- ✅ 已被批准 (Review Decision: APPROVED)
- ✅ 修复明显正确
- ✅ 无副作用（非架构变更）
- ✅ 非草稿 PR
- ✅ 无合并冲突

## 配置文件

### .github/triage-config.yml（需要手动创建）

```yaml
# 自动回复前缀
bot_prefix: "[jarvis-bot]"

# Issue 处理设置
issues:
  auto_answer_questions: true    # 自动回答并关闭问题
  auto_close_stale: false        # 不自动关闭过期 issue
  stale_days: 30                 # 过期天数

# PR 处理设置
pull_requests:
  auto_merge_safe_bugfixes: true  # 自动合并不危险的 bugfix
  require_ci_pass: true          # 必须 CI 通过
  require_approval: true         # 必须有人批准

# 通知设置
notifications:
  on_auto_merge: true            # 自动合并时通知
  on_manual_attention: true      # 需要人工处理时通知
```

## 启动自动化

运行以下命令启动自动化：
```bash
openclaw skills run github-triage
```

或手动执行一次测试：
```bash
cd C:\Users\USER\.openclaw\workspace
openclaw run github-triage --repo isonwongabc-spec/ison
```

## 日志位置

- Triage 日志: `logs/github-triage/`
- 子代理结果: `logs/github-triage/subagents/`

---
配置完成时间: 2026-03-02
