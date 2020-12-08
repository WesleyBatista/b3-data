from sqlalchemy import create_engine
from sqlalchemy import Column, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from zipfile import ZipFile
import csv
from io import TextIOWrapper


FIELDNAMES = 'RptDt;TckrSymb;UpdActn;GrssTradAmt;TradQty;NtryTm;TradId;TradgSsnId;TradDt'  # noqa
Base = declarative_base()
Session = sessionmaker()


class TickerCsv(Base):
    __tablename__ = 'tickercsv'

    _id = Column(BigInteger, name='id', primary_key=True)
    RptDt = Column(String, name='RptDt')
    TckrSymb = Column(String, name='TckrSymb')
    UpdActn = Column(BigInteger, name='UpdActn')
    GrssTradAmt = Column(Float, name='GrssTradAmt')
    TradQty = Column(BigInteger, name='TradQty')
    NtryTm = Column(BigInteger, name='NtryTm')
    TradId = Column(BigInteger, name='TradId')
    TradgSsnId = Column(BigInteger, name='TradgSsnId')
    TradDt = Column(String, name='TradDt')

    @classmethod
    def from_tuple(cls, *args):
        asdict = dict([x for x in zip(FIELDNAMES.split(';'), args)])
        return cls(**asdict)


def _make_sure_table_exists(engine):
    Base.metadata.create_all(engine)


def parse_row(**columns):
    if 'GrssTradAmt' in columns:
        columns['GrssTradAmt'] = float(columns['GrssTradAmt'].replace(',', '.'))
    return TickerCsv(**columns)


def _get_csv_reader(contents):
    return csv.DictReader(contents, fieldnames=FIELDNAMES.split(';'), delimiter=';')  # noqa


def _csv_in_chunks(reader, chunksize):
    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            chunk = []
        chunk.append(line)
    yield chunk


def _get_csv_file_stream_reader(filepath, date):
    zip_csv_filepath = f"TradeIntraday_{date.replace('-', '')}_1.txt"
    with ZipFile(filepath) as zip_archive:
        with zip_archive.open(zip_csv_filepath, 'r') as infile:
            reader = _get_csv_reader(TextIOWrapper(infile, 'utf-8'))
            for row in reader:
                yield row


def upload(dsn, chunk_size, date):
    engine = create_engine(dsn)
    _make_sure_table_exists(engine)
    Session.configure(bind=engine)
    s = Session()
    filepath = f"{date}.zip"
    csv_reader = _get_csv_file_stream_reader(filepath, date)
    processed_rows = 0
    for chunk_idx, chunk in enumerate(_csv_in_chunks(csv_reader, chunk_size), 1):
        print(f'chunk #{chunk_idx}')
        data = [parse_row(**row) for i, row in enumerate(chunk) if i != 0]
        s.bulk_save_objects(data)
        s.commit()
        processed_rows += len(data)
    print(f'processed rows: {processed_rows}')
    Session.close_all()
