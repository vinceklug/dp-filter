import feedparser
from feedgen.feed import FeedGenerator
import os

# Dan Patrick Show Original Feed
URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/2c906e2b-2518-466c-a457-ae320005bafb/4818243e-950b-4fc4-8a22-ae320005bb09/podcast.rss"

def main():
    feed = feedparser.parse(URL)
    fg = FeedGenerator()
    fg.load_extension('podcast')

    # Set up your new Feed Info
    fg.title('Dan Patrick Show (No C&R)')
    fg.description('Daily DP Show episodes without the fill-in hosts.')
    fg.link(href='https://github.com/your-username/dp-filter', rel='alternate')
    fg.language('en')

    count = 0
    for entry in feed.entries:
        # THE FILTER: Skip if "C&R" is in the title
        if "C&R" in entry.title:
            continue

        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.description(entry.description)
        fe.published(entry.published)
        
        if hasattr(entry, 'enclosures'):
            enclosure = entry.enclosures[0]
            fe.enclosure(enclosure.href, enclosure.length, enclosure.type)
        
        count += 1
        if count >= 50: # Keeps the file small and fast
            break

    fg.rss_file('filtered_feed.xml')

if __name__ == "__main__":
    main()
