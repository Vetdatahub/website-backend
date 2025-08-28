#!/bin/bash

# Local development helper script
# Run this script to execute all code quality checks locally

echo "🔍 Running code quality checks..."
echo "================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "   Run: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
    echo ""
fi

# Install development dependencies
echo "📦 Installing/updating development dependencies..."
pip install -r requirements-dev.txt

echo ""
echo "🔍 Running flake8 linting..."
flake8 --config=flake8-config . || echo "❌ Flake8 found issues"

echo ""
echo "🎨 Checking code formatting with black..."
black --check --diff . || echo "❌ Code formatting issues found. Run 'black .' to fix, or push to main branch for auto-fix"

echo ""
echo "📝 Checking import sorting with isort..."
isort --check-only --diff . || echo "❌ Import sorting issues found. Run 'isort .' to fix, or push to main branch for auto-fix"

echo ""
echo "🔒 Running security checks..."
echo "   Safety check..."
safety check -r requirements.txt || echo "❌ Security vulnerabilities found"
echo "   Bandit scan..."
bandit -r . -f txt || echo "❌ Bandit found security issues"

echo ""
echo "🧪 Running tests..."
export DJANGO_SETTINGS_MODULE=vetdatahub.settings.settings_dev
python manage.py migrate --settings=vetdatahub.settings.settings_dev
pytest --cov=. --cov-report=term-missing

echo ""
echo "✅ All checks completed!"
echo "📊 Check the coverage report above and aim for >80% coverage"
