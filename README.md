# PubMed Paper Fetcher  

A command-line tool to fetch and filter research papers from **PubMed**, identifying papers with at least one author affiliated with a **pharmaceutical or biotech company** and exporting the results to a CSV file.

## 🚀 Features  
- Fetches research papers using the **PubMed API**  
- Supports **custom search queries**  
- Filters papers based on **author affiliations**  
- Extracts **non-academic authors & company names**  
- Saves the results in a **CSV file**  
- Provides a **command-line interface (CLI)** with multiple options  

---

## 📦 Installation  

### **Prerequisites**
- **Python 3.9+**  
- **Poetry (Dependency Manager)** → Install with:  
  ```sh
  pip install poetry

Git → (Required for version control)

Clone the Repository

```sh
git clone https://github.com/ShaikShabeena5E7/pubmed-paper-fetcher.git

navigate to the origin folder

cd pubmed-paper-fetcher
---------------------------------------
Install Dependencies

poetry install
---------------------------------------
For fetching: run below in terminal 
poetry run python fetch_papers.py -q "biotechnology"

For saving the csv file
poetry run python fetch_papers.py -q "cancer research" -f "cancer_papers.csv"

Fr debg mode:
poetry run python fetch_papers.py -q "genomics" -d

