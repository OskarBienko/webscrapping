## biznes_pap

A company introducing its shares to trading on an organized market must sign an agreement with a news agency. In Poland it's the Polish Press Agency (Polska Agencja Prasowa - PAP). 
Through PAP a listed companies provide relevant information regarding their activities. Though there is a subpage with companies names and associated id numbers, the companies that have disappeared from the stock exchange for any reason are missing. However, there are historical reports for these companies. To sum up, the aim of the project was to get companies names based on id number. This information is vital for scraping historical financial reports in the future. It seems that PAP gives each company an id number from 1, incrementing by 1, to some (unknown) number. The workflow is:
* For a given id number, from 1 to 2000 (arbirary number) construct an url and try to open it
* If it's opened, get the name of a company, otherwise set a company name as NaN
* Save both an id number and a company name to pickle file after each iteration
* Use tqdm for showing the progress bar and for estimating the remaining time