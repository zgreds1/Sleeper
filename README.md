# Sleeper Trades Viewer

A static webpage to visualize trade history from your Sleeper league.

## How to Run Locally

1.  **Generate the Data File**:
    The webpage relies on a `docs/data.js` file which contains your trade data. You need to generate this from your JSON file.
    
    Run the Python script:
    ```bash
    python generate_data_js.py
    ```
    By default, this looks for `trades.json` in the current directory and outputs to `docs/data.js`.

2.  **Open the Webpage**:
    Navigate to the `docs` folder and open `index.html` in your web browser.
    
    *   **Windows**: Double-click `index.html` or right-click -> Open with -> Chrome/Edge/Firefox.
    *   **Mac/Linux**: `open docs/index.html`

## How to Change the Input File

If you have a different JSON file (e.g., `my_league_trades.json`), you can specify it when running the generation script:

```bash
python generate_data_js.py my_league_trades.json
```

This will read `my_league_trades.json` and update `docs/data.js`. Refresh your browser to see the new data.

## How to Share (Deployment)

To share this with others, you need to host the `docs` folder online.

### Option 1: GitHub Pages (Recommended)
1.  **Push your changes to GitHub**: Ensure the `docs` folder is committed and pushed to your repository.
2.  Go to the repository **Settings** > **Pages**.
3.  Under **Build and deployment**, select **Source** as `Deploy from a branch`.
4.  Select your branch (usually `main` or `master`) and set the folder to `/docs`.
5.  Click **Save**.
6.  GitHub will give you a link (e.g., `https://username.github.io/repo-name/`).

**Note**: If you see the README instead of the app, ensure you have pushed the `docs` folder and that `docs/index.html` exists in your repository. I have added a `.nojekyll` file to the `docs` folder to prevent build issues.

### Option 2: Netlify Drop
1.  Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2.  Drag and drop the `docs` folder onto the page.
3.  Netlify will instantly deploy it and give you a unique URL.
