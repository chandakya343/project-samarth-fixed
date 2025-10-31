# Push to GitHub - Instructions

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `project-samarth`
3. Description: `Intelligent Q&A System for Indian Agricultural & Climate Data`
4. Public (checked)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

## Step 2: Push Your Code

Run these commands:

```bash
cd /Users/aryanchandak/projects/project_samarth/project_samarth
git remote set-url origin https://github.com/chandakya343/project-samarth.git
git push -u origin main
```

When prompted for credentials:
- Username: `chandakya343`
- Password: Use your GitHub Personal Access Token (PAT) or GitHub password

## Alternative: Use GitHub CLI

If you have `gh` CLI installed:

```bash
gh auth login
gh repo create project-samarth --public --source=. --remote=origin --push
```

## Step 3: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `chandakya343/project-samarth`
5. Branch: `main`
6. Main file: `streamlit_app.py`
7. Click "Deploy"
8. Go to Settings → Secrets
9. Add secret: `GEMINI_API_KEY` = your API key
10. Redeploy

Your app will be live at: `https://project-samarth.streamlit.app`

