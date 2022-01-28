import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# create an engine
engine = create_engine('sqlite:///cryptodb.db')


# create a configured "Session" class
Session = sessionmaker(bind=engine)

Base = declarative_base()


# Класс криптовалют
class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    name = Column(String)


# Класс пар криптовалют (торговые пары)
class Pair(Base):
    __tablename__ = 'pairs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    currency_1_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    currency_1 = relationship("Cryptocurrency", foreign_keys=[currency_1_id])
    currency_2_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    currency_2 = relationship("Cryptocurrency", foreign_keys=[currency_2_id])


# Класс пользователей и их состояний
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_id = Column(String)
    current_state = Column(String)
    fav_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    fav_currency = relationship("Cryptocurrency", foreign_keys=[fav_currency_id])

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create data
btc = Cryptocurrency()
btc.name = "Bitcoin"
btc.ticker = "BTC"

eth = Cryptocurrency()
eth.name = "Ethereum"
eth.ticker = "ETH"

usdt = Cryptocurrency()
usdt.name = "Tether"
usdt.ticker = "USDT"

btc_eth = Pair()
btc_eth.name = "Btc_Eth"
btc_eth.currency_1 = btc
btc_eth.currency_2 = eth

user_1 = User()
user_1.chat_id = "9231139"
user_1.name = "Rinat"
user_1.current_state = "begin"

user_2 = User()
user_2.chat_id = "0000"
user_2.name = "Zhenya"
user_2.current_state = "begin"
user_2.fav_currency = usdt

user_3 = User()
user_3.chat_id = "9231139"
user_3.name = "Test_User"
user_3.current_state = "begin"



# 9 - persists ata
# session.add(btc)
# session.add(eth)
# session.add(usdt)
# session.add(btc_eth)
# session.add(user_1)
# session.add(user_2)
# session.add(user_3)

# Base.metadata.drop_all(bind=engine)
# 10 - commit and close session
session.commit()
session.close()