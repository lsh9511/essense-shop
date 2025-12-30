# 테스트 실행 스크립트

set -e

echo "🧪 Starting tests..."
echo ""

# pytest 실행
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Running pytest with coverage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# tests 폴더가 없으면 생성
if [ ! -d "tests" ]; then
  echo "⚠️  tests/ directory not found. Creating it..."
  mkdir tests
  touch tests/__init__.py
fi

uv run pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "✅ All tests passed!"
echo "📊 Coverage report generated in htmlcov/index.html"