import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
import seaborn as sns
import time

# Downloadedd from Ministry of Statistics
inflation_df = pd.read_csv(r"C:\Users\Srijan\Documents\Python Scripts\Projects\Project 5 -  How well do stocks hedge against inflation in India\All_India_Index_july2019_20Aug2020.csv")

#Cleaning up the Data
inflation_df = inflation_df.replace({'Marcrh':'March','November ':'November'})
inflation_df['Time'] = pd.to_datetime(inflation_df['Month'].astype('str') + ' ' + inflation_df['Year'].astype('str'))
inflation_df.drop(['Year','Month'], axis=1, inplace=True)
inflation_df = inflation_df[inflation_df.Sector == 'Rural+Urban']
inflation_df = inflation_df.set_index('Time')
inflation_df['General index'].dropna(axis=0, inplace=True)

# Visualization of Trend of General Index Values
'''
inflation_df['General index'].plot()
plt.xlabel('Time')
plt.ylabel('General Index')
plt.legend()
plt.title("Consumer Price Index, India\n Jan, 2013 - Aug, 2020\n Base year, value 2012 = 100")
plt.tight_layout()
plt.show()
'''

# Calculating inflation rate, monthly
inflation_df['Monthly Inflation Rate'] = inflation_df['General index'].pct_change(1)*100
inflation_df['Cumulative Inflation'] = (inflation_df['General index']/inflation_df['General index'][0])*100

# Plotting Monthly Inflation rate
'''
inflation_df['Monthly Inflation Rate'].plot()
plt.xlabel('Time')
plt.ylabel('Monthly Inflation Rate, %')
plt.legend()
plt.title("Monthly Inflation Rate, India\n Jan, 2013 - Aug, 2020")
plt.axhline(y=0, color='r', linestyle='-')
plt.tight_layout()
plt.show()
'''

#Fetching and cleaning Sensex data
bse_df = pd.read_csv(r"C:\Users\Srijan\Documents\Python Scripts\Projects\Project 5 -  How well do stocks hedge against inflation in India\BSE Data.csv")
bse_df = bse_df.reset_index()
date_list = list()
for date in bse_df['index']:
    month, year = date.split('-')
    date_list.append(pd.to_datetime(month+' '+year))
bse_df.drop(['Close', 'index'], axis=1, inplace=True)
bse_df.columns = ['Open', 'High', 'Low', 'Close']
bse_df['Time'] = date_list
bse_df = bse_df.set_index('Time')

#Sensex Monthly Retruns
bse_df['BSE Monthly Returns'] = bse_df['Close'].pct_change(1)*100
bse_df['BSE Cumulative Returns'] = (bse_df['Close']/bse_df['Close'][0])*100

#Comparison df
final_df = pd.concat([inflation_df['Monthly Inflation Rate'], bse_df['BSE Monthly Returns'],inflation_df['Cumulative Inflation'], bse_df['BSE Cumulative Returns']], axis=1, keys=['Monthly Inflation Rate','BSE Monthly Returns','Cumulative Inflation','BSE Cumulative Returns'])
final_df.dropna(axis=0, inplace=True)
final_df.loc[final_df['BSE Monthly Returns'] > final_df['Monthly Inflation Rate'], 'BSE Exceeds inflation?'] = 'Yes'
final_df.loc[final_df['BSE Monthly Returns'] <= final_df['Monthly Inflation Rate'], 'BSE Exceeds inflation?'] = 'No' 

# Final Visualizations and Conclusion

#Plot 1 --> Comparison of monthly changes
final_df['BSE Monthly Returns'].plot(color='y')
final_df['Monthly Inflation Rate'].plot(color='g')
plt.title('Comparison of Monthly rates\nJan 2013 - June 2020')
plt.xlabel("Time")
plt.ylabel("Percentage %")
plt.legend()
plt.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
plt.show()

#Plot 2 --> Cumulative Effects
final_df['Cumulative Inflation'].plot(color='r')
final_df['BSE Cumulative Returns'].plot(color='g')
plt.title('Comparison of Cumulative rates\nJan 2013 - June 2020')
plt.xlabel("Time")
plt.ylabel("Percentage %")
plt.legend()
plt.tight_layout()
plt.show()

#Plot 3 -->
sns.countplot(x ='BSE Exceeds inflation?', data = final_df)
plt.show()