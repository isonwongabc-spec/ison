#!/bin/bash
# OpenCode 自动安装脚本
# 支持 Ubuntu/Debian/CentOS/macOS

set -e

echo "=== OpenCode 安装脚本 ==="
echo ""

# 检测操作系统
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "检测系统: $OS $ARCH"

# 安装依赖
echo "安装依赖..."
if [[ "$OS" == "Linux" ]]; then
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y curl git nodejs npm
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y curl git nodejs npm
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y curl git nodejs npm
    fi
elif [[ "$OS" == "Darwin" ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install node git
fi

# 检查 Node.js 版本
echo "检查 Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "Node.js 版本过低，需要 18+"
        echo "请升级 Node.js: https://nodejs.org/"
        exit 1
    fi
else
    echo "未找到 Node.js，请手动安装 18+ 版本"
    exit 1
fi

# 安装 OpenCode
echo "安装 OpenCode..."
npm install -g @opencode-ai/opencode

# 验证安装
echo ""
echo "验证安装..."
if command -v opencode &> /dev/null; then
    echo "✅ OpenCode 安装成功！"
    echo "版本: $(opencode --version)"
else
    echo "❌ 安装可能失败，请检查 npm 路径"
    exit 1
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用方法:"
echo "  opencode --help          # 查看帮助"
echo "  opencode login           # 登录"
echo "  opencode init            # 初始化项目"
echo "  opencode run             # 运行"
echo ""
echo "如需配置 API Key:"
echo "  export OPENAI_API_KEY='your-key-here'"
