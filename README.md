# Kali Teeri Wrapped 2025

A Spotify Wrapped-style web application showcasing Kali Teeri game statistics.

## Quick Start

### Prerequisites

Make sure you have [Node.js](https://nodejs.org/) installed (npm comes with it).

**No installation needed!** Uses `npx` to run directly.

### Running the App

#### Option 1: Local Development (Computer Only)

```bash
npm run dev
```

or directly:

```bash
npx http-server -p 8000 -a localhost -o
```

This will start the server and automatically open your browser at `http://localhost:8000`

#### Option 2: Network Access (Computer + Phone)

```bash
npm start
```

or directly:

```bash
npx http-server -p 8000 -a 0.0.0.0 -o
```

This will:

- Start the server accessible on your network
- Automatically open your browser
- Allow access from any device on the same Wi-Fi

**To access from your phone:**

1. Find your computer's IP address:

   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
   ```

   (Or check your network settings)

2. On your phone, go to: `http://YOUR_IP_ADDRESS:8000`
   - Example: `http://192.168.1.17:8000`

#### Option 3: Server Only (No Auto-Open)

```bash
npm run serve
```

or directly:

```bash
npx http-server -p 8000 -a 0.0.0.0
```

Starts the server without opening a browser automatically.

## Generating Statistics

The statistics are calculated from `data.json` using a Python script. **Stats are calculated once** - you need to run the script manually whenever you want to update the statistics.

### Prerequisites

- Python 3 (usually pre-installed on Mac/Linux)
- Your game data in `data.json`

### Running the Statistics Script

```bash
python3 data.py
```

or

```bash
python data.py
```

This will:
1. Read game data from `data.json`
2. Calculate all statistics for frequent players
3. Print the results to the console

### Updating the Web App

After running `data.py`, you'll see the statistics printed in the terminal. You need to manually copy the relevant statistics into `wrapped_data.js` to update the web app display.

**Note:** The script calculates stats **once per run**. It doesn't automatically update the web app - you run it when you want fresh statistics, then update `wrapped_data.js` with the new data.

### Available Statistics

The script calculates:

**Existing Stats:**
- **The Boldest Bidders**: Average bid points when leading
- **Leader Conversion Rate**: Win percentage when leading
- **Clutch Leaders**: Wins with bids ≥220 points
- **The Most Wanted**: How often each player is called as a teammate
- **The Kingmakers**: Win percentage when playing as teammate
- **The Over-Sellers**: Failed bids (losses when leading)
- **Favorite Partnerships**: Most common leader-teammate combinations
- **Unstoppable Trios**: Best 3-player winning combinations

**New Stats (Added):**
- **The Champions**: Overall win rate (wins as leader OR teammate / total rounds)
- **The Traitors**: Average points lost when playing as teammate
- **Nemesis Tracking**: Worst partnerships (combinations with most losses)

## Features

- 📊 **Interactive Stats**: View game statistics in a beautiful wrapped format
- 📱 **Mobile-First**: Optimized for mobile devices
- 🎨 **Vibrant Design**: Spotify-inspired gradients and animations
- 📈 **Expandable Lists**: Click "Show All" to see complete rankings (top 10)
- ⬆️ **Back to Top**: Quick navigation button
- 🔄 **Swipe Navigation**: Vertical swipe between slides (like Instagram stories)

## File Structure

```
Kali-Teeri/
├── index.html          # Main HTML file
├── style.css          # Styles and animations
├── app.js             # Application logic
├── wrapped_data.js    # Game statistics data (manually updated)
├── data.py            # Python script to calculate statistics
├── data.json          # Raw game data (input for data.py)
└── README.md         # This file
```

## Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## Troubleshooting

- **Port already in use?**
  Edit `package.json` and change the port in the scripts:

  ```json
  "start": "http-server -p 8080 -a 0.0.0.0 -o"
  ```

- **Can't access from phone?**

  - Make sure both devices are on the same Wi-Fi network
  - Check your firewall settings (may need to allow port 8000)
  - Try using your computer's IP address instead of localhost

- **npm/npx command not found?**

  - Install Node.js from [nodejs.org](https://nodejs.org/)
  - npm and npx come bundled with Node.js

- **No need to install!**
  - Using `npx` means no `npm install` required
  - Dependencies are downloaded automatically when needed

## Deployment to GitHub Pages

### Quick Setup:

1. **Create a GitHub repository** (or use an existing one)

2. **Push your files to GitHub:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**

   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **Deploy from a branch**
   - Choose branch: `main` (or `master`)
   - Choose folder: `/ (root)`
   - **IMPORTANT:** Scroll down to "Custom domain" section and **leave it blank** (clear any text if present)
   - Click **Save**

4. **Your app will be live at:**
   - `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
   - Example: `https://johndoe.github.io/kali-teeri-wrapped/`

### Fix Custom Domain Error:

**If you see:** "The custom domain `kali-teeri-wrapped` is not properly formatted"

**Solution:**

1. Go to repository **Settings** → **Pages**
2. Scroll to **Custom domain** section
3. **Delete/clear any text** in the custom domain field (leave it completely blank)
4. Click **Save**

The GitHub Pages URL (`.github.io`) works perfectly - you don't need a custom domain!

### Important Notes:

- **No custom domain needed** - The GitHub Pages URL works perfectly
- **Repository name ≠ Custom domain** - Don't enter your repo name in the custom domain field
- **No build step required** - Since this is a static site, GitHub Pages will serve it directly
- **HTTPS is automatic** - GitHub Pages provides free SSL certificates

### File Structure:

Make sure these files are in the root of your repository:

- `index.html` ✅
- `style.css` ✅
- `app.js` ✅
- `wrapped_data.js` ✅
- `.nojekyll` ✅ (included to prevent Jekyll processing)
