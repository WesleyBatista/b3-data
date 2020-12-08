from datetime import date
import click


PREFIX = 'B3DATA'


@click.group(context_settings=dict(auto_envvar_prefix=PREFIX))
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


@cli.command()
@click.argument("date",
                type=click.DateTime(formats=["%Y-%m-%d"]),
                default=str(date.today()))
@click.option("--chunk-size", type=int, default=100000)
@click.option('--dsn', required=True, help=f'Set the environment variable {PREFIX}_UPLOAD_DSN')
def upload(date, chunk_size, dsn):
    """Uploads quotes data"""
    from b3_data import upload
    upload.upload(dsn, chunk_size, str(date.date()))
