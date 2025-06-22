#!/usr/bin/env python3
"""
Test script for Crossref searcher functionality
"""
import asyncio
from src.all_in_mcp.academic_platforms.crossref import CrossrefSearcher


async def test_crossref():
    """Test Crossref search functionality"""
    print("Testing Crossref searcher...")

    searcher = CrossrefSearcher()

    # Test search
    print("\n1. Testing search for 'quantum computing'...")
    papers = searcher.search("quantum computing", max_results=3)

    if papers:
        print(f"Found {len(papers)} papers:")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(
                f"   Authors: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}"
            )
            print(f"   DOI: {paper.doi}")
            print(
                f"   Year: {paper.published_date.year if paper.published_date else 'Unknown'}"
            )
            if paper.extra and paper.extra.get("journal"):
                print(f"   Journal: {paper.extra['journal']}")
    else:
        print("No papers found")

    # Test DOI search
    print("\n2. Testing DOI search...")
    if papers and papers[0].doi:
        doi_paper = searcher.search_by_doi(papers[0].doi)
        if doi_paper:
            print(f"Successfully retrieved paper by DOI: {doi_paper.title}")
        else:
            print("Failed to retrieve paper by DOI")

    print("\nTest completed!")


if __name__ == "__main__":
    asyncio.run(test_crossref())
