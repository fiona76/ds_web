# Trame VTU Viewer

This repository contains a minimal Trame web application that loads a `.vtu` file on the server and renders it with VTK.

## Requirements

- Python 3.9+
- `trame`, `trame-vtk`, `trame-vuetify`, `vtk`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Open the URL shown in the terminal (typically `http://localhost:8080`). Provide a path to a `.vtu` file accessible to the server, then click **Load**.
tmp
