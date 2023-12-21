from fastapi import FastAPI
from .models.models import create_database
from sqlalchemy.orm import Session
from .database.database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from .models.models import TransactionInFile
from sqlalchemy import Text, func
from datetime import datetime
from .models.models import Voters, Voting, BlindSig, BlindSigData, UsersHashes
import json

app = FastAPI()

get_session = create_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/")
async def create_transaction_endpoint(db: Session = Depends(get_db)):
    transactions_in_file = db.query(TransactionInFile).all()
    for transaction in transactions_in_file:
        parsed_data = json.loads(transaction.params)

        operation_addVotersList = next((item for item in parsed_data if item.get('key') == 'operation' and item.get('stringValue') == 'addVotersList'), None)
        operation_voters = next((item for item in parsed_data if item.get('key') == 'operation' and item.get('stringValue') == 'vote'), None)
        operation_blindSigIssue = next((item for item in parsed_data if item.get('key') == 'operation' and item.get('stringValue') == 'blindSigIssue'), None)

        if operation_addVotersList:
            new_transaction = Voters(
                nested_tx_id = transaction.nested_tx_id,
                timestamp = transaction.timestamp,
                operation=parsed_data[0]['stringValue'],
                contract_id=parsed_data[1]['stringValue'],
                voters_count=parsed_data[2]['intValue'],
                primary_uik_region_code=parsed_data[4]['stringValue'],
                primary_uik_number=parsed_data[5]['intValue']
            )  
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)
            user_id_hashes=json.loads(parsed_data[3]['stringValue'])
            for hash in user_id_hashes:
                new_user = UsersHashes (
                    user_id_hash = hash,
                    voter_id = new_transaction.id
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
        elif operation_voters:
            new_transaction = Voting(
                nested_tx_id = transaction.nested_tx_id,
                timestamp = transaction.timestamp,
                operation=parsed_data[0]['stringValue'],
                vote = parsed_data[1]['binaryValue'],
                blindSig = parsed_data[2]['binaryValue']
            )  
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)
        elif operation_blindSigIssue:
            new_transaction = BlindSig(
                nested_tx_id = transaction.nested_tx_id,
                timestamp = transaction.timestamp,
                operation = parsed_data[0]['stringValue'],
                primary_uik_region_code=parsed_data[2]['stringValue'],
                primary_uik_number=parsed_data[3]['intValue']
            )
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)
            data = json.loads(parsed_data[1]['stringValue'])
            new_data = BlindSigData (
                user_id = data[0]['userId'],
                masked_sig = data[0]['maskedSig'],
                blind_sig_id = new_transaction.id
            )
            db.add(new_data)
            db.commit()
            db.refresh(new_data)

@app.get('/voting/voters_count', status_code=200, name='Общее число голосующих')
def get_transaction_count(db: Session = Depends(get_db)):
    total_count = db.query(UsersHashes).count()    
    return {'count': total_count}

@app.get('/voting/results', status_code=200, name='Ход голосования')
def finish_voting(db: Session = Depends(get_db)):
    transactions_in_file = db.query(TransactionInFile).all()
    for transaction in transactions_in_file:
        parsed_data = json.loads(transaction.params)
        operation = next((item for item in parsed_data if item.get('key') == 'operation' and item.get('stringValue') == 'finishVoting'), None)
        if operation:
            return {'status': 'Голосование закончено'}
    return {'status': 'Голосование продолжается'}

@app.get('/voters/list', status_code=200, name='Общий список идентификаторов голосующих')
def get_list_voters(db: Session = Depends(get_db)):
    users = db.query(UsersHashes).all()
    return users

@app.get('/voting/get/results', status_code=200, name='Результаты голосования')
def get_results(db: Session = Depends(get_db)):
    transactions_in_file = db.query(TransactionInFile).all()
    for transaction in transactions_in_file:
        parsed_data = json.loads(transaction.params)
        operation = next((item for item in parsed_data if item.get('key') == 'operation' and item.get('stringValue') == 'results'), None)
        if operation:
            return {'status': 'Итоги подведены, но данных о них нету'}
    return {'status': 'Результатов голосования нет'}

@app.get('/voting/result/timestamp', status_code=200, name='Количество голосов в конкретный час')
def get_result_in_current_timestamp(start_datetime: datetime, end_datetime: datetime, db: Session = Depends(get_db)):
    count = db.query(Voting).filter(Voting.timestamp >= start_datetime,
                                         Voting.timestamp <= end_datetime).count()
    return {'count': count}

@app.get('/voting/ballots/timestamp', status_code=200, name='Количество выданных бюллютеней в конретный час')
def get_ballots_in_current_timestamp(start_datetime: datetime, end_datetime: datetime, db: Session = Depends(get_db)):
    count = db.query(Voting).filter(Voting.timestamp >= start_datetime,
                                         Voting.timestamp <= end_datetime).count()
    return {'count': count}

@app.get('/voters/registered', status_code=200, name='Проверка, зарегистрированы ли голосующие')
def get_is_registered(db: Session = Depends(get_db)):
    pass # Инфы нету