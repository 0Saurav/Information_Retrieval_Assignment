import feedparser
import pandas as pd
import os

# Directory to save data
DATA_DIR = "E:/Information_Retrieval_Assignment/Task_2_Classifier/data"
os.makedirs(DATA_DIR, exist_ok=True)
output_file = os.path.join(DATA_DIR, "raw_text.csv")

# Multiple RSS feeds per category
feeds = {
    "business": [
        "http://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.reuters.com/business/feed/"
    ],
    "technology": [
        "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.theverge.com/rss/index.xml"
    ],
    "sport": [
        "http://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.espn.com/espn/rss/news"
    ],
    "politics": [
        "http://feeds.bbci.co.uk/news/politics/rss.xml",
        "https://www.politico.com/rss/politics.xml"
    ],
    "entertainment": [
        "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "https://www.hollywoodreporter.com/t/hollywood-reporters-feed/"
    ]
}

all_data = []

# Fetch news from all feeds
for category, urls in feeds.items():
    for url in urls:
        print(f"Fetching {category} news from {url} ...")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            text = (title + " " + summary).strip()
            if text:  # Skip empty entries
                all_data.append([text, category])

# Create DataFrame
df_new = pd.DataFrame(all_data, columns=["text", "category"])

# Append to existing CSV if exists
if os.path.exists(output_file):
    df_old = pd.read_csv(output_file)
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    # Remove duplicates
    df_combined.drop_duplicates(subset="text", inplace=True)
else:
    df_combined = df_new

# Save updated CSV
df_combined.to_csv(output_file, index=False, encoding="utf-8")
print(f"✅ News data saved to {output_file}")
print(f"Total records: {len(df_combined)}")
