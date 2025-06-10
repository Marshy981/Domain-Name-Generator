import os
import logging
from dotenv import load_dotenv
import pandas as pd

from modules.trend_crawler import TrendCrawler
from modules.domain_sales_analyzer import DomainSalesAnalyzer
from modules.name_generator import NameGenerator
from modules.availability_checker import AvailabilityChecker
from modules.scoring_engine import ScoringEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

def main():
    load_dotenv() # Load environment variables from .env file

    logging.info("Starting Domain Name Generator Program")

    # Check for essential API keys
    product_hunt_api_key = os.getenv("PRODUCT_HUNT_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    domainr_api_key = os.getenv("DOMAINR_API_KEY")

    if not product_hunt_api_key:
        logging.warning("PRODUCT_HUNT_API_KEY not set. Product Hunt trends will be skipped.")
    if not openai_api_key:
        logging.warning("OPENAI_API_KEY not set. GPT-4 name generation will be skipped.")
    if not domainr_api_key:
        logging.warning("DOMAINR_API_KEY not set. Domain availability checks will be limited or skipped.")

    # Initialize modules
    try:
        trend_crawler = TrendCrawler()
        domain_sales_analyzer = DomainSalesAnalyzer(csv_path="market-activity.csv") # Assuming this file exists or will be provided
        name_generator = NameGenerator()
        availability_checker = AvailabilityChecker()
        scoring_engine = ScoringEngine(domain_sales_analyzer)
    except Exception as e:
        logging.error(f"Error initializing modules: {e}")
        return

    # Phase 1: Trend Crawling
    logging.info("\n--- Phase 1: Crawling Trends ---")
    trending_keywords = trend_crawler.get_trending_keywords()
    if not trending_keywords:
        logging.warning("No trending keywords found from crawlers. Using dummy keywords for demonstration.")
        trending_keywords_list = [
            {"keyword": "tech", "source": "Dummy", "velocity": 0.5, "score": 80},
            {"keyword": "innovation", "source": "Dummy", "velocity": 0.4, "score": 75},
            {"keyword": "future", "source": "Dummy", "velocity": 0.6, "score": 85}
        ]
    else:
        logging.info(f"Found {len(trending_keywords)} trending keywords.")
        # Convert dict to list of dicts for easier processing in name_generator
        trending_keywords_list = [{
            "keyword": k,
            "source": v["source"],
            "velocity": v["velocity"],
            "score": v["score"]
        } for k, v in trending_keywords.items()]

    # Phase 2: Domain Sales Analysis (Load and train model)
    logging.info("\n--- Phase 2: Analyzing Domain Sales Data ---")
    try:
        # For demonstration, we need a dummy market-activity.csv if it doesn\'t exist
        # In a real scenario, the user would provide this file.
        if not os.path.exists("market-activity.csv"):
            logging.warning("market-activity.csv not found. Creating a dummy file for demonstration.")
            dummy_data = {
                "Domain": ["example.com", "test-domain.net", "another.org", "brand.ai", "innovate.io", "short.com", "long-long-long.net"],
                "Price": [1000, 500, 750, 2000, 1500, 300, 200],
                "Date": ["2023-01-01", "2023-01-05", "2023-01-10", "2023-01-15", "2023-01-20", "2023-01-25", "2023-01-30"]
            }
            pd.DataFrame(dummy_data).to_csv("market-activity.csv", index=False)

        df_sales = domain_sales_analyzer.load_data()
        if df_sales is not None:
            df_sales = domain_sales_analyzer.extract_features(df_sales)
            domain_sales_analyzer.train_model(df_sales)
            logging.info("Domain sales model trained.")
        else:
            logging.warning("Could not load domain sales data. Resale value estimation will be skipped.")
    except Exception as e:
        logging.error(f"Error in Domain Sales Analysis: {e}")

    # Phase 3: Name Generation
    logging.info("\n--- Phase 3: Generating Domain Names ---")
    generated_names = name_generator.generate_names(
        trend_keywords=trending_keywords_list,
        use_gpt4=(openai_api_key is not None),
        num_names=20 # Generate more names for better chances
    )
    if not generated_names:
        logging.warning("No domain names generated. Exiting.")
        return
    logging.info(f"Generated {len(generated_names)} potential domain names.")

    # Phase 4: Availability Checking and Scoring
    logging.info("\n--- Phase 4: Checking Availability and Scoring ---")
    final_ranked_domains = []
    for name in generated_names:
        # Check availability for .com, .ai, .io
        availability_status = availability_checker.check_availability(name)
        
        for tld in availability_checker.tlds:
            full_domain = f"{name}.{tld}"
            predicted_value = None
            try:
                predicted_value = domain_sales_analyzer.estimate_value(name, tld)
            except Exception as e:
                logging.warning(f"Could not estimate resale value for {full_domain}: {e}")

            score = scoring_engine.score_domain(
                domain_name=name,
                tld=tld,
                trend_data=trending_keywords_list,
                predicted_resale_value=predicted_value,
                availability_status=availability_status
            )
            
            if score > 0: # Only add if score is positive (meaning it passed availability checks and other criteria)
                final_ranked_domains.append({
                    "domain": full_domain,
                    "score": score,
                    "predicted_value": predicted_value,
                    "availability": availability_status.get(tld, "unknown")
                })

    if not final_ranked_domains:
        logging.warning("No high-potential domains found after scoring and availability checks.")
        return

    # Phase 5: Output Results
    logging.info("\n--- Phase 5: Outputting Results ---")
    scoring_engine.output_ranked_list(final_ranked_domains, output_format="csv", filename="leaderboard")
    scoring_engine.output_ranked_list(final_ranked_domains, output_format="json", filename="leaderboard")

    logging.info("Domain Name Generation Program Finished.")

    # Clean up dummy market-activity.csv if it was created by the program
    if os.path.exists("market-activity.csv") and "dummy_data" in locals(): # Check if dummy_data was used
        os.remove("market-activity.csv")
        logging.info("Cleaned up dummy market-activity.csv.")

if __name__ == "__main__":
    # Ensure pandas is imported for the dummy data creation
    import pandas as pd
    main()


