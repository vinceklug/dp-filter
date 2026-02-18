import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime, timedelta
import time
import sys

URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/2c906e2b-2518-466c-a457-ae320005bafb/4818243e-950b-4fc4-8a22-ae320005bb09/podcast.rss"

# Filtering keywords
BANNED_WORDS = ["c&r", "c & r", "covino", "rich", "best of", "c&amp;r"]

def main():
    print("Fetching original feed...", flush=True)
    feed = feedparser.parse(URL)
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('Dan Patrick Show (Filtered)')
    fg.description('Daily DP Show episodes without C&R or Best Of clips.')
    fg.link(href='https://github.com/vinceklug/dp-filter', rel='alternate')
    fg.language('en')
    
    # Global Metadata
    fg.podcast.itunes_author('Dan Patrick')
    fg.podcast.itunes_category('Sports')

    # Widened to 14 days to ensure the feed isn't empty
    cutoff_date = datetime.now() - timedelta(days=14)
    count = 0

    for entry in feed.entries:
        # Date handling
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        if published_time < cutoff_date:
            continue

        # Content Filter
        search_blob = (
            entry.get('title', '') + 
            entry.get('summary', '') + 
            entry.get('description', '')
        ).lower()
        
        if any(word in search_blob for word in BANNED_WORDS):
            print(f">>> SKIPPING: {entry.title}", flush=True)
            continue

        # Add Entry
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.description(entry.get('description', ''))
        fe.published(entry.published)
        fe.podcast.itunes_author('Dan Patrick')
        
        # Enclosure check (Required for Apple Podcasts)
        if hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
            enclosure = entry.enclosures[0]
            fe.enclosure(enclosure.href, enclosure.length, enclosure.type)
            print(f"Added: {entry.title}", flush=True)
            count += 1
        
        if count >= 40: 
            break

    if count == 0:
        print("WARNING: No episodes found. Apple Podcasts may reject an empty feed.", flush=True)

    fg.rss_file('filtered_feed.xml')
    print(f"Done. {count} episodes in feed.", flush=True)

if __name__ == "__main__":
    main()
