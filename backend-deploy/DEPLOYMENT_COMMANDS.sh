#!/bin/bash

# Architector-LLM Analytics Backend - Deployment Script
# This script helps you deploy to various free hosting platforms

set -e  # Exit on error

echo "=================================================="
echo "Architector-LLM Analytics Backend Deployment"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project directory
PROJECT_DIR="/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
cd "$PROJECT_DIR"

echo "📁 Current directory: $PWD"
echo ""

# Function to create requirements.txt if not exists
create_requirements() {
    if [ ! -f "requirements.txt" ]; then
        echo "📝 Creating requirements.txt..."
        cat > requirements.txt << 'EOF'
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
EOF
        echo -e "${GREEN}✓ requirements.txt created${NC}"
    else
        echo -e "${GREEN}✓ requirements.txt already exists${NC}"
    fi
}

# Function to setup git
setup_git() {
    echo ""
    echo "📦 Setting up Git repository..."
    
    if [ ! -d ".git" ]; then
        git init
        echo -e "${GREEN}✓ Git initialized${NC}"
    else
        echo -e "${GREEN}✓ Git already initialized${NC}"
    fi
    
    # Create .gitignore
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << 'EOF'
analytics_data/
__pycache__/
*.pyc
.env
.venv/
venv/
*.log
.DS_Store
*.vsix
node_modules/
EOF
        echo -e "${GREEN}✓ .gitignore created${NC}"
    fi
    
    # Add files
    git add analytics_backend.py requirements.txt .gitignore backend-deploy/ 2>/dev/null || true
    
    # Check if there are changes to commit
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo -e "${YELLOW}⚠ No changes to commit${NC}"
    else
        git commit -m "Add analytics backend for deployment" 2>/dev/null || \
        git commit -m "Update analytics backend" 2>/dev/null || true
        echo -e "${GREEN}✓ Changes committed${NC}"
    fi
}

# Function to deploy to Render
deploy_render() {
    echo ""
    echo "🚀 Deploying to Render.com..."
    echo ""
    echo "Please follow these steps:"
    echo ""
    echo "1. Create GitHub repository:"
    echo "   - Go to https://github.com/new"
    echo "   - Repository name: architector-analytics"
    echo "   - Make it private (recommended for research data)"
    echo "   - Don't initialize with README"
    echo ""
    read -p "Press Enter when repository is created..."
    
    echo ""
    echo "2. Push code to GitHub:"
    read -p "Enter your GitHub username: " github_user
    
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$github_user/architector-analytics.git"
    git branch -M main
    
    echo "Pushing to GitHub..."
    if git push -u origin main; then
        echo -e "${GREEN}✓ Code pushed to GitHub${NC}"
    else
        echo -e "${RED}✗ Failed to push. Please check your credentials${NC}"
        return 1
    fi
    
    echo ""
    echo "3. Deploy on Render:"
    echo "   - Go to https://render.com"
    echo "   - Sign up/login with GitHub"
    echo "   - Click 'New +' → 'Web Service'"
    echo "   - Select 'architector-analytics' repository"
    echo "   - Name: architector-analytics"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: gunicorn -w 4 -b 0.0.0.0:\$PORT analytics_backend:app"
    echo "   - Click 'Create Web Service'"
    echo ""
    echo "4. Add persistent storage:"
    echo "   - In Render dashboard → Your service → Settings"
    echo "   - Scroll to 'Disks'"
    echo "   - Click 'Add Disk'"
    echo "   - Name: analytics-data"
    echo "   - Mount Path: /app/analytics_data"
    echo "   - Size: 1 GB"
    echo "   - Click 'Save Changes' → Manual Deploy"
    echo ""
    echo "5. Your backend will be at:"
    echo "   https://architector-analytics.onrender.com"
    echo ""
}

# Function to deploy to Railway
deploy_railway() {
    echo ""
    echo "🚀 Deploying to Railway.app..."
    
    # Check if railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    echo "Logging into Railway..."
    railway login
    
    echo "Initializing Railway project..."
    railway init
    
    echo "Deploying..."
    railway up
    
    echo ""
    echo "Getting your URL..."
    railway domain
    
    echo -e "${GREEN}✓ Deployed to Railway!${NC}"
}

# Function to deploy to Fly.io
deploy_fly() {
    echo ""
    echo "🚀 Deploying to Fly.io..."
    
    # Check if flyctl is installed
    if ! command -v flyctl &> /dev/null; then
        echo "Installing Fly CLI..."
        curl -L https://fly.io/install.sh | sh
    fi
    
    echo "Logging into Fly.io..."
    flyctl auth login
    
    echo "Launching app..."
    flyctl launch --config backend-deploy/fly.toml --yes
    
    echo "Creating volume for data..."
    flyctl volumes create analytics_data --size 1
    
    echo "Deploying..."
    flyctl deploy
    
    echo -e "${GREEN}✓ Deployed to Fly.io!${NC}"
    
    echo ""
    echo "Your backend URL:"
    flyctl status --json | grep "hostname"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose deployment platform:"
    echo ""
    echo "1) Render.com (⭐ RECOMMENDED - Easy, free, persistent storage)"
    echo "2) Railway.app (Fast, $5 free credit/month)"
    echo "3) Fly.io (Good performance, 3 free VMs)"
    echo "4) Setup only (prepare git, skip deployment)"
    echo "5) Exit"
    echo ""
}

# Main script
create_requirements

while true; do
    show_menu
    read -p "Select option (1-5): " choice
    
    case $choice in
        1)
            setup_git
            deploy_render
            break
            ;;
        2)
            setup_git
            deploy_railway
            break
            ;;
        3)
            setup_git
            deploy_fly
            break
            ;;
        4)
            setup_git
            echo -e "${GREEN}✓ Git setup complete. You can manually deploy later.${NC}"
            break
            ;;
        5)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please choose 1-5.${NC}"
            ;;
    esac
done

echo ""
echo "=================================================="
echo "✅ Deployment process complete!"
echo "=================================================="
echo ""
echo "📝 Next steps:"
echo "1. Copy your backend URL"
echo "2. Update extension files with new URL"
echo "3. Rebuild extension: npm run compile && npx vsce package"
echo "4. Test with: curl YOUR_URL/health"
echo ""
echo "📚 See backend-deploy/README.md for detailed instructions"
echo ""
