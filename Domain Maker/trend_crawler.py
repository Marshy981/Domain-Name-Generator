import os
import json
import requests
from pytrends.request import TrendReq
from bs4 import BeautifulSoup

class TrendCrawler:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.product_hunt_api_key = os.getenv('PRODUCT_HUNT_API_KEY')

    def get_google_trends(self, keywords, timeframe='today 1-m'):
        try:
            self.pytrends.build_payload(kw_list=keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            data = self.pytrends.interest_over_time()
            if not data.empty:
                return data.drop(columns=['isPartial'])
            return None
        except Exception as e:
            print(f"Error fetching Google Trends: {e}")
            return None

    def get_product_hunt_trends(self):
        if not self.product_hunt_api_key:
            print("PRODUCT_HUNT_API_KEY not set. Skipping Product Hunt trends.")
            return None
        # Product Hunt API is deprecated. Need to find an alternative or scrape.
        # For now, I'll add a placeholder for scraping.
        print("Product Hunt API is deprecated. Attempting to scrape Product Hunt.")
        url = "https://www.producthunt.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            # This is a placeholder. Actual scraping would require inspecting Product Hunt's HTML structure.
            # For demonstration, let's assume we can find trending topics in a specific div/class.
            trending_topics = []
            # Example: find all h3 tags with a specific class
            # for item in soup.find_all('h3', class_='styles_title__XXXXX'):
            #    trending_topics.append(item.get_text(strip=True))
            print("Product Hunt scraping placeholder executed. No actual data extracted without specific selectors.")
            return trending_topics
        except requests.exceptions.RequestException as e:
            print(f"Error scraping Product Hunt: {e}")
            return None

    def get_exploding_topics_trends(self):
        url = "https://explodingtopics.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            trending_topics = []
            # This is a placeholder. Actual scraping would require inspecting ExplodingTopics' HTML structure.
            # Example: find all div tags with a specific class containing topic names
            # for item in soup.find_all('div', class_='topic-name'):
            #    trending_topics.append(item.get_text(strip=True))
            print("ExplodingTopics scraping placeholder executed. No actual data extracted without specific selectors.")
            return trending_topics
        except requests.exceptions.RequestException as e:
            print(f"Error scraping ExplodingTopics: {e}")
            return None

    def get_trending_keywords(self):
        all_trends = {}

        # Google Trends
        # Need some initial keywords to start with for Google Trends
        # For now, let's use some generic ones. In a real scenario, these might come from a seed list or previous runs.
        google_keywords = ['AI', 'Machine Learning', 'Sustainable Energy', 'Virtual Reality', 'Blockchain']
        google_data = self.get_google_trends(google_keywords)
        if google_data is not None:
            for keyword in google_keywords:
                if keyword in google_data.columns:
                    # Simple velocity score: average of last 3 months vs previous 3 months
                    # This is a very basic example, a real velocity score would be more complex
                    if len(google_data[keyword]) >= 6:
                        current_avg = google_data[keyword].iloc[-3:].mean()
                        previous_avg = google_data[keyword].iloc[-6:-3].mean()
                        if previous_avg > 0:
                            velocity = (current_avg - previous_avg) / previous_avg
                        else:
                            velocity = 0 # Cannot calculate if previous is zero
                        all_trends[keyword] = {'source': 'Google Trends', 'velocity': velocity, 'score': current_avg}
                    else:
                        all_trends[keyword] = {'source': 'Google Trends', 'velocity': 0, 'score': google_data[keyword].mean()}

        # Product Hunt Trends
        product_hunt_data = self.get_product_hunt_trends()
        if product_hunt_data:
            for topic in product_hunt_data:
                # Assign a dummy velocity and score for now
                all_trends[topic] = {'source': 'Product Hunt', 'velocity': 0.1, 'score': 70}

        # Exploding Topics Trends
        exploding_topics_data = self.get_exploding_topics_trends()
        if exploding_topics_data:
            for topic in exploding_topics_data:
                # Assign a dummy velocity and score for now
                all_trends[topic] = {'source': 'Exploding Topics', 'velocity': 0.2, 'score': 80}

        return all_trends

if __name__ == '__main__':
    # This part is for testing the module independently
    # In the main program, it will be imported and used.
    # For testing, ensure .env is loaded if running directly.
    from dotenv import load_dotenv
    load_dotenv()
    crawler = TrendCrawler()
    trends = crawler.get_trending_keywords()
    if trends:
        print("\n--- Trending Keywords ---")
        for keyword, data in trends.items():
            print(f"Keyword: {keyword}, Source: {data['source']}, Velocity: {data['velocity']:.2f}, Score: {data['score']:.2f}")
    else:
        print("No trends found.")


