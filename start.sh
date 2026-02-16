#!/bin/bash
set -e

echo "🚀 Starting Resume Analyzer Setup..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH."
    exit 1
fi

echo "📦 Building and Starting Containers..."
docker-compose up --build -d

echo "✅ Application Started!"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:8000/docs"
echo ""
echo "📝 To analyze a resume:"
echo "   1. Open localhost:3000"
echo "   2. Upload 'demo_data/sample_resume.pdf'"
echo "   3. Paste content from 'demo_data/sample_job_description.txt'"
