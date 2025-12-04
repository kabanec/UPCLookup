# Simple Step-by-Step Deployment Guide

## What I Did
I created files that will automatically deploy your app to Render.com whenever you push code to GitHub.

## Step 1: Run /login in Claude Code
**Do this first!** Type `/login` in the Claude Code window and authenticate.

---

## Step 2: Get Your Render API Key

1. Open this link in your browser: https://dashboard.render.com/account/api-keys
2. Click the blue **"Create API Key"** button
3. Type a name like "GitHub Deploy"
4. Click **Create API Key**
5. **COPY the key that appears** (it looks like: `rnd_abc123xyz...`)
6. Save it in a notepad - you'll need it in Step 3

---

## Step 3: Add Secrets to GitHub

1. Open this link: https://github.com/kabanec/UPCLookup/settings/secrets/actions
   (If you don't have access, you need to be the repo owner or have admin rights)

2. Click **"New repository secret"** button

3. **First Secret:**
   - In the "Name" field, type exactly: `RENDER_API_KEY`
   - In the "Secret" field, paste the key you copied in Step 2
   - Click **"Add secret"**

4. Click **"New repository secret"** again

5. **Second Secret:**
   - In the "Name" field, type exactly: `RENDER_SERVICE_ID`
   - In the "Secret" field, type exactly: `srv-d0vlo6jipnbc7381tb60`
   - Click **"Add secret"**

You should now see 2 secrets listed.

---

## Step 4: Push Changes to GitHub

After running `/login`, tell me:
**"Please commit and push all the CI/CD changes to GitHub"**

I will run these commands for you:
```bash
git add .github/ render.yaml .gitignore DEPLOYMENT.md SIMPLE_DEPLOYMENT_STEPS.md
git commit -m "Add CI/CD pipeline for automatic deployment"
git push origin master
```

---

## Step 5: Watch It Deploy!

1. GitHub will automatically start deploying. Check here:
   https://github.com/kabanec/UPCLookup/actions

2. You'll see a workflow running called "Deploy to Render"

3. After GitHub finishes, check Render:
   https://dashboard.render.com/web/srv-d0vlo6jipnbc7381tb60/deploys

4. Your app will deploy automatically!

---

## What Happens Next?

**Every time you push code to GitHub**, it will automatically:
1. Run the GitHub Action
2. Deploy to Render
3. Your app updates automatically!

---

## If You Get Stuck

**Problem: Can't access GitHub settings**
- You need to be the repository owner or have admin access
- Check with the repo owner

**Problem: Render API key not working**
- Make sure you copied the ENTIRE key (starts with `rnd_`)
- Try creating a new API key

**Problem: Deployment fails**
- Check GitHub Actions logs: https://github.com/kabanec/UPCLookup/actions
- Check Render logs: https://dashboard.render.com/web/srv-d0vlo6jipnbc7381tb60/logs

**Problem: Claude Code says "OAuth expired"**
- Type `/login` in Claude Code and re-authenticate

---

## Quick Checklist

- [ ] Run `/login` in Claude Code
- [ ] Get Render API key from https://dashboard.render.com/account/api-keys
- [ ] Add `RENDER_API_KEY` secret to GitHub
- [ ] Add `RENDER_SERVICE_ID` secret to GitHub (value: `srv-d0vlo6jipnbc7381tb60`)
- [ ] Ask Claude to commit and push changes
- [ ] Watch deployment on GitHub Actions
- [ ] Verify app is running on Render

---

## Current Status

✅ CI/CD files created by Claude
⏳ Waiting for you to complete Steps 1-4
