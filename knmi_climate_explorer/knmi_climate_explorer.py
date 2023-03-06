from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List
import pandas as pd
import numpy as np


def scrap_data(url:str) -> List[List]:
    ''' Get raw text data using urlopen and bs4 packages, then convert it to a list of lists
    
    :param url: website url
    :type url: str
    :return: unformatted list of lists, i.e. a table in the form of 2 lists
    :rtype: List[List]
    '''
    # Use context manager to get the website's content
    with urlopen(url=url) as f:
        html = f.read().decode('utf-8')
    soup = BeautifulSoup(markup=html, features='html.parser')
    
    # Convert bs4.BeautifulSoup object to string
    soup_text = soup.get_text()
    
    # Create a list by splitting the string
    soup_text_split = soup_text.split(sep='\n')

    # Remove lists that are empty and these which contains '#' sign at the beginning
    # Source: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
    table_text = [row for row in soup_text_split if row and '#' not in row[:2]]
    
    return table_text


def preprocess_data(table: List[List]) -> List[List]:
    ''' Remove empty strings in each list in a main list
    
    :param table: unformatted list of lists
    :type table: List[List]
    :return: formatted list of lists, i.e. a table in the form of 2 lists
    :rtype: List[List]
    '''
    # Initialize an empty list
    table_preprocessed = []
    
    # Iterate over each row in a list
    for row in table:
        
        # Firstly, split the string in a row with spaces 
        row = row.split(sep=' ')
        
        # Secondly, remove all '' strings
        # Source: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
        row = [elem for elem in row if elem]
        
        # Append the result to the list
        table_preprocessed.append(row)
        
    return table_preprocessed


def get_dataframe(table: List[List]) -> pd.DataFrame:
    ''' Create a dataframe from the list of lists and then format it from long to wide format
    
    :param table: formatted list of lists, i.e. a table in the form of 2 lists
    :type table: List[List]
    :return: dataframe with a 'datetime' index and a 'value' column
    :rtype: pd.DataFrame
    '''
    df = pd.DataFrame(data=table)
    df = df.rename(columns={0: 'year'})
    df = pd.melt(frame=df, id_vars='year', value_vars=df.columns[1:], var_name='month')
    df['datetime'] = pd.to_datetime(arg=df['year'].astype(dtype=str) + df['month'].astype(dtype=str), format='%Y%m')
    df = df.set_index(keys='datetime')
    df = df.drop(columns=['year', 'month']).copy()
    df['value'] = df['value'].astype(dtype=float)
    df = df.sort_values(by=['datetime'])
    df.loc[df['value'] == -999.90, ['value']] = np.nan
    
    return df

# if __name__ == "__main__" idiom is a way to store code that should only run when the file is executed as a script
if __name__ == '__main__':
    url = 'http://climexp.knmi.nl/data/icpc_nao.dat'
    data_raw = scrap_data(url=url)
    data_preprocessed = preprocess_data(table=data_raw)
    nao_monthly = get_dataframe(table=data_preprocessed)
    nao_monthly.to_pickle(path='knmi_climate_explorer/nao_monthly.pkl')