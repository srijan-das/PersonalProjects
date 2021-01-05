import pandas as pd
import pandas_datareader.data as pdr
import time

#Defining Universe
it_tickers = list("TCS	INFY	HCLTECH	WIPRO	TECHM	LTI	HONAUT	BEL	OFSS	MPHASIS	MINDTREE	HEXAWARE	NIITTECH	TATAELXSI	PERSISTENT	INFIBEAM	REDINGTON	VAKRANGEE	FSL	ZENSARTECH	CYIENT	BSOFT	SONATSOFTW	ECLERX	KPITTECH	INTELLECT	ACCELYA	HGS	RSYSTEMS	TANLA	NEWGEN	ASTRAMICRO	MAJESCO	MASTEK	AGCNET	NUCLEUS	CIGNITITEC	QUICKHEAL	SASKEN	GENUSPOWER".split())
finance_tickers = list("HDFCBANK	HDFC	KOTAKBANK	ICICIBANK	BAJFINANCE	SBIN	AXISBANK	HDFCLIFE	BAJAJFINSV	SBILIFE	SBICARD	BANDHANBNK	ICICIPRULI	ICICIGI	HDFCAMC	IDBI	MUTHOOTFIN	INDUSINDBK	PNB	PEL	YESBANK	BAJAJHLDNG	BANKBARODA	PFC	RECLTD	AUBANK	NIACL	NAM-INDIA	IOB	CHOLAFIN	ISEC	BANKINDIA	IDFCFIRSTB	CANBK	MFSL	ABCAPITAL	LICHSGFIN	L&TFH".split())
real_estate_tickers = list("DLF	GODREJPROP	PHOENIXLTD	PRESTIGE	IBREALEST	NESCO	BRIGADE	SUNTECK OMAXE	MAHLIFE	ANANTRAJ	ASHIANA	TEXINFRA	IBULISL	KARDA	BINDALAGRO	ARVSMART	PROZONINTU	MARATHON	VIPULLTD	NILAINFRA	DBREALTY	HDIL	PARSVNATH	GEECEE	GANESHHOUC	PODDARHOUS	FMNL	PENINLAND	EMAMIREAL	TCIDEVELOP".split())
consumer_discretionary_tickers = list("MARUTI	DMART	TITAN	BAJAJ-AUTO	M&M	HEROMOTOCO	BOSCHLTD	TATAMOTORS	MOTHERSUMI	WHIRLPOOL	MRF	BALKRISIND	SRF	TRENT	PAGEIND	JUBLFOOD	VOLTAS	TVSMOTOR	BATAINDIA	RELAXO	CROMPTON	RAJESHEXPO	WABCOINDIA	ENDURANCE	SCHAEFFLER	ABFRL	INDHOTEL	TIINDIA	SUNDRMFAST	MINDAIND	TTKPRESTIG	DIXON	SFL	APOLLOTYRE	SYMPHONY	JCHAC	FRETAIL	AMBER".split())
consumer_staples_tickers = list("HINDUNILVR	ITC	NESTLEIND	BRITANNIA	DABUR	GODREJCP	MCDOWELL-N	MARICO	TATACONSUM	COLPAL	PGHH	RUCHI	UBL	VBL	GILLETTE	HATSUN	EMAMILTD	GODREJAGRO	BBTC	ZYDUSWELL	AVANTIFEED	KRBL	RADICO	VSTIND	GODFRYPHLP	EIDPARRY	JYOTHYLAB	KSCL	CCL	TASTYBITE	BALRAMCHIN	FCONSUMER	BAJAJCON	RENUKA	GAEL	TATACOFFEE	VENKEYS	DAAWAT	TRIVENI	DIAMONDYD".split())
communication_services_tickers = list("BHARTIARTL	INFRATEL	NAUKRI	IDEA	IRCTC	ZEEL	SUNTV	ITI	INDIAMART	TV18BRDCST	PVR	HATHWAY	STRTECH	AFFLE	 NETWORK18	DEN	JUSTDIAL	INOXLEISUR	HFCL	NAVNETEDUL	DBCORP	DISHTV	TVTODAY	JAGRAN	MATRIMONY	VINDHYATEL	NXTDIGITAL	BALAJITELE	GTPL	SAREGAMA	TTML	MTNL	ENIL	RADIOCITY	JUMPNET	MPSLTD".split())
health_care_tickers = list("SUNPHARMA	DRREDDY	DIVISLAB	CIPLA	BIOCON	AUROPHARMA	TORNTPHARM	LUPIN	CADILAHC	ABBOTINDIA	ALKEM	GLAXO	IPCALAB	APOLLOHOSP	PFIZER	APLLTD	SANOFI	SYNGENE	LALPATHLAB	AJANTPHARM	NATCOPHARM	GLENMARK	JUBILANT	FORTIS	ASTRAZEN	METROPOLIS	PGHL	SUVENPHAR	LAURUSLABS	ASTERDM	ERIS	NH	GRANULES	JBCHEPHARM	SPARC	SHILPAMED	FDC	STAR	AARTIDRUGS	POLYMED".split())
industrials_tickers = list("LT	ADANIPORTS	EICHERMOT	SIEMENS	INDIGO	HAVELLS	HAL	CONCOR	3MINDIA	ABB	ADANIENT	AIAENG	ASHOKLEY	LTTS	BHEL	ESCORTS	ASTRAL	EXIDEIND	POLYCAB	GMRINFRA	AMARAJABAT	CUMMINSIND	THERMAX	SKFINDIA	BDL	TIMKEN	VGUARD	KEC	RITES	KAJARIACER	GMMPFAUDLR	FINPIPE	GRINDWELL	SIS	QUESS	WESTLIFE	CARBORUNIV	RATNAMANI	BLUEDART	NBCC".split())
materials_tickers = list("ASIANPAINT	ULTRACEMCO	COALINDIA	SHREECEM	HINDZINC	PIDILITIND	BERGEPAINT	JSWSTEEL	VEDL	GRASIM	AMBUJACEM	TATASTEEL	HINDALCO	UPL	BAYERCROP	NMDC	ACC	PIIND	KANSAINER	COROMANDEL	JINDALSTEL	BHARATFORG	AARTIIND	RAMCOCEM	SAIL	SUPREMEIND	ATUL	SUMICHEM	DALBHARAT	GODREJIND	CASTROLIND	JKCEMENT	VINATIORGA	SOLARINDS	NAVINFLUOR	AKZOINDIA	TATACHEM	DEEPAKNTR	NATIONALUM	CHAMBLFERT".split())
list_of_sectors = [it_tickers, finance_tickers, real_estate_tickers, consumer_discretionary_tickers, consumer_staples_tickers, communication_services_tickers, health_care_tickers, industrials_tickers, materials_tickers]
sector_names = ['IT','Finance','Real Estate','Cons. Discretionary','Cons. Staples','Comms Services','Health Care','Industrials','Materials']

