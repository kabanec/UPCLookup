# Deployment Guide

This document explains how to set up CI/CD for the UPC Lookup application to deploy automatically to Render.com.

## Overview

The application uses GitHub Actions to automatically deploy to Render.com whenever code is pushed to the `master` or `main` branch.

## Prerequisites

1. GitHub repository: https://github.com/kabanec/UPCLookup
2. Render.com account with an existing web service
3. Render API key
4. Render Service ID

## Setup Instructions

### 1. Get Your Render API Key

1. Go to https://dashboard.render.com/account/api-keys
2. Click "Create API Key"
3. Give it a name (e.g., "GitHub Actions Deploy")
4. Copy the generated API key (you'll need this for step 2)

### 2. Get Your Render Service ID

Your service ID is: `srv-d0vlo6jipnbc7381tb60`

(You can find this in your Render dashboard URL: https://dashboard.render.com/web/**srv-d0vlo6jipnbc7381tb60**/deploys/...)

### 3. Add GitHub Secrets

1. Go to your GitHub repository: https://github.com/kabanec/UPCLookup
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

   **Secret 1:**
   - Name: `RENDER_API_KEY`
   - Value: [Your Render API key from step 1]

   **Secret 2:**
   - Name: `RENDER_SERVICE_ID`
   - Value: `srv-d0vlo6jipnbc7381tb60`

### 4. Configure Environment Variables in Render

1. Go to your Render service: https://dashboard.render.com/web/srv-d0vlo6jipnbc7381tb60
2. Go to **Environment** tab
3. Add the following environment variable:
   - Key: `BARCODE_API_KEY`
   - Value: [Your Barcode Lookup API key]

## How It Works

### Automatic Deployment

1. When you push code to `master` or `main` branch, GitHub Actions automatically triggers
2. The workflow installs dependencies and runs any tests
3. It triggers a deployment on Render using the Render API
4. Render pulls the latest code and deploys your application

### Manual Deployment

You can also trigger a deployment manually:

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select **Deploy to Render** workflow
4. Click **Run workflow** → **Run workflow**

## Files Created

- `.github/workflows/deploy.yml` - GitHub Actions workflow configuration
- `render.yaml` - Render deployment configuration (optional, for Infrastructure as Code)
- `DEPLOYMENT.md` - This documentation file

## Deployment Configuration

### GitHub Actions Workflow (`.github/workflows/deploy.yml`)

- **Triggers**: Push to master/main branch, or manual trigger
- **Steps**:
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies
  4. Run tests (placeholder for future tests)
  5. Deploy to Render via API
  6. Show success notification

### Render Configuration (`render.yaml`)

- **Service Type**: Web service
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Python Version**: 3.11.0
- **Plan**: Free tier

## Monitoring Deployments

### Via GitHub

1. Go to https://github.com/kabanec/UPCLookup/actions
2. Click on the latest workflow run
3. View deployment status and logs

### Via Render

1. Go to https://dashboard.render.com/web/srv-d0vlo6jipnbc7381tb60/deploys
2. View deployment history and logs
3. Monitor application health

## Troubleshooting

### Deployment Fails

1. Check GitHub Actions logs for errors
2. Verify GitHub secrets are set correctly
3. Check Render deployment logs
4. Ensure `BARCODE_API_KEY` is set in Render environment variables

### Application Not Starting

1. Check Render logs for startup errors
2. Verify `requirements.txt` includes all dependencies
3. Ensure `gunicorn` is in `requirements.txt`
4. Check that environment variables are set correctly

### API Key Issues

If you see errors about missing API keys:
1. Go to Render dashboard → Environment
2. Verify `BARCODE_API_KEY` is set
3. Restart the service

## Testing Locally Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export BARCODE_API_KEY="your-api-key"

# Run locally
python app.py

# Or run with gunicorn (production server)
gunicorn app:app
```

## Deployment Checklist

Before deploying, ensure:

- [ ] All changes are committed to git
- [ ] `.env` file is in `.gitignore` (don't commit secrets!)
- [ ] `requirements.txt` is up to date
- [ ] GitHub secrets are configured
- [ ] Render environment variables are set
- [ ] Code works locally

## Next Steps

1. **Add Tests**: Create a `tests/` directory and add unit tests
2. **Add Linting**: Add flake8 or pylint to workflow
3. **Add Notifications**: Configure Slack/Discord notifications for deployments
4. **Add Staging**: Create a staging environment for testing before production
5. **Add Health Checks**: Implement `/health` endpoint for monitoring

## Support

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Render Documentation: https://render.com/docs
- Repository: https://github.com/kabanec/UPCLookup

## Security Notes

- Never commit API keys or secrets to the repository
- Use GitHub Secrets for sensitive data
- Keep `.env` in `.gitignore`
- Rotate API keys regularly
- Use environment-specific configurations
