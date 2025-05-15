# 🐳 Python Docker Debugger for BPER Client

This repository provides a working VS Code + Docker + debugpy setup to run and debug the `bper-client.py` script with breakpoints and dynamic CLI arguments.

## ✅ Requirements

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- VS Code extensions:
  - Python (by Microsoft)
  - Docker (by Microsoft)

---

## 🧱 Project Structure

```
.
├── app/
│   └── secops/clients/cli/bper-client.py  # Main script
├── .vscode/launch.json                    # VS Code debug config
├── docker-compose.yml                     # Dev container
├── Dockerfile                             # Image with debugpy
├── requirements.txt
└── config/
    └── config.example.py                  # Template config (rename to config.py)
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone git@github.com:<your-username>/bper-client-debug.git
cd bper-client-debug
```

### 2. Ask For a Working and place it @ 


### 3. Build and launch the container

```bash
docker-compose up --build
```

The container will:
- Install dependencies
- Run `bper-client.py`
- Start `debugpy` and wait for VS Code to attach

---

### 4. Attach the debugger

1. Open VS Code in this folder
2. Go to **Run & Debug (Ctrl+Shift+D)**
3. Select `Attach to: bper-client`
4. Click ▶️ **Start Debugging**
5. Set breakpoints in `app/secops/clients/cli/bper-client.py`

---

## 🔁 Run with different arguments

To run the script with different options (e.g. `--cyberark "safes list"`):

```bash
DEBUG_SCRIPT='secops/clients/cli/bper-client.py --cyberark "safes list"' docker-compose up
```

Or modify `docker-compose.yml`:

```yaml
environment:
  DEBUG_SCRIPT: secops/clients/cli/bper-client.py --cyberark "safes list"
```

---

## 🧰 Developer Notes

- Line endings are normalized to **LF** for Linux compatibility
- `config/config.py` is `.gitignore`d by default
- Use `requirements.txt` to manage Python deps (e.g. debugpy, Django)

---

## 📦 Rebuild Tips

If you make changes to the Dockerfile or dependencies:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## 📄 License

MIT — feel free to fork and adapt.
