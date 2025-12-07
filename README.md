# Sleeper Trades Viewer

A static webpage to visualize trade history from your Sleeper league.

## How to Run Locally

1.  **Generate the Data File**:
    The webpage relies on a `web/data.js` file which contains your trade data. You need to generate this from your JSON file.
    
    Run the Python script:
    ```bash
    python generate_data_js.py
    ```
    By default, this looks for `trades.json` in the current directory.

2.  **Open the Webpage**:
    Navigate to the `web` folder and open `index.html` in your web browser.
    
    *   **Windows**: Double-click `index.html` or right-click -> Open with -> Chrome/Edge/Firefox.
    *   **Mac/Linux**: `open web/index.html`

## How to Change the Input File

If you have a different JSON file (e.g., `my_league_trades.json`), you can specify it when running the generation script:

```bash
python generate_data_js.py my_league_trades.json
```

This will read `my_league_trades.json` and update `web/data.js`. Refresh your browser to see the new data.

## How to Share (Deployment)

To share this with others, you need to host the `web` folder online. Here are a few free and easy options:

### Option 1: GitHub Pages (Recommended)
If you are using Git:
1.  Push this project to a GitHub repository.
2.  Go to the repository **Settings** > **Pages**.
3.  Under **Build and deployment**, select **Source** as `Deploy from a branch`.
4.  Select your branch (usually `main` or `master`) and set the folder to `/web` (if possible) or just `/` if you move everything to the root.
    *   *Note*: GitHub Pages usually serves from the root or `/docs`. You might want to move the contents of `web/` to the root of your repo or a `docs/` folder for easier configuration.
5.  GitHub will give you a link (e.g., `https://username.github.io/repo-name/`).

### Option 2: Netlify Drop
1.  Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2.  Drag and drop the `web` folder onto the page.
3.  Netlify will instantly deploy it and give you a unique URL.
4.  You can claim the site to keep it permanently.

### Option 3: Vercel
1.  Install Vercel CLI: `npm i -g vercel`
2.  Run `vercel` inside the `web` directory.
3.  Follow the prompts.
