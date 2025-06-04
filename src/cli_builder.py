import sys

import requests
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm

from .court_listener import search_courtlistener
from .export_csv import export_csv
from .export_pdf import export_pdf

console = Console()

@click.command(
    help=(
        "lexcli is a CLI tool to search legal databases and output the results."
    )
)
def generate_cli():
    console.print("\n[bold blue]Welcome to lexcli! (Interactive Mode)[/]")
    
    query = click.prompt("Enter search term", type=str)
    page = click.prompt("Enter results page to fetch", type=int, default=1, show_default=True)
    page_size = click.prompt("Enter total results to fetch", type=int, default=10, show_default=True)
    
    export_csv_ask = Confirm.ask("Do you want to export the results as CSV?", default=False)
    export_pdf_ask = Confirm.ask("Do you want to export the results as PDF?", default=False)
    
    console.print()
    console.print(
        Panel(
            "[bold][green] Press Enter to Search [/green][/bold]",
            title="Ready",
            subtitle="(click Enter)",
            expand=False,
            border_style="blue",
        )
    )
    perform_search = Confirm.ask("", default=True)
    
    if not perform_search:
        console.print("[bold red]Exiting...[/]")
        sys.exit(0)
        
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
    table.add_column("Download Link (not guaranteed to work)", style="yellow", no_wrap=True)

    for idx, item in enumerate(results, start=1):
        name = item.get("caseName", "-")
        court = item.get("court", "-")
        date_filed = item.get("dateFiled", "-")
        dl_link = item.get("opinions")[0].get("download_url", "None")
        table.add_row(str(idx), name, court, date_filed, dl_link)

    console.print(table)

    if export_csv_ask:
        try:
            export_csv(results)
            console.print(f"\n[bold green]CSV exported successfully![/]")
        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/]")
    if export_pdf_ask:
        try:
            export_pdf(query, results)
            console.print(f"[green]PDF saved![/]\n")
        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/]")
    
    console.print(f"[green]Done![/]")
