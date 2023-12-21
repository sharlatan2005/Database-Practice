from fastapi import FastAPI
import models

from database import SessionLocal, Base, engine
from sqlalchemy.orm import with_polymorphic
from sqlalchemy import desc
from datetime import date

app = FastAPI()

Base.metadata.create_all(engine)

session = SessionLocal()

# obj_rb1 = models.Transaction_Receive_Bulletin(signature='ffaf', date = '2000-01-04', bulletin_number='6')
# obj_rb2 = models.Transaction_Receive_Bulletin(signature='ff', date = '2000-01-05', bulletin_number='7')
# obj_rb3 = models.Transaction_Receive_Bulletin(signature='dwd', date = '2000-01-06', bulletin_number='8')

# obj_v1 = models.Transaction_Vote(signature='dwd', date = '2000-01-07', candidate_number='1')
# obj_v2 = models.Transaction_Vote(signature='asc', date = '2000-01-08', candidate_number='1')
# obj_v3 = models.Transaction_Vote(signature='dasdas', date = '2000-01-09', candidate_number='1')
# obj_v4 = models.Transaction_Vote(signature='dasd', date = '2000-01-10', candidate_number='3')

# obj_r1 = models.Transaction_Results(signature='dads', date = '2000-01-12', candidate_number='1', number_of_votes='3')
# obj_r2 = models.Transaction_Results(signature='dasdd', date = '2000-01-12', candidate_number='3', number_of_votes='1')

# session.add(obj_rb1)
# session.add(obj_rb3)
# session.add(obj_rb2)

# session.add(obj_v1)
# session.add(obj_v2)
# session.add(obj_v3)
# session.add(obj_v4)

# session.add(obj_r1)
# session.add(obj_r2)

# session.commit()


@app.get("/transactions")
def get_all_transactions():

    transactions = session.query(with_polymorphic(models.Transaction, '*')).all()
    return {
        "transactions" : transactions
    }

@app.get("/transactions/count/")
def get_transactions_count_by_time(start : date, end : date):
    transactions = session.query(with_polymorphic(models.Transaction, '*')).filter(
        models.Transaction.date >= start, models.Transaction.date <= end
    ).all()

    transactions_count = len(transactions)

    return {
        "transactions_count" : transactions_count
    }

@app.get("/transactions/number_of_votes/")
def get_number_of_votes(candidate_id : int):
    transactions = session.query(models.Transaction_Vote).filter(
        models.Transaction_Vote.candidate_number == candidate_id).all()
    
    transactions_count = len(transactions)
    
    return {
        "number_of_votes" : transactions_count
    }

@app.get("/transactions/results")
def get_results_of_voting():
    winner = session.query(models.Transaction_Results).order_by(
        desc(models.Transaction_Results.number_of_votes)).first()
    return {
        "winner" : winner.candidate_number,
        "number_of_votes" : winner.number_of_votes
    }
