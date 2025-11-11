# Local Development

## Quick Start

To test this helpdesk site locally (required due to CORS restrictions):

### Option 1: Python Server (Recommended)
```bash
cd docs
python3 server.py
```
Then open: http://localhost:8000

### Option 2: Python Simple Server
```bash
cd docs
python3 -m http.server 8000
```
Then open: http://localhost:8000

### Option 3: Node.js (if you have Node installed)
```bash
cd docs
npx http-server -p 8000
```
Then open: http://localhost:8000

## Why?

Browsers block loading local files (like `list.json` and markdown files) when opening HTML directly from the file system due to CORS security restrictions. Running a local server solves this issue.

**Note:** This is only needed for local testing. GitHub Pages automatically serves files over HTTP, so this works without any server when deployed.

