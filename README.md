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
├── wrapped_data.js    # Game statistics data
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

1. Push all files to a GitHub repository
2. Go to repository Settings → Pages
3. Select source branch (usually `main`)
4. Your app will be live at: `https://YOUR_USERNAME.github.io/REPO_NAME`
