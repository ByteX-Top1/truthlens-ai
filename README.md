TruthLens AI — AI-Powered Fake News Verification Agent

About the Project

TruthLens-AI is a web application that helps users investigate online claims by searching the web and collecting relevant sources using SerpAPI.

It provides a preliminary automated evidence assessment to help users explore whether a claim may be supported, contradicted, or unclear.

Features

- Search the web for a submitted claim.
- Find related fact-checking and official-source results.
- Display relevant source links.
- Provide a preliminary evidence assessment.
- Simple and user-friendly web interface.

Technologies Used

- Python
- Flask
- HTML
- CSS
- SerpApi Google Search API

How to Run

1. Install the dependencies using "pip install -r requirements.txt".
2. Create a ".env" file and add your SerpApi API key as "SERPAPI_KEY=your_api_key".
3. Run "python app.py".
4. Open "http://127.0.0.1:5000" in your browser.

Limitations

The assessment uses simple keyword-based logic and search results. It does not guarantee that a claim is true or false. Users should review the original sources and verify important claims independently.

Security
Keep API keys private. Never commit the ".env" file to a public repository.
Keep API keys private. Never commit the ".env" file to a public repository.
Keep API keys private. Neve
