# Flask Installation for BOTHAVIOR

The BOTHAVIOR orchestrator requires Flask. Here's how to install it:

## Option 1: System Package (Recommended for Ubuntu/Debian)

```bash
sudo apt install python3-flask
```

## Option 2: Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install
pip install flask requests

# Run orchestrator
python3 tools/bothavior_orchestrator.py
```

## Option 3: User Install (if system allows)

```bash
pip3 install --user flask requests
```

## Option 4: Break System Packages (NOT recommended)

```bash
pip3 install flask requests --break-system-packages
```

## Check Installation

```bash
python3 -c "import flask; print(flask.__version__)"
```

If this prints a version number, Flask is installed!

## Note

`requests` is already installed in your environment. Only Flask is needed.
