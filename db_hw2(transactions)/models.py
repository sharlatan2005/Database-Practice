from database import Base
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String, Integer, DateTime
# from sqlalchemy.orm import relationship
# from typing import List
from sqlalchemy import ForeignKey

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    signature = Column(String(50))
    date = Column(DateTime)

    type_ = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "transactions",
        "polymorphic_on": type_
    }

class Transaction_Receive_Bulletin(Transaction):

    __tablename__ = "transactions_receive_bulletin"

    id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)

    bulletin_number = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity" : "transaction_receive_bulletin"
    }

class Transaction_Vote(Transaction):
    
    __tablename__ = "transactions_vote"

    id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)

    candidate_number = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "transaction_vote"
    }

class Transaction_Results(Transaction):

    __tablename__ = "transactions_results"

    id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)

    candidate_number = Column(Integer)
    number_of_votes = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "transaction_results"
    }




