# Crypto Finance Education Blog

This project sets up an automated blog for generating high-value, SEO-friendly content related to cryptocurrency, finance, and making money. It leverages Poe for content generation, Jekyll for static site generation, and GitHub Actions for continuous automation and deployment to GitHub Pages.

## Features

*   **Automated Content Generation:** Generates blog posts using the Poe API based on predefined topics and structures.
*   **SEO-Friendly:** Content is designed to be SEO-optimized with catchy titles, descriptions, categories, and tags.
*   **Jekyll Integration:** Generated posts are formatted as Jekyll Markdown files with appropriate front matter.
*   **GitHub Pages Deployment:** Automatically builds and deploys the blog to GitHub Pages via GitHub Actions.
*   **Daily Posting:** Configured to generate 1-2 new posts daily.

## Setup

### 1. Poe API Key

To use this automation, you'll need a Poe API key.

*   **Local Development:** Create a `.env` file in the root of this project and add your Poe API key:

    ```
    POE_API_KEY=YOUR_POE_API_KEY_HERE
    ```

    **Remember to replace `YOUR_POE_API_KEY_HERE` with your actual Poe API key.** This `.env` file is already added to `.gitignore` to prevent accidental commits.

*   **GitHub Actions:** Add your Poe API key as a GitHub Secret named `POE_API_KEY` in your repository settings:
    1.  Go to your repository on GitHub.
    2.  Click on "Settings".
    3.  In the left sidebar, click on "Secrets and variables" > "Actions".
    4.  Click on "New repository secret".
    5.  For "Name", enter `POE_API_KEY`.
    6.  For "Secret", paste your actual Poe API key.
    7.  Click "Add secret".

### 2. Install Dependencies

Ensure you have Python installed. Then, install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Usage

### Local Content Generation

You can generate a single blog post locally using the `generate_post.py` script:

```bash
python generate_post.py "Your Desired Blog Post Topic"
```

This will create a new Markdown file in the `_posts` directory.

### Automated Workflow (GitHub Actions)

The `.github/workflows/crypto_finance_education.yml` file configures a GitHub Actions workflow that runs daily at 10:00 UTC. This workflow will:

1.  Set up a Python environment.
2.  Install dependencies from `requirements.txt`.
3.  Generate multiple blog posts using `generate_post.py` with predefined topics.
4.  Deploy the generated posts to your GitHub Pages site.

To trigger a manual run of the workflow for testing:

1.  Go to your repository on GitHub.
2.  Click on the "Actions" tab.
3.  Select the "Crypto Finance Education" workflow.
4.  Click "Run workflow" and then "Run workflow" again to confirm.

## Project Structure

*   `_posts/`: Contains the generated Jekyll blog posts.
*   `.github/workflows/crypto_finance_education.yml`: GitHub Actions workflow for automation and deployment.
*   `generate_post.py`: Python script for generating blog post content via Poe.
*   `requirements.txt`: Python dependencies.
*   `.env`: Local environment variables (ignored by Git).
*   `README.md`: This file.