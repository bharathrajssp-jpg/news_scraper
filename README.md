# news_scraper
# News Headlines Web Scraper

A Python script that automatically scrapes top headlines from news websites and saves them to a text file.

## Features
- Scrapes headlines from BBC News and Reuters
- Filters duplicates and irrelevant content
- Saves timestamped results to `.txt` file
- Respectful scraping with proper headers and delays

## Quick Start

### Installation
```bash
pip install requests beautifulsoup4
```

### Usage
```bash
python news_scraper.py
```

## Output
- **Terminal**: Shows scraping progress and preview
- **File**: `news_headlines.txt` with all headlines and timestamp

### Sample Output
```
News Headlines - Scraped on 2025-09-25 14:32:15
============================================================

 1. [BBC] UK inflation rises to 4.2% in latest figures
 2. [Reuters] Global markets surge on Federal Reserve decision
 3. [BBC] Climate summit reaches historic agreement
...

Total headlines: 27
```

## Files
- `news_scraper.py` - Main scraper script
- `news_headlines.txt` - Generated output file

## Requirements
- Python 3.6+
- requests
- beautifulsoup4

## Note
Always check website terms of service before scraping. This script includes respectful delays and proper headers.
