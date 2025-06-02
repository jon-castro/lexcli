import sys

import requests
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

from .court_listener import search_courtlistener


console = Console()

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
    "--output-pdf",
    "-d",
    default="../output.pdf",
    show_default=True,
    help="PDF output file name."
)
@click.option(
    "--output-csv",
    "-c",
    default="../output.csv",
    show_default=True,
    help="CSV output file name."
)
def generate_cli(query: str, page: int, page_size: int, output_pdf: str, output_csv: str):
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
    table = Table(title=f"Results for '{query}'")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Case Name", style="white")
    table.add_column("Court", style="cyan", no_wrap=True)
    table.add_column("Date Filed",style="green")
    table.add_column("Download Link", style="yellow", no_wrap=True)

    for idx, item in enumerate(results, start=1):
        name = item.get("caseName", "-")
        court = item.get("court", "-")
        date_filed = item.get("dateFiled", "-")
        dl_link = item.get("downloadLink", "-")
        table.add_row(str(idx), name, court, date_filed, dl_link)

    console.print(table)

    #TODO:Export JSON
    #TODO:Export CSV
    
    console.print(f"[green]Done![/]")
