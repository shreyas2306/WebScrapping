# Web-Scrapping

This project aims to extract the text data from 'New York Times' political section after every 30 mins using 
web scrapping technology and job scheduler.

When you run the project, it will hit the nytimes/political section url and will start extracting the text data from url
and store in a text file after every 30 mins making sure that no same article is scrapped twice. 

## Basic Requirements
- **Python3.0+**

### Dependencies:

- bs4==4.8.0
- pandas==0.25.1
- numpy==1.17.3
- schedule==0.6.0

### Installation

Clone or download the repository in your local environment.

Go inside the directory of the project and use the following command:

`pip install -r requirements.txt`

then run the following command:

`python main.py`

