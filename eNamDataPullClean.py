# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 11:51:45 2021

@author: Sanjeeb
"""


from pymongo import MongoClient
import requests
import pandas as pd
import random
import socket
import struct
import datetime


def eNamDataPull(from_date,to_date):
    
    socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    url = 'https://enam.gov.in/web/Ajax_ctrl/trade_data_list'
    data = { "language" : "en", "stateName" : "-- All --", "apmcName" : "-- Select APMCs --", 
            "commodityName" : "-- Select Commodity --", "fromDate" : from_date, "toDate" : to_date}
    headers = {"Referer":"https://enam.gov.in/web/dashboard/trade-data", "Origin":"https://enam.gov.in"}
    
    r = requests.post(url,data,headers=headers)
    r.json()
    # print(r.ok)
    # print(r.headers)
    # print(r.encoding)
       
    data_dict = r.json()["data"]
    df_raw = pd.DataFrame(data_dict)            
    df_raw = df_raw [df_raw['modal_price'] != "0" ]
    df_raw.drop(['id','status','state','commodity_traded'],axis=1, inplace=True)    
    df_raw['apmc'] = df_raw['apmc'].str.title()
    df_raw['commodity'] = df_raw['commodity'].str.title()
    return df_raw

def dataMapping(df_raw):
    print("Importing data from mongo")
    try:
        connect = MongoClient("Enter your Connection String URI of MongoDB")
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
        
    db = connect.gramoday_new
    marketmain_df =  pd.DataFrame(list(db.market_main.find()))
    print("Fetched market main data")
    marketmain_df.drop(['_id','majorMandi', 'createdAt', 'updatedAt', '__v'], axis=1, inplace=True)
    
    raw_cmdtyGrade_df =  pd.DataFrame(list(db.cmdty_grade.find()))
    print("Fetched raw cmdtyGrade reports")
    raw_cmdtyGrade_df.drop(['_id', 'gradeDescr'], axis=1, inplace=True)
    raw_cmdtyGrade_df = raw_cmdtyGrade_df[raw_cmdtyGrade_df["defGrade"] == 1]
    
    df_apmc_map = pd.read_excel(r"C:\Users\Sanjeeb\Desktop\New folder\apmcMapData.xlsx")
    dict_raw_to_mapApmc = dict(zip(df_apmc_map['proper_apmc'].tolist(), df_apmc_map['mapped_apmc'].tolist()))
    df_raw['apmc'] = df_raw.apmc.map(dict_raw_to_mapApmc)
    
       
    dict_stdName_to_type = dict(zip(marketmain_df['stdName'].tolist(), marketmain_df['type'].tolist()))
    dict_stdName_to_marketID = dict(zip(marketmain_df['stdName'].tolist(), marketmain_df['marketID'].tolist()))
    dict_stdName_to_loclevel3 = dict(zip(marketmain_df['stdName'].tolist(), marketmain_df['loclevel3'].tolist()))
    df_raw['marketType'] = df_raw.apmc.map(dict_stdName_to_type)
    df_raw['loclevel3'] = df_raw.apmc.map(dict_stdName_to_loclevel3)
    df_raw['marketID'] = df_raw.apmc.map(dict_stdName_to_marketID)
    
    
    df_cmdty_map = pd.read_excel(r"C:\Users\Sanjeeb\Desktop\New folder\cmdtyMapData.xlsx")
    dict_raw_to_mapCmdty = dict(zip(df_cmdty_map['proper_commodity'].tolist(), df_cmdty_map['mapped_cmdty'].tolist()))
    df_raw['cmdtyStdName'] = df_raw.commodity.map(dict_raw_to_mapCmdty)
    
    df_crop_universe = pd.read_excel(r"C:\Users\Sanjeeb\Desktop\New folder\Gramoday_Datasets.xlsx")
    dict_stdName_to_cmdtyID = dict(zip(df_crop_universe['stdName'].tolist(), df_crop_universe['cmdtyID'].tolist()))
    df_raw['cmdtyID'] = df_raw.cmdtyStdName.map(dict_stdName_to_cmdtyID)
    
    
    
    df_raw.columns = ['marketStdName', 'varietyName', 'minPrice', 'modalPrice', 'maxPrice',
           'commodity_arrivals', 'dateOfReport', 'Commodity_Uom', 
           'marketType','loclevel3', 'marketID', 'cmdtyStdName', 'cmdtyID']
    
    
    df_dist = pd.read_excel(r"C:\Users\Sanjeeb\Desktop\New folder\Gramoday_Datasets.xlsx", sheet_name=1)
    dict_loclevel3_to_dist = dict(zip(df_dist['loclevel3'].tolist(), df_dist['name'].tolist()))
    df_raw['loclevel3Name'] = df_raw.loclevel3.map(dict_loclevel3_to_dist)
    
    df_raw['type'] = 'raw_secondary'
    df_raw['extContributorName'] = 'eNam'
    df_raw['extContributorID'] = '7'
    
    dict_cmdtyID_to_gradeID = dict(zip(raw_cmdtyGrade_df['cmdtyID'].tolist(), raw_cmdtyGrade_df['gradeID'].tolist()))
    dict_cmdtyID_to_gradeName = dict(zip(raw_cmdtyGrade_df['cmdtyID'].tolist(), raw_cmdtyGrade_df['gradeName'].tolist()))
    df_raw['gradeID'] = df_raw.cmdtyID.map(dict_cmdtyID_to_gradeID)
    df_raw['gradeName'] = df_raw.cmdtyID.map(dict_cmdtyID_to_gradeName)
    
    df_raw['varietyID'] = ''
    df_raw['createdAt'] = datetime.datetime.now()
    df_raw['processed'] = ''
    
    
    dict_unit = {'Qui':'Quintal', 'Kg':'Kg', 'Nos':'Nos'}
    df_raw['rawReportArrivalUnit'] = df_raw.Commodity_Uom.map(dict_unit)
    df_raw['rawReportPriceUnit'] = df_raw.Commodity_Uom.map(dict_unit)
    df_raw.drop(['Commodity_Uom'], axis=1, inplace=True)
    
    unitsMain_df =  pd.DataFrame(list(db.units_main.find()))
    print("Fetched unit main data")
    unitsMain_df.drop(['_id'], axis=1, inplace=True)
    dict_unitName_to_unitID = dict(zip(unitsMain_df['unitName'].tolist(), unitsMain_df['unitID'].tolist()))
    df_raw['rawReportArrivalUnitID'] = df_raw.rawReportArrivalUnit.map(dict_unitName_to_unitID)
    df_raw['rawReportPriceUnitID'] = df_raw.rawReportPriceUnit.map(dict_unitName_to_unitID)
    
    
    df_raw['baseFctrArrival'] = '1'
    df_raw['baseFctrPrice'] = '1'
    
    dict_convFctr = {'Quintal':100, 'Kg':1}
    df_raw['rawArrivalConvFctr'] = df_raw.rawReportArrivalUnit.map(dict_convFctr)
    df_raw['rawPriceConvFctr'] = df_raw.rawReportPriceUnit.map(dict_convFctr)
    df_raw.drop(['commodity_arrivals'],axis=1, inplace=True)
    
    df_raw.to_excel(r"C:\Users\Sanjeeb\Desktop\New folder\generatedOutput.xlsx", index=False)
    print("Data Mapped Sucessfully!!!")
    
if __name__ == "__main__":
    from_date = input("Enter from date in YYYY-MM-DD format\n")
    to_date = input("Enter to date in YYYY-MM-DD format\n")
    
    df_raw = eNamDataPull(from_date,to_date)
    dataMapping(df_raw)
