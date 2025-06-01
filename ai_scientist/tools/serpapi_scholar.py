import os
import requests
import time
import warnings
from typing import Dict, List, Optional, Union
import re

import backoff

from ai_scientist.tools.base_tool import BaseTool


def on_backoff(details: Dict) -> None:
    print(
        f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
        f"calling function {details['target'].__name__} at {time.strftime('%X')}"
    )


class SerpAPIScholarSearchTool(BaseTool):
    def __init__(
        self,
        name: str = "SearchGoogleScholar",
        description: str = (
            "Search for relevant literature using Google Scholar via SerpAPI. "
            "Provide a search query to find relevant academic papers."
        ),
        max_results: int = 10,
    ):
        parameters = [
            {
                "name": "query",
                "type": "str",
                "description": "The search query to find relevant papers.",
            }
        ]
        super().__init__(name, description, parameters)
        self.max_results = max_results
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            warnings.warn(
                "No SerpAPI key found. Set the SERPAPI_KEY environment variable for Google Scholar access."
            )

    def use_tool(self, query: str) -> Optional[str]:
        papers = self.search_for_papers(query)
        if papers:
            return self.format_papers(papers)
        else:
            return "No papers found."

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.HTTPError, requests.exceptions.ConnectionError),
        on_backoff=on_backoff,
    )
    def search_for_papers(self, query: str) -> Optional[List[Dict]]:
        if not query or not self.api_key:
            return None
        
        params = {
            "engine": "google_scholar",
            "q": query,
            "num": self.max_results,
            "hl": "en",  # English results
            "as_ylo": 2015,  # Papers from 2015 onwards for relevancy
            "api_key": self.api_key
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            print(f"SerpAPI Response Status Code: {response.status_code}")
            
            if response.status_code == 429:
                print("SerpAPI rate limit reached. Consider upgrading your plan or waiting before next request.")
                return None
            elif response.status_code == 401:
                print("SerpAPI authentication failed. Please check your API key.")
                return None
            
            response.raise_for_status()
            
            results = response.json()
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                print("SerpAPI returned no organic results for this query.")
                return None
            
            # Convert SerpAPI format to standard format
            papers = []
            for result in organic_results:
                paper = self._format_serpapi_result(result)
                if paper:
                    papers.append(paper)
            
            if not papers:
                print("No valid papers could be extracted from SerpAPI results.")
                return None
            
            # Sort by citation count if available
            papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
            print(f"SerpAPI successfully returned {len(papers)} papers.")
            return papers
            
        except Exception as e:
            print(f"Error searching with SerpAPI: {e}")
            return None

    def _format_serpapi_result(self, result: Dict) -> Optional[Dict]:
        """Convert SerpAPI result to standard paper format"""
        try:
            title = result.get("title", "Unknown Title")
            publication_info = result.get("publication_info", {})
            
            # Extract authors from publication info
            authors = self._extract_authors(publication_info)
            
            # Extract venue and year
            venue = self._extract_venue(publication_info)
            year = self._extract_year(publication_info)
            
            # Extract citation count
            cited_by = result.get("cited_by", {})
            citation_count = self._extract_citation_count(cited_by)
            
            # Get abstract from snippet
            abstract = result.get("snippet", "No abstract available.")
            
            # Generate BibTeX for compatibility
            bibtex = self._generate_bibtex(result)
            
            return {
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
                "abstract": abstract,
                "citationCount": citation_count,
                "citationStyles": {"bibtex": bibtex},
                "url": result.get("link", "")
            }
        except Exception as e:
            print(f"Error formatting result: {e}")
            return None

    def _extract_authors(self, publication_info: Dict) -> str:
        """Extract authors from publication info"""
        if isinstance(publication_info, dict):
            authors = publication_info.get("authors", [])
            if isinstance(authors, list):
                return ", ".join([author.get("name", "") for author in authors if author.get("name")])
            elif isinstance(authors, str):
                return authors
        elif isinstance(publication_info, str):
            # Try to extract authors from string format
            # Common format: "Authors - Journal, Year"
            parts = publication_info.split(" - ")
            if len(parts) > 0:
                return parts[0].strip()
        return "Unknown Authors"

    def _extract_venue(self, publication_info: Dict) -> str:
        """Extract venue/journal from publication info"""
        if isinstance(publication_info, dict):
            return publication_info.get("journal", publication_info.get("conference", "Unknown Venue"))
        elif isinstance(publication_info, str):
            # Try to extract venue from string
            # Common format: "Authors - Journal, Year"
            if " - " in publication_info:
                venue_part = publication_info.split(" - ", 1)[1]
                if ", " in venue_part:
                    return venue_part.split(", ")[0].strip()
                return venue_part.strip()
        return "Unknown Venue"

    def _extract_year(self, publication_info: Dict) -> int:
        """Extract publication year"""
        if isinstance(publication_info, dict):
            year = publication_info.get("year")
            if year:
                try:
                    return int(year)
                except ValueError:
                    pass
        elif isinstance(publication_info, str):
            # Extract year from string using regex
            year_match = re.search(r'\b(19|20)\d{2}\b', publication_info)
            if year_match:
                return int(year_match.group())
        return 2024  # Default to current year if not found

    def _extract_citation_count(self, cited_by: Dict) -> int:
        """Extract citation count"""
        if isinstance(cited_by, dict):
            total = cited_by.get("total", 0)
            if isinstance(total, (int, str)):
                try:
                    return int(total)
                except ValueError:
                    pass
        return 0

    def _generate_bibtex(self, result: Dict) -> str:
        """Generate BibTeX entry for compatibility with existing code"""
        title = result.get("title", "Unknown Title")
        authors = self._extract_authors(result.get("publication_info", {}))
        venue = self._extract_venue(result.get("publication_info", {}))
        year = self._extract_year(result.get("publication_info", {}))
        
        # Generate a simple BibTeX key
        first_author = authors.split(",")[0].strip().replace(" ", "").lower() if authors != "Unknown Authors" else "unknown"
        key = f"{first_author}{year}"
        
        # Remove special characters from key
        key = re.sub(r'[^a-zA-Z0-9]', '', key)
        
        bibtex = f"""@article{{{key},
 title = {{{title}}},
 author = {{{authors}}},
 journal = {{{venue}}},
 year = {{{year}}}
}}"""
        return bibtex

    def format_papers(self, papers: List[Dict]) -> str:
        paper_strings = []
        for i, paper in enumerate(papers):
            paper_strings.append(
                f"""{i + 1}: {paper.get("title", "Unknown Title")}. {paper.get("authors", "Unknown Authors")}. {paper.get("venue", "Unknown Venue")}, {paper.get("year", "Unknown Year")}.
Number of citations: {paper.get("citationCount", "N/A")}
Abstract: {paper.get("abstract", "No abstract available.")}"""
            )
        return "\n\n".join(paper_strings)


# Standalone function for backward compatibility
@backoff.on_exception(
    backoff.expo, requests.exceptions.HTTPError, on_backoff=on_backoff
)
def search_for_papers_serpapi(query, result_limit=10) -> Union[None, List[Dict]]:
    """Search for papers using SerpAPI Google Scholar"""
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    if not serpapi_key:
        warnings.warn(
            "No SerpAPI key found. Set SERPAPI_KEY environment variable for Google Scholar access."
        )
        return None
    
    if not query:
        return None
    
    params = {
        "engine": "google_scholar",
        "q": query,
        "num": result_limit,
        "hl": "en",
        "as_ylo": 2015,  # Papers from 2015 onwards
        "api_key": serpapi_key
    }
    
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        print(f"SerpAPI Response Status Code: {response.status_code}")
        
        if response.status_code == 429:
            print("SerpAPI rate limit reached. The system will fall back to Semantic Scholar.")
            return None
        elif response.status_code == 401:
            print("SerpAPI authentication failed. Please check your API key.")
            return None
            
        response.raise_for_status()
        
        results = response.json()
        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            print("SerpAPI returned no organic results for this query.")
            return None
        
        # Convert to standard format
        tool = SerpAPIScholarSearchTool()
        papers = []
        for result in organic_results:
            paper = tool._format_serpapi_result(result)
            if paper:
                papers.append(paper)
        
        if not papers:
            print("No valid papers could be extracted from SerpAPI results.")
            return None
        
        time.sleep(1.0)  # Rate limiting
        print(f"SerpAPI successfully returned {len(papers)} papers.")
        return papers
        
    except Exception as e:
        print(f"Error in SerpAPI search: {e}")
        return None 