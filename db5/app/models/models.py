from sqlalchemy import Column, Integer, String, Index, JSON, BigInteger, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import sessionmaker
from ..database.database import engine, Base
import os
import pandas as pd
from datetime import datetime
import pytz


class TransactionInFile(Base):
    __tablename__ = 'transaction_in_file'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nested_tx_id = Column(String)
    type = Column(String)
    signature = Column(String)
    timestamp = Column(DateTime)
    sender_public_key = Column(String)
    params = Column(JSON)
    diff = Column(JSON)
    filename = Column(String)
    Index('idx_transaction_in_file_nested_tx_id', nested_tx_id)
    Index('idx_transaction_in_file_type', type)
    Index('idx_transaction_in_file_signature', signature)
    Index('idx_transaction_in_file_timestamp', timestamp)
    Index('idx_transaction_in_file_sender_public_key', sender_public_key)

class Voters(Base):
    __tablename__ = 'voter'

    id = Column(Integer, primary_key=True, index=True)
    nested_tx_id = Column(String)
    timestamp = Column(DateTime)
    operation = Column(String)
    contract_id = Column(String)
    voters_count = Column(Integer)
    primary_uik_region_code = Column(String, nullable=True)
    primary_uik_number = Column(Integer, nullable=True)

class UsersHashes(Base):
    __tablename__ = 'user_hash'

    id = Column(Integer, primary_key=True, index=True)
    user_id_hash = Column(String, nullable=True)
    voter_id = Column(Integer, ForeignKey('voter.id'))

class Voting(Base): # кто голосует  
    __tablename__ = 'voting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nested_tx_id = Column(String)
    timestamp = Column(DateTime)
    operation = Column(String)
    vote = Column(String)
    blindSig = Column(String)

class BlindSig(Base): # битые бюллютени
    __tablename__ = 'blind_sig'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nested_tx_id = Column(String)
    timestamp = Column(DateTime)
    operation = Column(String)
    primary_uik_region_code = Column(String)
    primary_uik_number = Column(Integer)

class BlindSigData(Base):
    __tablename__ = 'blind_sig_data' 

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    masked_sig = Column(String)
    blind_sig_id = Column(Integer, ForeignKey("blind_sig.id"))

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

def save_transactions_to_db(df):
    df.to_sql('transaction_in_file', con=engine, if_exists='append', index=False)

def save_to_database(df, session, filename_value):
    for index, row in df.iterrows():
        existing_entry = session.query(TransactionInFile).filter_by(nested_tx_id=row[0]).first()
        if existing_entry:
            continue

        timestamp_ms = int(row[4])
        timestamp_seconds = timestamp_ms / 1000
        dt_utc = datetime.utcfromtimestamp(timestamp_seconds)
        tz_moscow = pytz.timezone('Europe/Moscow')
        dt_moscow = dt_utc.replace(tzinfo=pytz.utc).astimezone(tz_moscow)
        dt_moscow = dt_moscow.replace(microsecond=0)

        new_entry = TransactionInFile(
                    nested_tx_id=row[0],
                    type=row[1],
                    signature=row[2],
                    timestamp=dt_moscow,
                    sender_public_key=row[5],
                    params=row[8],
                    diff=row[9],
                    filename=filename_value
        )
        session.add(new_entry)
        session.commit()

def get_info_from_transactions(session):
    src_folder = os.path.join(os.getcwd(), 'data')

    folders = os.listdir(src_folder)
    print(len(folders))

    for folder in folders:
        folder_path = os.path.join(src_folder, folder)
        if os.path.isfile(folder_path):
            continue
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
        for csv_file in csv_files:
             filename = csv_file.split('_')[1] + "_" + csv_file.split('_')[2]
             df = pd.read_csv(os.path.join(folder_path, csv_file), sep=';', header=None)
             save_to_database(df, session, filename)

def create_database():    
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    get_info_from_transactions(session)
    session.close()


