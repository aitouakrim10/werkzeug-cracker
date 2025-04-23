# Werkzeug PIN Generator


```text
 __          __             _
 \ \        / /            | |
  \ \  /\  / /   ___  _ __ | | __ ____  ___  _   _   __ _   ___  _ __
   \ \/  \/ /   / _ \| '__|| |/ /|_  / / _ \| | | | / _` | / _ \| '__|
    \  /\  /   |  __/| |   |   <  / / |  __/| |_| || (_| ||  __/| |
     \/  \/     \___||_|   |_|\_\/___| \___| \__,_| \__, | \___||_|
                                                     __/ |
                                                    |___/
```


## Overview

This project is a Python script designed to calculate the PIN required to access the Werkzeug debugger console in Flask applications. This can be useful for penetration testing or ethical hacking purposes when debugging and analyzing vulnerable applications.

---

## Features

- **PIN Generation**: Calculate the Werkzeug debugger PIN using key system parameters.
- **Cookie Generation**: Generate a cookie that can be used in conjunction with the PIN for access.
- **Parameter Discovery**: Extracts necessary data points from server files and paths.
- **User-Friendly**: Interactive command-line tool with detailed usage instructions.
- **Educational Purposes**: Ideal for learning about vulnerabilities in web frameworks.

---

## Prerequisites

- Python 3.7+
- `hashlib` (Standard Library)
- `itertools` (Standard Library)
- `argparse` (Standard Library)
- `colorama` (Install via `pip install colorama`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SidneyJob/werkzeug-pin-gen.git
   cd werkzeug-pin-gen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Command-Line Arguments

```bash
python3 gen.py --username <USERNAME> --path <FLASK_PATH> --mac <MAC_ADDRESS> --cgroup <CGROUP> --machine_id <MACHINE_ID> [--modname <MODULE_NAME>] [--appname <APP_NAME>]
```

- `--username` *(Required)*: Username of the user running the Flask app (e.g., `web-app`).
- `--path` *(Required)*: Path to the `app.py` file in the Flask installation.
- `--mac` *(Required)*: MAC address of the network interface.
- `--cgroup` *(Required)*: CGROUP value from `/proc/self/cgroup`.
- `--machine_id` *(Required)*: Machine ID from `/etc/machine-id` or `/proc/sys/kernel/random/boot_id`.
- `--modname` *(Optional)*: Flask module name (default: `flask.app`).
- `--appname` *(Optional)*: Flask application name (default: `Flask`).

### Example

```bash
python3 gen.py --username web-app --path '/home/web-app/.local/lib/python3.11/site-packages/flask/app.py' --mac '02:42:ac:11:00:1c' --cgroup '12:cpuset:/' --machine_id '43e1bc61-2abe-4e9b-8095-28e6508bfb39' --modname flask.app --appname Flask
```

### Output Example

```text
[+] SUCCESS!
[*] PIN: 8xx-xxx-x1x
[*] Cookie: __wzd11441xxxxexxxx34xxx8=17xxxx31xx|08xxxx68xx59
[*] Modname: flask.app
[*] Appname: Flask
```

---

## How It Works

1. **Extract Required Parameters**:
   - Username from `/etc/passwd` or `/proc/self/environ`.
   - MAC address from `/sys/class/net/[device]/address`.
   - Machine ID from `/etc/machine-id` or `/proc/sys/kernel/random/boot_id`.
   - CGROUP value from `/proc/self/cgroup`.
2. **Generate PIN**:
   - Combine public and private bits to calculate the Werkzeug debugger PIN.
3. **Generate Cookie**:
   - Generate a unique cookie value based on the calculated PIN.

---

## Notes

- **Disclaimer**: Use this tool for ethical and educational purposes only. Unauthorized access to systems is illegal.
- **Compatibility**: Tested with Flask installations using Werkzeug debugger.

---

## Logo

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---