#Fetching Data 
start_date = pd.to_datetime('2016-01-01')
end_date = pd.to_datetime('2020-08-12')

for industry in list_of_sectors:
    i=0
    for _ in industry:
        industry[i] = industry[i]+".NS"
        i+=1

universe_total = {}
i=0
for ind in list_of_sectors:
    attempts = 0
    drop = []
    universe_total[sector_names[i]] = pd.DataFrame()
    while len(ind) != 0 and attempts < 5 :
        ind = [j for j in ind if j not in drop]
        for tick in ind:
            try:
                print("Fetching :", tick)
                temp = pdr.get_data_yahoo(tick, start_date, end_date)
                universe_total[sector_names[i]][tick+'Close'] = temp['Close']
                drop.append(tick)
            except:
                print("Unable to fetch {}. Retrying ....".format(tick))
                time.sleep(10)
                continue
        attempts+=1
    ind = drop
    i+=1

# splitting into test and train data sets
universe_test = {}
universe_train = {}

for sector in universe_total :
  universe_train[sector] = universe_total[sector].loc[:'2019-12-31']
  universe_test[sector] = universe_total[sector].loc['2020-01-01':]

#Calculatig the CAGR
import numpy as np
CAGR_train_stocks = {}
CAGR_train_industry = {}

for industry in universe_train :
  temp_dict = {}
  for stock in universe_train[industry].columns.to_list() :
    temp_dict[stock] = ((universe_train[industry][stock][-1]/universe_train[industry][stock][0])**(0.25)-1)*100
  CAGR_train_stocks[industry] = temp_dict
print('____________________________________________________________________')
print("CAGR for stocks for 2016-01-01 to 2019-12-31: ")
for industry in CAGR_train_stocks :
  print(industry,':',CAGR_train_stocks[industry])
  CAGR_train_industry[industry] = np.array(list(CAGR_train_stocks[industry].values())).mean()
print('\n'+'Industry Average During Period: ')
print(CAGR_train_industry)
print('____________________________________________________________________')

