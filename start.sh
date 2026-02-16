#!/bin/bash
set -e

echo "🚀 Starting Resume Analyzer Setup..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "⚠️ Docker not found. Switching to Native Mode..."
    
    # Check Ports
    if lsof -i :3000 > /dev/null || lsof -i :8000 > /dev/null; then
        echo "❌ Ports 3000 or 8000 are in use. Please stop other processes."
        lsof -i :3000
        lsof -i :8000
        exit 1
    fi

    echo "📦 Initializing Backend (Native)..."
    cd backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    echo "Installing Python dependencies (this may take a while)..."
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    # Run Backend in background
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..

    echo "🎨 Initializing Frontend (Native)..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    # Run Frontend (this will take over the terminal)
    echo "✅ Starting Frontend... (Press Ctrl+C to stop)"
    npm run dev
    
    # Cleanup
    kill $BACKEND_PID
    exit 0
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
