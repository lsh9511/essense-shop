# 코드 품질 검사 스크립트 (포맷팅 + 린팅 + 타입체크)

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 Starting code quality checks..."
echo ""

# 1. Black 포맷팅
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 Step 1/4: Black Formatting"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run black app/ --line-length 100
echo "✅ Black formatting complete!"
echo ""

# 2. Ruff 포맷팅
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Step 2/4: Ruff Formatting"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run ruff format app/
echo "✅ Ruff formatting complete!"
echo ""

# 3. Ruff 린팅 (자동 수정)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Step 3/4: Ruff Linting"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run ruff check app/ --fix
echo "✅ Ruff linting complete!"
echo ""

# 4. Mypy 타입 체크
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔬 Step 4/4: Mypy Type Checking"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run mypy app/ --ignore-missing-imports
echo "✅ Type checking complete!"
echo ""

echo "🎉 All code quality checks passed!"