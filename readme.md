# AI Gaming Agent

This repository contains a simple Python script that allows an AI agent powered by OpenAI's GPT models to interact with a desktop game. The agent periodically captures screenshots, sends them to GPT for analysis and receives a suggested key press (e.g. `w`, `a`, `s`, `d`, `e`), which is then simulated on the keyboard.

## Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

`pyautogui` requires access to the desktop environment and may need additional permissions on your system.

## Usage

Run the agent by providing your OpenAI API key. Optionally supply a goal for the agent and other parameters. The `--memory` flag sets how many previous screenshots and actions are sent back to the model:

```bash
python game_agent.py --api-key YOUR_OPENAI_KEY --goal "Find the exit" --memory 5 --delay 1.0
```

The script will start capturing the screen, querying GPT and pressing keys until interrupted.

## Warning

This is an experimental example. Interacting with games automatically may violate the game's terms of service. Use at your own risk.
