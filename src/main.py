import os
import json
import csv
import sys
from pathlib import Path

from dotenv import load_dotenv
import click
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

console = Console()

load_dotenv()
cl_url = os.getenv("COURTLISTENER_URL")
cl_token = os.getenv("COURTLISTENER_TOKEN")

def search_courtlistener(query: str, page: int = 1, page_size: int = 10) -> list[dict]:
    headers = {}
    if cl_token:
        headers["Authorization"] = f"Token {cl_token}"
    params = {
        "q": query,
        "page": page,
        "page_size": page_size
    }
    
    response = requests.get(f"{cl_url}/search", headers=headers, params=params)
    response.raise_for_status()
    return response.json()["results"]

@click.command(
    help=(
        "lexcli is a CLI tool to search legal databases and output to a CSV file."
    )
)
@click.option(
    "--query",
    "-q",
    required=True,
    help="Enter a search term to query legal databases."
)
@click.option(
    "--page",
    "-p",
    default=1,
    help="Page of the results fo fetch (10 results per page)."
)
@click.option(
    "--page-size",
    "-ps",
    default=10,
    help="How many results to fetch (max 100)."
)
@click.option(
    "--output-json",
    "-j",
    default="../output.json",
    show_default=True,
    help="JSON output file name."
)
@click.option(
    "--output-csv",
    "-c",
    default="../output.csv",
    show_default=True,
    help="CSV output file name."
)
def main(query: str, page: int, page_size: int, output_json: str, output_csv: str):
    console.print(f"\n[bold cyan]lexcli[/] -> Searching legal databases for [green]{query}[/]...\n")
    
    #Send request to CourtListener API
    try:
        results = search_courtlistener(query, page, page_size)
    except requests.HTTPError as e:
        console.print(f"[red]Error: {e}[/]")
        sys.exit(1)
    if not results:
        console.print(f"[yellow]No results returned fro '{query}'.")
        sys.exit(0)
    
    #Printing some results
    # table = Table(title=f"Results for '{query}'")
    # table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    # table.add_column("Citation", style="magenta")
    # table.add_column("Case Name", style="white")
    # table.add_column("Date Filed",style="green")
    # 
    # for idx, item in enumerate(results, start=1):
    #     citation = item.get("citation") or item.get("caseName", "-")
    #     name = item.get("caseName", "-")
    #     date_filed = item.get("dateFiled", "-")
    #     table.add_row(str(idx), citation, name, date_filed)
    # 
    # console.print(table)
    # 
    #TODO:Export JSON
    #TODO:Export CSV
    
    console.print(f"[green]Done![/]")
    console.print(f"[cyan]Results: {results}[/]")
if __name__ == "__main__":
    main()
