# eNamScrapping
#### Scrapping Agriculture data from eNam website using Selenium library, then clean that raw data using Pandas library in Python and upload it to MongoDB
#### [eNam Website](https://enam.gov.in/web/dashboard/trade-data)
1. The Code is given in jupyter Notebook.ipynb and .py format.
2. Directory path of **```Gramoday_Datasets_market.xlsx, cmdtyMapData.xlsx, apmcMapData.xlsx file```** need to be changed while running on other machine.
3. **```Gramoday_Datasets_market.xlsx, cmdtyMapData.xlsx, apmcMapData.xlsx file```** file is attached.



```Python version 3.7.9 (default, Aug 31 2020, 17:10:11) [MSC v.1916 64 bit (AMD64)] Version info. sys.version_info(major=3, minor=7, micro=9, releaselevel='final', serial=0)```

1. ```open Anaconda prompt, change file directory path i.e., cd path_to_folder```
2. **```conda create -n eNamScrapping python=3.7```**
3. **```conda activate eNamScrapping```**
4. **```conda install spyder```**
5. ```pip install -r path_of_requirments.txt```
6. **```pymongo==3.11.4```**
7. **```requests==2.25.1```**
8. **```pandas==1.2.0```**
9. After above installation type **```spyder```** in Anaconda prompt. Now Spyder IDE will open in sometime.
10. open **```eNamDataPullClean.py```** in spyder

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### Screenshots of works done
1. #### **eNam Website Data Page (This Tabular data needs to be extracted)**
![Website Data Page (This Tabular data needs to be extracted)](https://github.com/sanjeebKumarGouda/eNamScrapping/blob/main/resources/1.png)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2. #### **Extracted Raw Data**
![Extracted Raw Data](https://github.com/sanjeebKumarGouda/eNamScrapping/blob/main/resources/2.png)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3. #### **Extracted Cleaned Data_1**
![Extracted Cleaned Data](https://github.com/sanjeebKumarGouda/eNamScrapping/blob/main/resources/3.png)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
4. #### **Extracted Cleaned Data_2**
![Extracted Cleaned Data](https://github.com/sanjeebKumarGouda/eNamScrapping/blob/main/resources/4.png)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
5. #### **Cleaned Data uploaded to MongoDB**
![Extracted Cleaned Data](https://github.com/sanjeebKumarGouda/eNamScrapping/blob/main/resources/5.png)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
