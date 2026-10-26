
import json
from pathlib import Path

data_file = Path(__file__).parent / "sample_messages.json"

with data_file.open("r", encoding="utf-8") as file:
    messages = json.load(file)

print(f"JSON loaded successfully!")
print(f"Total sample messages: {len(messages)}")

for item in messages:
    print(f"\nTest {item['id']}: {item['category']}")
    print(f"Expected warning: {item['expected_warning']}")
