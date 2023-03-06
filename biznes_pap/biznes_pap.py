from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import numpy as np
import time


def get_names(last_id: int) -> pd.Series:
    ''' Get companies names from the biznes.pap.pl website by starting from id=0, incrementing by 1, and ending before the last_id argument
    
    :param last_id: a number specifying at which company's id to stop scraping
    :type last_id: int
    :return: series with id numbers as an index and companies names as values
    :return type: pd.Series
    '''
    # Set options incognito mode and without actually opening a browser window (headless argument)
    # Also disable selenium loggin messages
    options = webdriver.ChromeOptions()
    options.add_argument(argument='--ignore-certificate-errors')
    options.add_argument(argument='--incognito')
    options.add_argument(argument='--headless')
    options.add_experimental_option(name='excludeSwitches', value=['enable-logging'])

    # Create a dictionary for storing names
    names = dict()
    
    for i in tqdm(iterable=range(1, last_id, 1)):
        url = f'https://biznes.pap.pl/pl/reports/espi/company/{i},0,0,0,1'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        # Wait so I don't overload the server
        time.sleep(1)
        
        # If there's a company for a given i, get its name
        try:
            # Get the path to the first row containting the name of the company (third column's header is NAZWA)
            row_path = driver.find_elements(by=By.XPATH, value='//table[@class = "espi"]//td[3]')[1]
            name = row_path.find_element(by=By.XPATH, value='./a').get_attribute(name='innerText')
            
        # If there is no company for a given i, set name to NaN
        except:
            name = np.nan
        
        # Update the dict  
        names[i] = name
        
        # Save to pickle - so if there is any interruption the data stored in a dictionary won't get lost
        pd.Series(data=names).to_pickle(path='pap_names.pkl')
    
    driver.quit()
    

# Use if __name__ == '__main__' idiom to store code that should only run when the file is executed as a script
if __name__ == '__main__':
    get_names(last_id=2000)