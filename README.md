# 🗜️ manzcompression — Multi-Algorithm Archive Engine & GUI

A custom file compression utility and archiver featuring a multi-algorithm backend (`.manz` format), a high-speed command-line interface (`manz_cli.py`), and a user-friendly desktop GUI (`manz_gui.py`).

---

## ⚡ Features

- **📦 Multi-Algorithm Backend (`manz_compressor.py`)**:
  - Supports multiple compression algorithms: `deflate`, `bzip2`, `lzma`, and uncompressed `store`.
  - Configurable compression levels from 1 (fastest) to 9 (maximum ratio).
  - Directory recursion and single-file archiving into standard container streams.
- **🖥️ Desktop GUI (`manz_gui.py`)**:
  - Intuitive graphical interface to browse files, select target directories, adjust compression levels, and monitor progress bars.
- **⚡ Command-Line Tool (`manz_cli.py`)**:
  - Scriptable CLI for batch automation and fast shell archiving/extraction.

---

## 🚀 Quick Start

### Prerequisites
* Python 3.8+ (standard library only; no third-party package dependencies required!)

### CLI Usage
To compress:
```bash
python manz_cli.py -c "path/to/folder" -o "archive.manz" -m lzma -l 9
```

To decompress:
```bash
python manz_cli.py -x "archive.manz" -o "path/to/destination"
```

### GUI Usage
Launch the desktop application:
```bash
python manz_gui.py
```

---

## 📂 File Overview

* **`manz_compressor.py`**: Core compression/decompression engine with format abstractions.
* **`manz_cli.py`**: Command-line interface with flag parsing (`-c`, `-x`, `-m`, `-l`).
* **`manz_gui.py`**: Desktop GUI with visual file pickers, algorithm selectors, and progress tracking.

---

## 📜 License
MIT License. Created by [Manz](https://github.com/SuperManzDev).
