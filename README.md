# Cockatoo Edge
**A Dynamic Discord Moderation Platform**

> [!IMPORTANT]
> Work in progress — NOT production ready.

---

## Setup

**Supported Environments:**

Definitely works:

* `GNU/Linux` - Tested on:
```
Ubuntu Server 22.04 (bare metal | Docker)
Ubuntu Server 24.04 (Docker)
Ubuntu Desktop 24.04 (bare metal | Docker)
Debian 13 (bare metal | Docker)
```

* `Windows` - Tested on:
```
Windows 11 - 24H2 (bare metal)
Windows 10 - 22H2 (bare metal)
```

* `Docker` - Tested on:
```
Docker version 28.3.3
```

Probably works (untested):

* `BSD`
* `MacOS`

Does not work:
`Unknown` 

**Deployment:**

```bash
N/A
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