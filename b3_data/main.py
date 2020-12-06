from datetime import date
import click


@click.group()
def cli():
    "Utility for http://b3.com.br datasets"


@cli.command()
@click.argument("date",
                type=click.DateTime(formats=["%Y-%m-%d"]),
                default=str(date.today()))
@click.option("--chunk-size", type=int, default=10000)
def download(date, chunk_size):
    """Downloads quotes data"""
    from b3_data import download
    download.download_tickercsv(str(date.date()), chunk_size)
