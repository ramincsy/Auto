import os
import random

def generate_content():
    topics = ['AI', 'Machine Learning', 'Data Science', 'Web Development', 'Cloud Computing']
    return f'Daily study topic: {random.choice(topics)}'

# Prepare date string
date_string = f"{os.getenv('year')}-{os.getenv('month')}-{os.getenv('day')}"

# Update README.md
with open('README.md', 'a') as f:
    f.write(f'\n## Contributions for {date_string}\n')
    for i in range(3):  # Add 3 lines of daily content
        f.write(f'- {generate_content()}\n')
