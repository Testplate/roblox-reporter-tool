# Roblox Asset Reporting Tool

A high-performance, multi-threaded Python utility designed for automated reporting of inappropriate assets on the Roblox platform. This tool is built with a focus on speed, reliability, and ease of use, featuring automatic region unlocking, proxy rotation, and real-time status tracking.

**Note**: This repository is published for **educational purposes and vulnerability research**. It is intended to assist developers in identifying and patching similar reporting logic flaws. This project has no harmful intent and is not intended for abusive use.

## 🚀 Features

- **Multi-Threaded Performance**: Leverages Python's `ThreadPoolExecutor` for concurrent reporting across multiple accounts.
- **Automatic Region Unlocking**: Automatically authorizes session cookies for use in different regions before reporting.
- **Proxy Support & Rotation**: Supports authenticated HTTP/HTTPS proxies with automatic rotation and URL-encoded credential handling.
- **Session Persistence**: Saves successfully unlocked cookies to a separate file for future use.
- **Dynamic Comment Generation**: Uses a natural language randomization engine to create unique, human-like report comments.
- **Real-Time Feedback**: ANSI-colored terminal output providing instant updates on authorization, reporting progress, and connection status.
- **Flexible Connection Modes**: Option to run via local connection or through a proxy list.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone http://github.com/Testplate/roblox-reporter-tool.git
   cd roblox-reporter-tool
   ```

2. **Install Dependencies**:
   This tool requires the `requests` library.
   ```bash
   pip install requests
   ```

## ⚙️ Configuration

Populate the following text files in the root directory:

- **`cookies.txt`**: Add your `.ROBLOSECURITY` cookies (one per line).
- **`proxies.txt`** (Optional): Add your proxies in `username:password@ip:port` format.
- **`comment.txt`**: Add base report messages. The tool will randomize these for each submission.

## 📖 Usage

Run the script using Python:

```bash
python roblox_reporter.py
```

1. **Connection Mode**: If proxies are detected, you will be prompted to enable or disable Proxy Mode.
2. **Target ID**: Enter the numeric **Game ID** of the asset you wish to report.
3. **Execution**: The tool will initialize threads and begin the reporting cycle.

## ⚠️ Disclaimer

This tool is provided for **educational and research purposes only**. It is shared to help identify and patch potential exploits in automated systems. The author is not responsible for any misuse or violations of the Roblox Terms of Service. Use this tool responsibly and at your own risk.

---
**Made by Rio**
