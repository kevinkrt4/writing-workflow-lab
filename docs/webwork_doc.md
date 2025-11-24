# GitHub Website Development and Deployment Guide

## Introduction

This document summarizes the complete setup and workflow for maintaining and publishing your website using two GitHub repositories:

- **webwork (private):** your local workspace for drafts, testing, and development.
- **kevinkrt4.github.io (public):** your GitHub Pages site for public deployment.

It explains how to configure your environment, convert and test content locally, and publish updates to your live site with one command.

---

## Table of Contents

1. [GitHub Remote Repository Setup Summary](#github-remote-repository-setup-summary)
   1. [Create and Organize Repositories](#create-and-organize-repositories)
   2. [Local Directory Structure](#local-directory-structure)
   3. [Configure Git and Identity](#configure-git-and-identity)
   4. [Set Up SSH Authentication](#set-up-ssh-authentication)
   5. [Configure Remotes](#configure-remotes)
   6. [Deploy Script Workflow](#deploy-script-workflow)
   7. [GitHub Pages Configuration](#github-pages-configuration)
   8. [Verification](#verification)
   9. [Final State](#final-state)
2. [Workflow Summary: Making and Deploying Changes](#workflow-summary-making-and-deploying-changes)
   1. [Edit Text Source Files](#edit-text-source-files)
   2. [Convert Text to HTML](#convert-text-to-html)
   3. [Preview Changes Locally](#preview-changes-locally)
   4. [Commit Changes to Webwork](#commit-changes-to-webwork)
   5. [Deploy the Updated Site](#deploy-the-updated-site)
   6. [Verify Live](#verify-live)
   7. [Deployment Flow Recap](#deployment-flow-recap)

---

## GitHub Remote Repository Setup Summary

### 1. Create and Organize Repositories
- **Private repo (`webwork`):** contains your source files, scripts, and draft content.
- **Public repo (`kevinkrt4.github.io`):** serves as your GitHub Pages website, hosted remotely on GitHub.
- The workflow: edit and test in `webwork`, then publish to `kevinkrt4.github.io` using the deploy script.

### 2. Local Directory Structure

```
Documents/
└── GitHub/
    └── webwork/
        ├── drafts/
        ├── tools/
        │   ├── deploy.sh
        │   ├── txt2html.py
        │   └── serve.py
        ├── working_site/
        └── publish/
```

- `drafts/`: working text files and notes (not published)
- `tools/`: utility scripts for conversion, testing, and deployment
  - `txt2html.py`: converts text files into HTML using a standard header and paragraph formatting
  - `serve.py`: starts a local Python web server to preview the site before deployment
  - `deploy.sh`: builds and deploys your working site to the public GitHub Pages repository
- `working_site/`: final HTML and resource files ready for testing
- `publish/`: temporary deployment area created by the script

### 3. Configure Git and Identity

```
git config --global user.name "Kevin Thompson"
git config --global user.email "krt444@proton.me"
```

Default editor: **vim** (installed via macOS Command Line Developer Tools)

### 4. Set Up SSH Authentication

```
ssh-keygen -t ed25519 -C "krt444@proton.me"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Add your public key to GitHub under *Settings → SSH and GPG keys → New SSH key*.
Verify connection:

```
ssh -T git@github.com
```

### 5. Configure Remotes

```
git remote set-url origin git@github.com:kevinkrt4/webwork.git
```

In your deploy script:

```
git remote add origin git@github.com:kevinkrt4/kevinkrt4.github.io.git
```

### 6. Deploy Script Workflow (`deploy.sh`)

```
./tools/deploy.sh
```

Confirmation prompt:

```
About to deploy working_site to PUBLIC internet. Continue? (y/N)
```

### 7. GitHub Pages Configuration

Enable Pages for `kevinkrt4.github.io` → **Settings → Pages → Source: main branch**.

Live site: [https://kevinkrt4.github.io](https://kevinkrt4.github.io)

### 8. Verification

- SSH authentication verified (no login prompts)
- `deploy.sh` publishes site
- Local testing works via `serve.py`
- HTML generated via `txt2html.py`

### ✅ 9. Final State

- **Private:** `webwork` for writing, testing, and conversion.
- **Public:** `kevinkrt4.github.io` for live site.
- One-command publishing via `./tools/deploy.sh`.

---

## Workflow Summary: Making and Deploying Changes

### 1. Edit Text Source Files

```
webwork/drafts/
```

### 2. Convert Text to HTML

```
python3 tools/txt2html.py drafts/StarbucksNotebook1.txt working_site/StarbucksNotebook1.html
```

This:

- Adds your standard HTML header
- Wraps paragraphs in `<p>` tags
- Writes the new `.html` into `working_site/`

### 3. Preview Changes Locally

```
python3 tools/serve.py
```

Visit: [http://localhost:8000](http://localhost:8000)

Check that styling, links, and images work as expected.

### 4. (Optional) Commit Changes to `webwork`

```
git add drafts/StarbucksNotebook1.txt working_site/StarbucksNotebook1.html
git commit -m "Update StarbucksNotebook1 and regenerate HTML"
git push origin main
```

### 5. Deploy the Updated Site Publicly

```
./tools/deploy.sh
```

When prompted:

```
About to deploy working_site to PUBLIC internet. Continue? (y/N)
```

Type `y` and press Enter.

The script:

1. Copies `working_site/` → `publish/`
2. Creates a temporary git repo in `publish/`
3. Commits that snapshot
4. Pushes it to `kevinkrt4.github.io` via SSH
5. Removes `.git` from `publish/` so that folder is just static files

### 6. Verify Live

Visit: [https://kevinkrt4.github.io](https://kevinkrt4.github.io)

### ✅ 7. Deployment Flow Recap

1. Edit `.txt` in `drafts/`
2. Run `txt2html.py` → new `.html` in `working_site/`
3. Preview locally with `serve.py`
4. (Optional) Commit/push to `webwork`
5. Run `./tools/deploy.sh`
6. Check your live site

