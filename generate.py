import json
import random
import time
from datetime import datetime, timedelta

# Constants
DESCRIPTIONS = [
    "GitHub",
    "Google",
    "Facebook",
    "Twitter",
    "LinkedIn",
    "Amazon",
    "Netflix",
    "Spotify",
    "Zoom",
    "Slack",
    "Reddit",
    "Microsoft Office",
    "Dropbox",
    "Instagram",
    "WhatsApp",
    "Trello",
    "Jira",
    "Asana",
    "GitLab",
    "Salesforce",
    "Quora",
    "Pinterest",
    "YouTube",
    "Medium",
    "TikTok",
    "Snapchat",
    "PayPal",
    "eBay",
    "Yelp",
    "Airbnb",
    "Uber",
    "Lyft",
    "Stripe",
    "Square",
    "Shopify",
    "WordPress",
    "Zoom",
    "HubSpot",
    "Mailchimp",
    "Hootsuite",
    "Buffer",
    "Canva",
    "Twitch",
    "Kickstarter",
    "Patreon",
    "Coursera",
    "Udemy",
    "Skillshare",
    "Duolingo",
]

USERNAMES = [
    "simonTest",
    "johnDoe",
    "alice123",
    "bobTest",
    "charlieDev",
    "eveUser",
    "malloryQ",
    "trudyExample",
    "victorVal",
    "peggyDemo",
]

PASSWORDS = [
    "test_password_1",
    "test_password_2",
    "password123",
    "adminPass",
    "userPass2021",
    "securePassword",
    "qwerty12345",
    "mySecretPass",
    "samplePassword",
    "randomPass",
]

CATEGORIES = [
    "work",
    "personal",
    "finance",
    "social",
    "health",
    "education",
    "entertainment",
    "travel",
    "shopping",
    "misc",
]


# Helper functions
def random_timestamp():
    start = datetime(2020, 1, 1)
    end = datetime.now()
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


def generate_unique_entry(existing_entries):
    while True:
        entry = {
            "description": random.choice(DESCRIPTIONS),
            "password": {"current_password": random.choice(PASSWORDS)},
        }

        if random.choice([True, False]):
            entry["username"] = random.choice(USERNAMES)
        else:
            entry["username"] = ""

        if random.choice([True, False]):
            entry["password"]["old_passwords"] = random.sample(
                PASSWORDS, random.randint(0, 5)
            )

        if random.choice([True, False]):
            entry["categories"] = random.sample(CATEGORIES, random.randint(0, 5))

        if random.choice([True, False]):
            entry["note"] = random.choice(DESCRIPTIONS + [""])

        if random.choice([True, False]):
            timestamp = random_timestamp().timestamp()
            entry["created_at"] = timestamp
            entry["last_modified"] = timestamp + random.randint(0, 1000)

        # Check for uniqueness
        unique_key = (entry["description"], entry["username"])
        if unique_key not in existing_entries:
            existing_entries.add(unique_key)
            return entry


# Generate 50 unique entries
entries = []
existing_entries = set()

for _ in range(50):
    entry = generate_unique_entry(existing_entries)
    entries.append(entry)

# Print or save to a file
print(json.dumps(entries, indent=2))

# Save to file
with open("generated_entries.json", "w") as f:
    json.dump(entries, f, indent=2)
