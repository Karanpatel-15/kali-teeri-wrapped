# GitHub Pages Setup Guide

## Fix Custom Domain Error

If you're seeing this error:

> "The custom domain `kali-teeri-wrapped` is not properly formatted"

**Solution: Remove the custom domain setting**

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Scroll down to **Custom domain**
4. **Clear the field** (delete `kali-teeri-wrapped` if it's there)
5. Click **Save**

Your site will work perfectly at: `https://YOUR_USERNAME.github.io/kali-teeri-wrapped/`

**Note:** Custom domains are only needed if you own a domain name (like `example.com`). For GitHub Pages, you can use the free `.github.io` URL which works great!

## Quick Deployment Steps

1. **Initialize git (if not done):**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages:**

   - Repository → **Settings** → **Pages**
   - Source: **Deploy from a branch**
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
   - **Leave Custom domain blank**
   - Click **Save**

4. **Wait 1-2 minutes** for GitHub to build your site

5. **Visit your site:**
   `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

## Files Included

✅ `.nojekyll` - Prevents Jekyll processing (important for static sites)
✅ All HTML, CSS, and JS files in root directory
✅ Proper file structure for GitHub Pages

## Troubleshooting

- **404 Error?** Make sure `index.html` is in the root directory
- **Custom domain error?** Clear the custom domain field in Settings → Pages
- **Site not updating?** Wait a few minutes and hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
