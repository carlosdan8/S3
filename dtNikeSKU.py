# MISIÓN 3RA SESIÓN
#%% DatSetNik.csv son los datos originales, queremos llegar a DataSetNike_sku.csv
import numpy as np
import pandas as pd

#DEFINE QUALITY REPORT TO GET INFO OF OUR DATA
def quality_report(data):

    """This method will do a basic data quality report for a data frame"""
        
    if (type(data) != pd.core.frame.DataFrame):
        raise TypeError("Data must be pandas.core.frame.DataFrame")
    else: 
        columns = list(data.columns.values)
        data_type = pd.DataFrame(data.dtypes, columns=['Data type'])
        missing_data = pd.DataFrame(
        data.isnull().sum(), columns=['missing values'])
        present_data = pd.DataFrame(data.count(), columns=['present values'])
        unique_values = pd.DataFrame(columns=['unique values'])
        minimum_values = pd.DataFrame(columns=['minimum values'])
        max_values = pd.DataFrame(columns=['maximun values'])
        
        for i in columns:
            unique_values.loc[i] = [data[i].nunique()]
            try:
                minimum_values.loc[i] = [data[i].min()]
                max_values.loc[i] = [data[i].max()]
            except:
                pass
        
        DQ_report = data_type.join(missing_data).join(present_data).join(
        unique_values).join(minimum_values).join(max_values)
    
    return DQ_report

csv_original = 'DataSetNike.csv'
dataset_original = pd.read_csv(csv_original, encoding = 'latin-1', low_memory = False)
dataset_original

quality_report(dataset_original)

dtNikeSKU = dataset_original[['Date', 'Material', 'Units']]
dtNikeSKU = dtNikeSKU.dropna()
dtNikeSKU = dtNikeSKU[dtNikeSKU.Units >= 1]
dtNikeSKU = dtNikeSKU.rename(columns = {'Material' : 'CÓDIGO'})

dtNikeSKU['Date'] = pd.to_datetime(dtNikeSKU['Date'])
dtNikeSKU['Month'] = dtNikeSKU['Date'].dt.month
dtNikeSKU['AÑO'] = dtNikeSKU['Date'].dt.year
dtNikeSKU = dtNikeSKU.sort_values(by = ['Month','AÑO'])
dtNikeSKU = dtNikeSKU.pivot_table(values = 'Units', index = ['CÓDIGO', 'AÑO'], columns='Month', fill_value=0,aggfunc = 'sum').reset_index(drop=False)
dtNikeSKU = dtNikeSKU.rename(columns = {1:'ENE',2:'FEB',3:'MAR',4:'ABR',5:'MAY',6:'JUN',7:'JUL',8:'AGO',9:'SEP',10:'OCT',11:'NOV',12:'DIC'})
dtNikeSKU = dtNikeSKU.sort_values(['AÑO','CÓDIGO'])
dtNikeSKU.to_csv('NikeSKU.csv')

print(dtNikeSKU)

