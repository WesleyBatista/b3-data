from datetime import date
import click


@click.group()
def cli():
    "Utility for http://b3.com.br datasets"


@cli.command()
@click.option("--date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--chunk-size", type=int, default=10000)
def download(date, chunk_size):
    """Downloads quotes data"""
    print(date)
    if not date:
        import subprocess
        date = subprocess.getoutput("""echo $(curl --silent 'https://arquivos.b3.com.br/apinegocios/dates') | sed -e 's/"//g' -e 's/\[//g' -e 's/\]//g' | cut -d"," -f 1""")
    else:
        date = str(date)

    from b3_data import download
    download.download_tickercsv(date, chunk_size)
