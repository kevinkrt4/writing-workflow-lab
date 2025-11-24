# WebWork Project: Developer Setup Guide

Welcome! 🎉  
This guide will walk you (Jordan) through setting up your local development environment so you can work on the site and contribute changes.

You do **not** need to publish the live site yourself — Kevin handles deployment.  
You’ll be working directly in the `working_site` directory to edit and improve HTML, CSS, and related files.

---

## 1. Prerequisites

You’ll need:

- **Git**
  - On macOS: run `git --version`.  
    - If it prompts you to install Command Line Developer Tools, accept it.
- **Python 3** *(optional, used by some tools)*
  - Run `python3 --version`.  
    - If you don’t have it, install from python.org or `brew install python`.
- **GitHub account**
  - Your username is `jordanjt4`.
- **Write access to the `webwork` repo**
  - Kevin will invite you. You must accept the invitation before you can clone or push.

---

## 2. Set up SSH access to GitHub

You’ll use SSH so you can push/pull without typing a password.

### 2.1 Generate an SSH key

In Terminal:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

If asked:
- `Enter a file in which to save the key` → press Enter to accept the default (`~/.ssh/id_ed25519`)
- `Enter passphrase` → you can just press Enter for no passphrase (easier day to day)

This creates two files:
- `~/.ssh/id_ed25519`        ← private key (keep this secret; do not send it to anyone)
- `~/.ssh/id_ed25519.pub`    ← public key (safe to upload to GitHub)

### 2.2 Add your key to the SSH agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 2.3 Add the public key to GitHub

Show your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (it’s one long line starting with `ssh-ed25519`).

Then:
1. Go to GitHub in your browser.
2. Click your profile picture → **Settings**.
3. Go to **SSH and GPG keys**.
4. Click **New SSH key**.
   - Title: something like `MacBook` or `Workstation`
   - Key type: Authentication Key
   - Key: paste the line you copied
5. Save.

### 2.4 Verify SSH is working

Run:

```bash
ssh -T git@github.com
```

You should see something like:

```text
Hi jordanjt4! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see that, GitHub recognizes you and your key is good.

---

## 3. Clone the repository

You’ll use the **Terminal** (on macOS) to enter the commands in this section.  
To open Terminal, press **Command + Space**, type **Terminal**, and press **Enter**.


Pick a folder where you want the project to live. For example:

```bash
cd ~/Documents
mkdir GitHub
cd GitHub
```

Now clone Kevin’s private repo (this is the main working repo):

```bash
git clone git@github.com:kevinkrt4/webwork.git
cd webwork
```

If that works, you’re in.

You should now see something like:

```text
drafts/
tools/
working_site/
publish/
.gitignore
```

You’ll be working mainly in `working_site/`:
- Edit HTML files directly.
- Update CSS under `resources/css/`.
- Replace or add images under `resources/images/`.
- Update or add JS files under `resources/js/`.

The `tools/` directory contains internal utilities used for deployment. You don’t need to run those.

---

## 4. Commit and push your changes

Once your content looks good locally and you’re happy with it:

1. Stage your changes:
   ```bash
   git add working_site/
   ```

2. Commit:
   ```bash
   git commit -m "Update site layout and content"
   ```

3. Push to GitHub:
   ```bash
   git push origin main
   ```

This updates the private `webwork` repo on GitHub so Kevin can review and deploy.

⚠️ IMPORTANT:  
Do not commit secrets (tokens, passwords, API keys).  
If a file contains private credentials, DO NOT push it.

---

## 5. Deployment (who does it)

Publishing to the public site (`kevinkrt4.github.io`) is handled by Kevin.  
He runs:

```bash
./tools/deploy.sh
```

That script:
- Copies everything from `working_site/`
- Builds a clean snapshot
- Pushes it to the public GitHub Pages site

You normally do not need to run `deploy.sh`.

---

## 6. Quick reference / cheat sheet

### One-time setup
```bash
# generate ssh key
ssh-keygen -t ed25519 -C "your_email@example.com"

# add to agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# copy public key and add it to GitHub
cat ~/.ssh/id_ed25519.pub

# verify
ssh -T git@github.com
```

### Clone the repo
```bash
cd ~/Documents
mkdir GitHub
cd GitHub
git clone git@github.com:kevinkrt4/webwork.git
cd webwork
```

### Save your work to GitHub
```bash
git add working_site/
git commit -m "Update site content and design"
git push origin main
```

---

## 7. Troubleshooting

If you hit:
- `Permission denied (publickey)` → your SSH key probably isn’t added to GitHub or you didn’t accept the repo invite yet.
- `fatal: repository not found` → you don’t have access to `kevinkrt4/webwork` yet (ask Kevin to confirm the invite).
- Updates don’t appear in GitHub → make sure you’re committing and pushing to the `main` branch.

---

You’re all set!  
You can edit HTML, CSS, and other web resources directly in `working_site/`, test locally with VS Code’s Live Server extension, and push updates to GitHub. Kevin will handle deploying changes to the live site.

