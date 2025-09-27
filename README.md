# 🚀 Python Desktop App Auto-Updater with DevOps
<img src="[docs/diagram.png](https://github.com/Walidbadry/Python-Desktop-App-devops/blob/main/image)" alt="Architecture Diagram" width="500"/>

A **complete end-to-end project** demonstrating how to build a **self-updating Python desktop application** with modern DevOps practices.

This repository shows how to combine:
- 🐍 Python (Desktop App + Updater)
- ⚙️ Jenkins (CI/CD pipeline)
- 🌐 Nginx (Update server)
- 📦 Version Control & Rollback
- 🔄 Automatic Deployment Scripts

---

## 📌 Why This Project?
Managing updates for desktop apps is usually hard. Users often miss updates or developers struggle to deliver patches quickly.

This project solves that problem by:
- Automating builds with **Jenkins**
- Hosting versions on a secure **Nginx server**
- Auto-updating the client with a **Python updater**
- Supporting **rollback** if a release breaks

---

## 🏗 Architecture Overview

```text
                ┌─────────────────────┐
                │     Developer       │
                │   Pushes to GitHub  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │      Jenkins        │
                │  CI/CD Pipeline     │
                └─────────┬──────────┘
                          │
                  Build + Package
                          │
                          ▼
                ┌─────────────────────┐
                │     Server          │
                │ Nginx + deploy.sh   │
                └─────────┬──────────┘
                          │
              latest.json │  versions/
                          │
                          ▼
                ┌─────────────────────┐
                │   Client App        │
                │   updater.py        │
                └─────────────────────┘
---
my_app/
├── app/                # Desktop app source code
│   ├── main.py
│   ├── updater.py
│   └── version.txt
├── deploy.sh           # Deployment script (server-side)
├── nginx.sh            # Auto-setup Nginx config
├── Jenkinsfile         # CI/CD pipeline definition
├── README.md           # Documentation

---
⚙️ How It Works

Build Phase

Jenkins builds your Python app and creates an installer (.exe for Windows, .AppImage for Linux).

Deploy Phase

deploy.sh uploads the new build into /var/www/my_app/versions/<timestamp>/.

Updates latest.json with the latest version + download URL.

Serve Updates

Nginx hosts latest.json and versioned installers.

Example:

http://your-server.com/my_app/latest.json

http://your-server.com/my_app/versions/20250927220045/my_app_installer.exe

Client Auto-Update

On startup, updater.py fetches latest.json.

Compares current version (version.txt) with the latest.

If newer → downloads & runs installer.

Rollback Support

Run:

./deploy.sh rollback <version_id>


latest.json is updated to point back to the chosen version.

🚀 Setup Instructions
1. Server Setup (Nginx)
chmod +x nginx.sh
./nginx.sh


This will:

Create /var/www/my_app/versions

Configure Nginx

Enable serving updates (latest.json + installers)

2. Deploying a New Version
chmod +x deploy.sh
./deploy.sh deploy my_app_installer.exe


This will:

Create a timestamped folder under versions/

Copy installer inside

Update latest.json with new download URL

3. Rollback to Previous Version
./deploy.sh rollback 20250927220045


This will:

Reset latest.json to the old version

Keep all builds available under versions/

🖥 Client-Side (Updater)

Inside your desktop app, updater.py will:

Fetch latest update info:

{
  "version": "20250927220045",
  "download_url": "http://your-server.com/my_app/versions/20250927220045/my_app_installer.exe"
}


Compare with version.txt

Download + run installer if new version exists

Run manually:

python app/updater.py

🔄 CI/CD with Jenkins

Pipeline (Jenkinsfile) flow:

Pull code from GitHub

Build & package app

Upload installer to server

Run deploy.sh remotely

Update Nginx & latest.json

This ensures every Git push → new version auto-deployed 🚀

🔑 Security & Best Practices

Store secrets (SSH keys, server credentials, update URLs) in Jenkins Credentials Manager

Use HTTPS on Nginx with Let’s Encrypt

Keep only the last few versions, clean up old ones

Monitor deployments with Jenkins logs

📷 Example Workflow

Push code → GitHub

Jenkins builds → Deploys to server

Nginx hosts → latest.json updated

User opens app → Auto-updater checks → New version installed

📜 License

MIT License – free to use and modify.

🤝 Contributions

Fork this repo

Submit Pull Requests

Open issues for improvements

🙌 Author

Built with ❤️ as a DevOps + Python integration project.
Showcases CI/CD, automation, and desktop app delivery in real-world workflows.


---

👉 Do you want me to also **create a LinkedIn-style diagram (PNG/Markdown)** for the README so it looks more professional and attractive on your GitHub profile?

---
## ⚙️ How It Works
1. **Build:** Jenkins packages the app.  
2. **Deploy:** `deploy.sh` uploads the new version to `/var/www/my_app/versions/`.  
3. **Publish:** `latest.json` is updated with the latest version and download URL.  
4. **Client Update:** On startup, `updater.py` checks for updates and downloads new builds.  
5. **Rollback:** Use `deploy.sh rollback <version>` to revert.  

---

## 🔧 Setup Instructions

### 1. Server Setup
```bash
chmod +x nginx.sh
./nginx.sh
