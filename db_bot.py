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

# Класс типов консенсуса
class Сonsensus(Base):
    __tablename__ = 'consensuses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
# Класс распространенности
class Adoption(Base):
    __tablename__ = 'adoptions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
# Класс криптовалют
class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    name = Column(String)
    consensus_id = Column(Integer, ForeignKey('consensuses.id'))
    consensus = relationship("Сonsensus", foreign_keys=[consensus_id])
    has_smart_contract = Column(Boolean)
    adoption_id = Column(Integer, ForeignKey('adoptions.id'))
    adoption = relationship("Adoption", foreign_keys=[adoption_id])


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

# 4 - create data from https://www.home.saxo/content/articles/cryptocurrencies/crypto-comparison-07102021
# adoption creation
ad_low = Adoption()
ad_low.name = "Low"

ad_med = Adoption()
ad_med.name = "Medium"

ad_high = Adoption()
ad_high.name = "High"

# Consensuses creation
prow = Сonsensus()
prow.name = "PoW"
prow.description = "Proof of work"

pros = Сonsensus()
pros.name = "PoS"
pros.description = "Proof of stake"

othcons = Сonsensus()
othcons.name = "Other"
othcons.description = "Other"

# Cryptocurrencies creation
btc = Cryptocurrency()
btc.name = "Bitcoin"
btc.ticker = "BTC"
btc.consensus = prow
btc.has_smart_contract = False
btc.adoption = ad_high

eth = Cryptocurrency()
eth.name = "Ethereum"
eth.ticker = "ETH"
eth.consensus = prow
eth.has_smart_contract = True
eth.adoption = ad_high

ltc = Cryptocurrency()
ltc.name = "Litecoin"
ltc.ticker = "LTC"
ltc.consensus = prow
ltc.has_smart_contract = True
ltc.adoption = ad_low

bnb = Cryptocurrency()
bnb.name = "Binance Coin"
bnb.ticker = "BNB"
bnb.consensus = pros
bnb.has_smart_contract = True
bnb.adoption = ad_high

bch = Cryptocurrency()
bch.name = "Bitcoin Cash"
bch.ticker = "BCH"
bch.consensus = prow
bch.has_smart_contract = False
bch.adoption = ad_low

ada = Cryptocurrency()
ada.name = "Cardano"
ada.ticker = "ADA"
ada.consensus = pros
ada.has_smart_contract = True
ada.adoption = ad_low

dot = Cryptocurrency()
dot.name = "Polkadot"
dot.ticker = "DOT"
dot.consensus = pros
dot.has_smart_contract = False
dot.adoption = ad_low

xrp = Cryptocurrency()
xrp.name = "Ripple"
xrp.ticker = "XRP"
xrp.consensus = othcons
xrp.has_smart_contract = False
xrp.adoption = ad_low

sol = Cryptocurrency()
sol.name = "Solana"
sol.ticker = "SOL"
sol.consensus = pros
sol.has_smart_contract = True
sol.adoption = ad_med

xlm = Cryptocurrency()
xlm.name = "Stellar"
xlm.ticker = "XLM"
xlm.consensus = othcons
xlm.has_smart_contract = True
xlm.adoption = ad_low

xtz = Cryptocurrency()
xtz.name = "Tezos"
xtz.ticker = "XTZ"
xtz.consensus = pros
xtz.has_smart_contract = True
xtz.adoption = ad_low

trx = Cryptocurrency()
trx.name = "Tron"
trx.ticker = "TRX"
trx.consensus = pros
trx.has_smart_contract = True
trx.adoption = ad_med





# pair creation
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
user_2.fav_currency = xtz

user_3 = User()
user_3.chat_id = "9231139"
user_3.name = "Test_User"
user_3.current_state = "begin"



# 9 - persists вata
# session.add(ad_low)
# session.add(ad_med)
# session.add(ad_high)
#
# session.add(pros)
# session.add(prow)
# session.add(othcons)
#
#
# session.add(btc)
# session.add(eth)
# session.add(ltc)
# session.add(bnb)
# session.add(bch)
# session.add(ada)
# session.add(dot)
# session.add(xrp)
# session.add(sol)
# session.add(xlm)
# session.add(xtz)
# session.add(trx)
#
# session.add(btc_eth)
# session.add(user_1)
# session.add(user_2)
# session.add(user_3)

# Base.metadata.drop_all(bind=engine)
# 10 - commit and close session
session.commit()
session.close()

