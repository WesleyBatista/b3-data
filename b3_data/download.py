# flake8: noqa
import requests


# https://stackoverflow.com/a/34325723
def _printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def download_tickercsv(date, chunk_size):
    # http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/cotacoes/
    url = 'https://arquivos.b3.com.br/apinegocios/tickercsv/' + date
    filepath = f"{url.split('/')[-1]}.zip"
    print(f'downloading {url} to {filepath}')
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_length = int(r.headers.get('content-length'))
        print(f'total_length: {total_length} bytes')
        with open(filepath, 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size), 1):
                _printProgressBar(i*chunk_size, total_length, prefix='Progress:', suffix='Complete', length=50)
                f.write(chunk)

    return filepath
