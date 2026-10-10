from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_serpapi(query):
    """Search the web using SerpApi."""

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5
    }

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=20
    )

    data = response.json()

    if "error" in data:
        return []

    return data.get("organic_results", [])


def research_claim(claim):
    """Perform multiple searches for the same claim."""

    queries = [
        claim,
        claim + " fact check",
        claim + " official source"
    ]

    all_results = []
    seen_links = set()

    for query in queries:

        results = search_serpapi(query)

        for result in results:

            link = result.get("link", "")

            if link and link not in seen_links:

                seen_links.add(link)
                all_results.append(result)

    return all_results[:10]


def analyze_results(results):
    """
    Simple evidence assessment.

    This is not an authoritative fact-check.
    """

    support_words = [
        "confirmed",
        "official",
        "according to",
        "announced",
        "reported",
        "evidence",
        "research shows",
        "verified"
    ]

    contradiction_words = [
        "false",
        "fake",
        "misleading",
        "incorrect",
        "debunked",
        "fact check",
        "no evidence",
        "not true"
    ]

    support_score = 0
    contradiction_score = 0

    for result in results:

        text = (
            result.get("title", "")
            + " "
            + result.get("snippet", "")
        ).lower()

        for word in support_words:

            if word in text:
                support_score += 1

        for word in contradiction_words:

            if word in text:
                contradiction_score += 1

    if contradiction_score > support_score:

        status = "Contradicted"

        explanation = (
            "Some retrieved sources contain language "
            "that questions or contradicts the claim."
        )

    elif support_score > contradiction_score:

        status = "Supported"

        explanation = (
            "Some retrieved sources contain information "
            "that supports the claim."
        )

    else:

        status = "Unclear"

        explanation = (
            "The retrieved sources do not provide enough "
            "evidence for a clear conclusion."
        )

    return status, explanation, support_score, contradiction_score


@app.route("/", methods=["GET", "POST"])
def home():

    claim = ""
    results = []
    error = ""

    status = ""
    explanation = ""

    support_score = 0
    contradiction_score = 0

    if request.method == "POST":

        claim = request.form.get("claim", "").strip()

        if not claim:

            error = "Please enter a news claim."

        elif not SERPAPI_KEY:

            error = "SerpApi API key is missing."

        else:

            try:

                results = research_claim(claim)

                if results:

                    (
                        status,
                        explanation,
                        support_score,
                        contradiction_score
                    ) = analyze_results(results)

                else:

                    status = "No Results"

                    explanation = (
                        "No relevant web results were found."
                    )

            except Exception as e:

                print("ERROR:", e)

                error = (
                    "Something went wrong while "
                    "researching the claim."
                )

    return render_template(
        "index.html",
        claim=claim,
        results=results,
        error=error,
        status=status,
        explanation=explanation,
        support_score=support_score,
        contradiction_score=contradiction_score
    )


if __name__ == "__main__":
    app.run(debug=True)
