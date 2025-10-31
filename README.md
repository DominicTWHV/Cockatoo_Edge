# Cockatoo Edge
**A Dynamic Discord Moderation Platform**

> [!IMPORTANT]
> Work in progress — NOT production ready.

[![CodeQL](https://github.com/DominicTWHV/Cockatoo_Edge/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/DominicTWHV/Cockatoo_Edge/actions/workflows/github-code-scanning/codeql)

---

## Deployment:

**Docker (Recommended):**

Install dependencies:

```bash
sudo apt update
sudo apt install docker.io screen -y

sudo usermod aG docker $USER #optional, add current user to docker group
exit #you need to start a new shell session for changes to take effect
```

Clone the repository

```bash
git clone https://github.com/DominicTWHV/Cockatoo_Edge.git
cd Cockatoo_Edge
```

Edit the environment variables

```bash
cp example.env .env
nano .env
```

Insert your Discord bot token into the `.env` file, then use `ctrl+o ctrl+x` to save and quit.

Next, configure settings, they are located within Cockatoo_Edge/edge/registry with a `.py` suffix. This step is optional, default settings will work fine out of the box.

Use the provided Docker build script to automate the build process

```bash
./setup_docker.sh -b -t -c
```

Run the bot in a screen session

Optionally, put this line into a bash file and use crontab to automatically start the bot upon reboot.

```bash
screen -dmS cockatoo docker run cockatoo_edge:latest
```

**Bare Metal:**

Clone the repository

```bash
git clone https://github.com/DominicTWHV/Cockatoo_Edge.git
cd Cockatoo_Edge
```

We provide a streamlined bare metal deployment script

```bash
./setup_raw.sh
```

Next, edit your `.env` file to include the bot token

```bash
nano .env
```

Finally, use a screen session to run the bot:

```bash
screen -dmS cockatoo python3 main.py
```

---

## How it works

Cockatoo Edge consumes a public database published by Cockatoo Core (a proprietary, real-time ML-powered component of the Cockatoo family) to identify and mitigate known threats. 

The Edge deployment minimizes computational overhead and improves reaction times by handling decisions locally.

---

## Contributing

Issues
- Search for existing reports before opening a new issue.
- Ensure the problem is reproducible and not caused by bad configuration.
- Include steps to reproduce, expected vs. actual behavior, and any relevant logs or screenshots.

Pull requests
- Explain the goal of the change and reference any related issues.
