# Cockatoo Edge — A Dynamic Discord Moderation Platform

> [!IMPORTANT]
> Work in progress — NOT production ready.

## Setup

**Supported Environments:**

```csv
GNU Linux
Docker
Windows (requires manual deployment)
MacOS (? - Untested)
```

**Deployment:**

```bash
N/A
```

## How it works

Cockatoo Edge consumes a public database published by Cockatoo Core (a proprietary, real-time ML-powered component of the Cockatoo family) to identify and mitigate known threats. 

The Edge deployment minimizes computational overhead and improves reaction times by handling decisions locally. Note that Discord API gateway rate limits and network latency still apply (just like any other bot).

## Contributing

Issues
- Search for existing reports before opening a new issue.
- Ensure the problem is reproducible and not caused by bad configuration.
- Include steps to reproduce, expected vs. actual behavior, and any relevant logs or screenshots.

Pull requests
- Explain the goal of the change and reference any related issues.