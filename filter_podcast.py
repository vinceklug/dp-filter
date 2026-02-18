import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime, timedelta
import time

URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/2c906e2b-2518-466c-a457-ae320005bafb/4818243e-950b-4fc4-8a22-ae320005bb09/podcast.rss"

# Filtering keywords
BANNED_WORDS = ["c&r", "c & r", "covino", "rich", "best of", "c&amp;r"]

def main():
    feed = feedparser.parse(URL)
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('Dan Patrick Show (Filtered)')
    fg.description('Daily DP Show episodes without C&R or Best Of clips.')
    fg.link(href='https://github.com/vinceklug/dp-filter', rel='alternate')
    fg.language('en')
    
    # Global Artist/Album Artist Metadata
    fg.author({'name': 'Dan Patrick'})
    fg.podcast.itunes_author('Dan Patrick')

    # Calculate the cutoff date (7 days ago)
    cutoff_date = datetime.now() - timedelta(days=7)

    count = 0
    for entry in feed.entries:
        # 1. DATE FILTER: Check if episode is older than 7 days
        # feedparser dates are tuples; we convert to datetime for comparison
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        
        if published_time < cutoff_date:
            continue

        # 2. CONTENT FILTER: Check Title and Description
        search_blob = (
            entry.get('title', '') + 
            entry.get('summary', '') + 
            entry.get('description', '')
        ).lower()
        
        if any(word in search_blob for word in BANNED_WORDS):
            print(f"Skipping banned content: {entry.title}")
            continue

        # 3. ADD ENTRY
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.description(entry.get('description', ''))
        fe.published(entry.published)
        
        # Set Artist to Dan Patrick and Album Artist to zzzpodcast for sorting
        fe.podcast.itunes_author('Dan Patrick')
        # This helps on the iPod/Surfans to keep podcasts at the bottom of the list
        fe.podcast.itunes_summary('zzzpodcast') 
        
        if hasattr(entry, 'enclosures'):
            enclosure = entry.enclosures[0]
            fe.enclosure(enclosure.href, enclosure.length, enclosure.type)
        
        count += 1
        if count >= 40: 
            break

    fg.rss_file('filtered_feed.xml')
    print(f"Successfully updated feed with {count} episodes.")

if __name__ == "__main__":
    main()
