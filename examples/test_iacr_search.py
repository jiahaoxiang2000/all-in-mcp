# examples/test_iacr_search.py
"""
Example script to test IACR paper search functionality
"""
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from all_in_mcp.academic_platforms.iacr import IACRSearcher


def test_iacr_search():
    """Test the IACR search functionality"""
    print("Testing IACR ePrint Archive search...")

    searcher = IACRSearcher()

    # Test search
    try:
        print("\n1. Testing search functionality:")
        papers = searcher.search("cryptography", max_results=5)
        print(f"Found {len(papers)} papers for query 'cryptography':")

        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   Authors: {', '.join(paper.authors)}")
            print(f"   Paper ID: {paper.paper_id}")
            print(f"   Published: {paper.published_date}")
            print(f"   URL: {paper.url}")
            print(
                f"   Abstract: {paper.abstract[:200]}..."
                if len(paper.abstract) > 200
                else f"   Abstract: {paper.abstract}"
            )

        # Test download if we found papers
        if papers:
            print(f"\n2. Testing PDF download for first paper:")
            paper = papers[0]
            save_path = "./downloads"

            try:
                pdf_path = searcher.download_pdf(paper.paper_id, save_path)
                print(f"✓ PDF downloaded successfully: {pdf_path}")

                # Test reading the paper
                print(f"\n3. Testing paper reading:")
                text_content = searcher.read_paper(paper.paper_id, save_path)
                print(f"✓ Paper text extracted successfully")
                print(f"   Text length: {len(text_content)} characters")
                print(f"   First 300 characters: {text_content[:300]}...")

                # Clean up the downloaded file
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                    print(f"✓ Cleaned up downloaded file")

            except Exception as e:
                print(f"✗ Error in download/read test: {e}")

    except Exception as e:
        print(f"✗ Error in search test: {e}")


if __name__ == "__main__":
    test_iacr_search()
