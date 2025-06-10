# Domain Name Generator Program

This program autonomously generates high-potential domain names based on current global trends and historical domain sales data. It is built with a modular architecture, allowing for easy expansion and maintenance.

## Features

- **Trend Crawler**: Gathers trending keywords from Google Trends, Product Hunt (placeholder for scraping), and ExplodingTopics (placeholder for scraping).
- **Domain Sales Analyzer**: Parses historical domain sales data (from `market-activity.csv`) and trains a simple regression model to estimate domain resale value.
- **Name Generator**: Combines trending keywords with brandable suffixes/patterns, applies phonetic filtering, and can optionally use GPT-4 for smarter name generation.
- **Availability Checker**: Checks `.com`, `.ai`, and `.io` domain availability using the Domainr API.
- **Scoring Engine**: Scores generated domain names based on trend relevance, brandability, domain length, TLD preference, and predicted resale value, outputting a ranked list.

## Setup and Installation

1.  **Clone the repository (or create the project structure manually):**
    ```bash
    mkdir domain_name_generator
    cd domain_name_generator
    mkdir modules
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file contains:
    ```
    python-dotenv
    pytrends
    producthunt
    beautifulsoup4
    requests
    pandas
    scikit-learn
    openai
    ```

4.  **API Keys and `.env` file:**
    This program requires API keys for certain functionalities. Create a file named `.env` in the root directory of the project (`domain_name_generator/`). Copy the content from `.env.template` into your `.env` file and fill in your API keys:

    ```
    PRODUCT_HUNT_API_KEY=YOUR_PRODUCT_HUNT_API_KEY
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    DOMAINR_API_KEY=YOUR_DOMAINR_API_KEY
    ```
    *   **PRODUCT_HUNT_API_KEY**: Product Hunt's public API is deprecated. The current implementation includes a placeholder for scraping, but it requires specific HTML element selectors to work. If you have access to an alternative Product Hunt data source or a working scraping method, you can integrate it here.
    *   **OPENAI_API_KEY**: Required for GPT-4 integration in the Name Generator. If not provided, GPT-4 name generation will be skipped.
    *   **DOMAINR_API_KEY**: Required for checking domain availability. If not provided, availability checks will be limited or skipped.

5.  **`market-activity.csv` file:**
    The `Domain Sales Analyzer` module requires historical domain sales data. Please download `market-activity.csv` from [NameBio](https://namebio.com/) and place it in the root directory of the project (`domain_name_generator/`). If this file is not found, the program will create a dummy file for demonstration purposes, but the resale value estimation will not be accurate.

## How to Run

From the root directory of the project (`domain_name_generator/`), run the `main.py` script:

```bash
python3 main.py
```

## Program Flow

1.  **Initialization**: Loads environment variables and initializes all modules.
2.  **Trend Crawling**: Fetches trending keywords. If API keys are missing or requests fail (e.g., Google Trends 429 error), it falls back to dummy keywords.
3.  **Domain Sales Analysis**: Loads and processes `market-activity.csv` (or creates a dummy one if not found) and trains a regression model for resale value prediction.
4.  **Name Generation**: Generates potential domain names based on trending keywords, applying phonetic filters. Optionally uses GPT-4 if the API key is provided.
5.  **Availability Checking and Scoring**: For each generated name, it checks availability across `.com`, `.ai`, and `.io` TLDs (if `DOMAINR_API_KEY` is set). It then scores each available domain based on various factors and predicts its resale value.
6.  **Output Results**: Saves a ranked list of high-potential domains to `leaderboard.csv` and `leaderboard.json` in the project root directory.

## Module Breakdown

### `modules/trend_crawler.py`
Handles fetching trending data. Currently supports Google Trends via `pytrends`. Product Hunt and ExplodingTopics are implemented with placeholders for scraping, requiring further development to specify correct HTML selectors or alternative data sources.

### `modules/domain_sales_analyzer.py`
Processes historical domain sales data. It extracts features like word count and TLD, then trains a `LinearRegression` model to estimate domain resale value. Requires `market-activity.csv`.

### `modules/name_generator.py`
Generates domain names by combining keywords with predefined suffixes and patterns. Includes a basic phonetic filter to avoid awkward consonant clusters. Can integrate with OpenAI's GPT-4 for more creative name suggestions.

### `modules/availability_checker.py`
Checks the availability of generated domain names for `.com`, `.ai`, and `.io` TLDs using the Domainr API. Includes basic error handling and fallback logic.

### `modules/scoring_engine.py`
Calculates a weighted score for each domain name based on:
-   Trend relevance
-   Brandability (currently based on length)
-   Domain length
-   TLD preference
-   Predicted resale value

It outputs the ranked list to CSV and JSON files.

## Limitations and Future Improvements

-   **API Keys**: The program's full functionality heavily relies on external API keys. Without them, some features will be skipped or use dummy data.
-   **Scraping**: The Product Hunt and ExplodingTopics scraping implementations are placeholders. They need to be updated with robust scraping logic, including proper HTML element selection and handling of website structure changes.
-   **Trend Data**: Google Trends API (pytrends) can be rate-limited (429 errors). Implementing retry mechanisms with exponential backoff or using alternative trend data sources would improve robustness.
-   **Domain Sales Data**: The `market-activity.csv` is a large file and needs to be manually downloaded. Automating this process or using a dedicated API for historical domain sales would be beneficial.
-   **Resale Value Model**: The current regression model is simple. More advanced machine learning models and additional features (e.g., industry, keyword popularity, age of domain) could significantly improve prediction accuracy.
-   **Brandability Scoring**: The brandability score is currently very basic. Integrating more sophisticated linguistic analysis, sentiment analysis, or even user feedback mechanisms could enhance this.
-   **Phonetic Filtering**: The phonetic filtering is a simple consonant cluster check. More advanced phonetic rules and language-specific considerations could be added.
-   **TLD Coverage**: Currently, only `.com`, `.ai`, and `.io` are checked for availability. Expanding this to a wider range of TLDs would be valuable.
-   **Error Handling**: While basic error logging is in place, more comprehensive error handling, including specific error codes and user-friendly messages, could be implemented.

## Missing APIs

During development, the following APIs were identified as potentially missing or requiring further attention:

-   **Product Hunt API**: The public API is deprecated. The current implementation uses a placeholder for scraping. A robust alternative data source or a working scraping solution is needed.
-   **Domainr API**: While a placeholder for the API key is present, a valid key is required for actual availability checks.
-   **OpenAI API (GPT-4)**: A valid API key is required to leverage GPT-4 for advanced name generation.

Please provide any missing API keys or guidance on alternative data sources to enhance the program's capabilities.

