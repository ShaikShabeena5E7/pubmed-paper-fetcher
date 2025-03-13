import requests
import xml.etree.ElementTree as ET
import csv
import argparse

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query, max_results=5):
    """Fetch paper IDs from PubMed based on a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    
    print("Error fetching data:", response.status_code)
    return []

def fetch_paper_details(paper_ids):
    """Fetches detailed information for given paper IDs from PubMed."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if response.status_code != 200:
        print("Error fetching data from PubMed")
        return []

    return parse_paper_details(response.text)

def parse_paper_details(xml_data):
    """Parses PubMed XML response and extracts relevant details."""
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "N/A"

        # Extract authors and affiliations
        authors = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName").text if author.find("LastName") is not None else ""
            fore_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else "Unknown"

            authors.append({
                "name": f"{fore_name} {last_name}".strip(),
                "affiliation": affiliation
            })

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "PublicationDate": pub_date,
            "Authors": authors
        })

    return papers

def filter_non_academic_authors(papers):
    """Filters papers to include only those with at least one non-academic author."""
    company_keywords = ["Inc.", "Ltd.", "Pharma", "Biotech", "Corporation", "Therapeutics", "Biosciences", "Genomics"]

    filtered_papers = []
    
    for paper in papers:
        non_academic_authors = []
        company_affiliations = set()

        for author in paper["Authors"]:
            affiliation = author["affiliation"]
            if any(keyword in affiliation for keyword in company_keywords):
                non_academic_authors.append(author["name"])
                company_affiliations.add(affiliation)

        if non_academic_authors:
            paper["NonAcademicAuthors"] = non_academic_authors
            paper["CompanyAffiliations"] = list(company_affiliations)
            filtered_papers.append(paper)

    return filtered_papers

def save_to_csv(papers, filename="filtered_papers.csv"):
    """Saves the filtered papers to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-Academic Authors", "Company Affiliations", "Corresponding Author Email"])

        for paper in papers:
            writer.writerow([
                paper["PubmedID"],
                paper["Title"],
                paper["PublicationDate"],
                ", ".join(paper["NonAcademicAuthors"]),
                ", ".join(paper["CompanyAffiliations"]),
                paper.get("CorrespondingAuthorEmail", "N/A")
            ])

    print(f"✅ Data saved to {filename}")

def main():
    """Command-line argument handling and execution."""
    parser = argparse.ArgumentParser(description="Fetch and filter research papers from PubMed.")
    parser.add_argument("-q", "--query", type=str, required=True, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, default="filtered_papers.csv", help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.debug:
        print(f"🔍 Debug Mode: Query = {args.query}, Output File = {args.file}")

    # Fetch paper IDs
    paper_ids = search_pubmed(args.query)
    print("Fetched Paper IDs:", paper_ids)
    
    # Fetch paper details
    paper_details = fetch_paper_details(paper_ids)
    
    if paper_details:
        filtered_papers = filter_non_academic_authors(paper_details)

        # Save results to CSV
        if filtered_papers:
            save_to_csv(filtered_papers, args.file)
        else:
            print("No non-academic papers found.")
    else:
        print("No papers found.")

# Run the program
if __name__ == "__main__":
    main()

