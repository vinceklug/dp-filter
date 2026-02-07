import feedparser
from feedgen.feed import FeedGenerator

# Dan Patrick Show Original Feed
URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/2c906e2b-2518-466c-a457-ae320005bafb/4818243e-950b-4fc4-8a22-ae320005bb09/podcast.rss"

# Add any words here that you want to block
BANNED_WORDS = ["C&R", "Best of"]

def main():
    feed = feedparser.parse(URL)
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('Dan Patrick Show (Filtered)')
    fg.description('Daily DP Show episodes without C&R or Best Of clips.')
    fg.link(href='https://github.com/vinceklug/dp-filter', rel='alternate')
    fg.language('en')
    
    # --- ADDED THESE LINES ---
    # This sets the "Artist" at the Show level
    fg.author({'name': 'Dan Patrick'})
    fg.podcast.itunes_author('Dan Patrick')
    # -------------------------

    count = 0
    for entry in feed.entries:
        title_lower = entry.title.lower()
        if any(word.lower() in title_lower for word in BANNED_WORDS):
            continue

        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.description(entry.description)
        fe.published(entry.published)
        
        # --- ADDED THIS LINE ---
        # This ensures each individual episode is tagged with the artist
        fe.podcast.itunes_author('Dan Patrick')
        # -----------------------
        
        if hasattr(entry, 'enclosures'):
            enclosure = entry.enclosures[0]
            fe.enclosure(enclosure.href, enclosure.length, enclosure.type)
        
        count += 1
        if count >= 40: 
            break

    fg.rss_file('filtered_feed.xml')

if __name__ == "__main__":
    main()
