from tqdm import tqdm
from typing import List, Dict
import pandas as pd
import requests
import time

KEY = open('key.txt').read()

def get_place_details(df: pd.DataFrame = None) -> List[Dict]:
    
    """Download place details using the Place Details API

    :param df: dataframe with a 'place_id' column
    :type df: pd.DataFrame
    :return: List with the dictionaries, containing the 'fields' defined below
    :rtype: List[Dict]
    """
    
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    details = list()
    for place_id in tqdm(df['place_id']):
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,formatted_phone_number,website',
            'key': KEY,
        }
        response = requests.get(url, params=params)
        result = response.json().get('result', {})
        details.append(result)
        
    return details


def download_data(
    location: str = None,
    keywords: List[str] = None,
) -> None:
    
    """Download data for a given location and a collection of keywords
    using the Text Search API (explicitly) and the Details API (implicitly)

    :param location: name of the location, defaults to None
    :type location: str, optional
    :param keywords: keywords associated with the subject of interest, defaults to None
    :type keywords: List[str], optional
    """
    
    dfs = list()
    for keyword in keywords:
    
        # Step 1: Search using the Text Search API
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': f'{location} {keyword}',
            'key': KEY,
        }

        results_list = []
        while True:
            response = requests.get(url, params=params)
            results = response.json().get('results', [])

            for result in results:
                results_list.append(result)

            # Check if there are more results
            if 'next_page_token' not in response.json():
                break

            # Wait for a few seconds before making the next request
            time.sleep(3)

            # Use the pagetoken from the previous request to fetch the next page
            params['pagetoken'] = response.json()['next_page_token']
        
        results_df = pd.DataFrame(results_list)
        
        # Step 2: Search for place details using the Details API
        print(f'Getting the details for: {location} {keyword}')
        details = get_place_details(df=results_df)
        details = pd.DataFrame(details)
        dfs.append(details)
    
    df = pd.concat(objs=dfs, axis=0).drop_duplicates()
    df.to_excel(f'''{location.replace(' ', '_').lower()}.xlsx''')
    
    # Use if __name__ == '__main__' idiom to store code that should only run when the file is executed as a script
if __name__ == '__main__':
    download_data(location='Zgierz', keywords=['stomatolog', 'dent'])
    