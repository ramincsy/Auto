import random
import os

def generate_content():
    """
    Generate a random topic for daily contribution.
    """
    topics = ['AI', 'Machine Learning', 'Data Science', 'Web Development', 'Cloud Computing']
    return f"Daily study topic: {random.choice(topics)}"

def update_readme():
    """
    Update the README.md file with daily content.
    """
    # Get the current date from environment variables
    year = os.getenv('year', 'unknown')
    month = os.getenv('month', 'unknown')
    day = os.getenv('day', 'unknown')
    date_string = f"{year}-{month}-{day}"

    # Append new content to README.md
    with open("README.md", "a") as f:
        f.write(f"\n\n## Contribution for {date_string}\n")
        for i in range(int(day)):  # Loop based on day number for more content
            f.write(f"- {generate_content()}\n")

if __name__ == "__main__":
    update_readme()
