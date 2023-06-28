# Web Scraping Law Firm

This is a web scraper script which employs Selenium and does the following:
- Cycles through each page of lawyers' last names arranged alphabetically by A-Z, scrolls to the bottom of each page, and presses each "Load More" button
- Collects all URLs from these A-Z pages and provides a method to eliminate extraneous URLs to select for lawyers' profile URLs
- Cycles through all of the lawyers' profile URLs and uses XPath references to HTML elements to pull relevant information from lawyers' profiles
- Aggregates specified information from attorneys' profiles into an Excel file
