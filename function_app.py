import logging
import tweepy as tw
import re
from datetime import datetime, timedelta
import pytz
#from Ipython.Display import Image, display

# Twitter API credentials
consumer_key = "yHnNAB0FmNJ4phHtrSF036xsQ"
consumer_secret = "Wzk2AV8sk2YFAglBjS3N5DkTruMlvZODKGZdJik4kmUo9hGgIH"
access_token = "1778022552209694720-VrhQhka5heICC6tki5UcGw8sCOdH39"
access_secret ="uJcqECB9HHbOLFjkbdv4ChxKDSdWfqo01hoAxyfUvaazJ"
BEARER_TOKEN = ""

# Authenticate with Twitter API
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Search query for Downdetector tweets
search_query = "downdetector -filter:retweets"

# Fetch tweets from the last 24 hours
tweets = tw.Cursor(api.search_tweets,
                   q=search_query,
                   lang="en",
                   result_type="recent",
                   tweet_mode="extended",
                   since=(datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")).items(5)

# Timezone setup (using pytz)
timezone = pytz.timezone("America/New_York")  

# Process tweets
downdetector_data = []
for tweet in tweets:
    tweet_text = tweet.full_text
    tweet_time = tweet.created_at
    username = tweet.user.screen_name
    
    # Convert tweet time to the desired timezone
    tweet_time = tweet_time.astimezone(timezone)

    # Use regex to find keywords related to downdetector and outages
    if re.search(r"\b(down|outage|failure|unavailable|offline)\b", tweet_text, re.IGNORECASE):
        downdetector_data.append({
            "time": tweet_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),  # formatted time with timezone
            "user": username,
            "text": tweet_text
        })

# Print results
for data in downdetector_data:
    print(f"[{data['time']}] @{data['user']}: {data['text']}")