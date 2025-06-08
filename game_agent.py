import base64
import io
import time
from collections import deque

import openai
import pyautogui


class GameAgent:
    """Simple agent that captures screenshots and asks GPT for the next action."""

    def __init__(self, api_key: str, goal: str = "Explore the world", memory_size: int = 5,
                 delay: float = 1.0, model: str = "gpt-4"):
        openai.api_key = api_key
        self.goal = goal
        self.memory = deque(maxlen=memory_size)
        self.delay = delay
        self.model = model

    def capture_screen(self) -> str:
        """Capture the screen and return it as base64 encoded PNG."""
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def build_messages(self, image_data: str):
        messages = [
            {"role": "system", "content": "You are a gaming AI helping to achieve the user's goal."},
            {"role": "system", "content": f"Goal: {self.goal}"},
        ]
        for i, (img, action) in enumerate(self.memory):
            messages.append({"role": "system", "content": f"Previous screenshot {i} (PNG base64): {img}"})
            messages.append({"role": "system", "content": f"Previous action {i}: {action}"})
        messages.append({"role": "user", "content": f"Current screenshot (PNG base64): {image_data}"})
        messages.append({
            "role": "user",
            "content": "What key should be pressed next? Reply with a single character such as w, a, s, d, e, etc."
        })
        return messages

    def choose_action(self, image_data: str) -> str:
        messages = self.build_messages(image_data)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
        )
        content = response["choices"][0]["message"]["content"].strip().lower()
        return content[0]

    def press_key(self, key: str):
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)

    def run(self):
        while True:
            img_data = self.capture_screen()
            action = self.choose_action(img_data)
            self.press_key(action)
            self.memory.append((img_data, action))
            time.sleep(self.delay)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the game agent")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--goal", default="Explore the world", help="Goal for the agent")
    parser.add_argument("--memory", type=int, default=5, help="Number of previous frames/actions to keep")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between actions in seconds")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    args = parser.parse_args()

    agent = GameAgent(api_key=args.api_key, goal=args.goal, memory_size=args.memory, delay=args.delay, model=args.model)
    agent.run()
