## Google Maps API

A friend of mine was building a database of dental facilities in and around Łódź. She needed the following: name, address, phone number, and websiste address. Within a couple of hours I was able to provie her some excel files so that she could analyse the data. I utilized a Text Search API and a Place Details API. The Text Search API returns information about a set of places based on a string — for example "pizza in New York" or "shoe stores near Ottawa" or "123 Main Street". The service responds with a list of places matching the text string and any location bias that has been set. A Place Details request returns more comprehensive information about the indicated place such as its complete address, phone number, user rating and reviews. 
The workflow is:
* For a given location and each keyword from the list of keywords query the Text Search API
* Then query the Place Details API with the places ID's obtained in the previous step
* Save the data to an Excel file which name is the name of the location
* Use tqdm for showing the progress bar and for estimating the remaining time