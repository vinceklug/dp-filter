import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime, timedelta
import time
import sys

URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/2c906e2b-2518-466c-a457-ae320005bafb/4818243e-950b-4fc4-8a22-ae320005bb09/podcast.rss"

BANNED_WORDS = ["c&r", "c & r", "covino", "rich", "best of", "c&amp;r"]

def main():
    print("Starting podcast filter script...", flush=True)
    feed = feedparser.parse(URL)
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('Dan Patrick Show (Filtered)')
    fg.description('Daily DP Show episodes without C&R or Best Of clips.')
    fg.link(href='https://github.com/vinceklug/dp-filter', rel='alternate')
    fg.language('en')
    
    fg.author({'name': 'Dan Patrick'})
    fg.podcast.itunes_author('Dan Patrick')

    cutoff_date = datetime.now() - timedelta(days=7)
    count = 0

    print(f"Checking {len(feed.entries)} entries from the original feed...", flush=True)

    for entry in feed.entries:
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        
        # Date Filter
        if published_time < cutoff_date:
            continue

        # Content Filter
        search_blob = (
            entry.get('title', '') + 
            entry.get('summary', '') + 
            entry.get('description', '')
        ).lower()
        
        if any(word in search_blob for word in BANNED_WORDS):
            # THE KEY FIX: Added flush=True here
            print(f">>> SKIPPING BANNED CONTENT: {entry.title}", flush=True)
            continue

        # Add Entry
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.description(entry.get('description', ''))
        fe.published(entry.published)
        fe.podcast.itunes_author('Dan Patrick')
        fe.podcast.itunes_summary('zzzpodcast') 
        
        if hasattr(entry, 'enclosures'):
            enclosure = entry.enclosures[0]
            fe.enclosure(enclosure.href, enclosure.length, enclosure.type)
        
        print(f"Added: {entry.title}", flush=True)
        count += 1
        if count >= 40: 
            break

    fg.rss_file('filtered_feed.xml')
    print(f"--- Process Complete. Added {count} episodes to filtered_feed.xml ---", flush=True)

if __name__ == "__main__":
    main()
