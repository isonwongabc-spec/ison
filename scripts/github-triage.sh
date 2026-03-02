# GitHub Triage 自动化脚本
# 仓库: isonwongabc-spec/ison

REPO="isonwongabc-spec/ison"

echo "=========================================="
echo "🤖 GitHub Triage 自动化"
echo "仓库: $REPO"
echo "时间: $(date)"
echo "=========================================="

# 1. 获取所有开放的 Issues
echo ""
echo "📋 检查 Issues..."
gh issue list --repo $REPO --state open --json number,title,state,createdAt,updatedAt,labels,author,body --limit 100

ISSUE_COUNT=$(gh issue list --repo $REPO --state open --json number --jq 'length')
echo "找到 $ISSUE_COUNT 个开放 Issues"

# 2. 获取所有开放的 PRs
echo ""
echo "🔀 检查 Pull Requests..."
gh pr list --repo $REPO --state open --json number,title,state,createdAt,updatedAt,labels,author,body,headRefName,baseRefName,isDraft,mergeable,reviewDecision --limit 100

PR_COUNT=$(gh pr list --repo $REPO --state open --json number --jq 'length')
echo "找到 $PR_COUNT 个开放 PRs"

# 3. 显示总结
echo ""
echo "=========================================="
echo "📊 Triage 总结"
echo "=========================================="
echo "Issues: $ISSUE_COUNT"
echo "PRs: $PR_COUNT"
echo ""
echo "✅ Triage 检查完成"
echo "下一个自动化检查将在 1 小时后执行"
