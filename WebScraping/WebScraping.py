#Import required libraries
import requests
import time
import urllib.request
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import numpy as np
import dateutil.parser as parser
import os
import re

class WebScraping:

    """
    Class is created to extract/scrape the text data from Online websites to create a corpus.

    It allows user to select a website from which they can extract the text data to create corpus of the required domain.

    """

    def __init__(self):
        """ 
        Constructor: Initialize the Input dictionary
        
        @param url_dic: Python Dictionary for storing the URL to be scraped.

        """
        
        self.url_dic = {'1': 'https://www.nytimes.com/section/politics/'}
        

    def get_url(self):
        """ 
        Method to get the URL from user to be scraped.

        @Returns: URL

        """
        try:
            #self.url_input = input('Please enter the Number: ') #For later stages
            self.url_input = '1'
            self.url = self.url_dic[self.url_input]

        except:
            print('ERROR !! Please Enter the Number')
            self.get_url()
            
        return self.url
    
    def scrape_url(self):
        """
        Method to select the url of articles to extract text.

        @Returns: List of urls from which to extract text.

        """

        #Hit the url to get the page content
        response = requests.get(self.url)
        
        #Initialize BeutifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        self.url_list = []
        latest_news_container = soup.findAll('div', {'class': 'css-1l4spti'})
        
        for container in latest_news_container:
            self.url_list.append('https://www.nytimes.com/' + container.a['href'])
          
        
        
        return self.url_list

    
    def scrape_data_info(self):
        """
        Method to extract the required information and text from the urls.
        
        """



        article_id = [] #list for storing articleid
        date_modified = [] #list for storing date modified
        update_url = [] #list for storing updated url
        text = [] #list for storing text
        flag = None #Changes when there is an update in values

        if os.path.exists('.//WebScraping//Data//df_politics.csv'):
            df_politics = pd.read_csv('.//WebScraping//Data//df_politics.csv', index_col = [0]) #Load saved data
        else:
            df_politics  = pd.DataFrame(columns = ['ArticleId', 'DateModified', 'URL', 'Text']) #Create dataframe


        self.df_check = pd.DataFrame(columns = ['ArticleId', 'DateModified', 'URL', 'Text']) #Create dataframe for storing updated values

        for url in self.url_list: #Extracting required data from each url in self.url_list
            try:
                response = requests.get(url) #Getting the response from the url
                soup = BeautifulSoup(response.text, 'html.parser') #Converting the response to text using html parser
                for tag in soup.find_all('meta'): #Loop over meta tag in html 'head' to extract articleid and date modified
                    if tag.get('name', None) == 'articleid': #Extracting Article ID
                        a_id = int(tag.get('content', None)) #Storing article id in a_id variable
                        
                       
                    if tag.get('property', None) == 'article:modified': #Extracting Date Modified
                        d_modified = parser.parse(tag.get('content', None)).isoformat() #storing date modified in d_modified variable
                
                if a_id not in df_politics['ArticleId'].values: #If Article Id in new
                    article_id.append(a_id)#append article id to the list
                    date_modified.append(d_modified)#append date modified to the list
                    update_url.append(url)#append url to the list
                    text.append(self.scrape_text(soup))#append text using method 'scrape_text' to the list
                
                else: #If article id is not new
                    if d_modified > df_politics.DateModified[df_politics['ArticleId'] == a_id].values[0]: #Check if date modified has changed or not
                        df_politics.drop(df_politics[df_politics['ArticleId'] == a_id].index, inplace = True) #drop repeating row
                        article_id.append(a_id) #append article id to the list
                        date_modified.append(d_modified) #append date modified to the list
                        update_url.append(url) #append url to the list
                        text.append(self.scrape_text(soup)) #append text using method 'scrape_text' to the list

                

            except:
                pass
        if len(article_id) == len(date_modified) and len(article_id) > 0: #Check for update
            
            flag = 'Update' #Set flag as 'update'
            self.df_check['ArticleId'] = article_id #Add updated articleid list to the dataframe column
            self.df_check['DateModified'] = date_modified #Add updated datemodified list to the dataframe column
            self.df_check['URL'] = update_url #Add updated url list to the dataframe column
            self.df_check['Text'] = text #Add text to the dataframe column
        print(self.df_check)
        print('Url List :', len(update_url))
        print('Article List:', len(article_id))
        print('Date Modified :', len(date_modified))
        
        if flag == 'Update':
            self.concat = pd.concat([df_politics, self.df_check], ignore_index=True) #Concatenate the old df and the new one
            self.concat.to_csv('.//WebScraping//Data//df_politics.csv') #Store the new dataframe as csv
            self.write_text() #Calling method to save text extracted as txt file
    
    def scrape_text(self, soup):

        """
        Method to extract Text from the url. 
        Called in 'scrape_data_info' method.

        @param soup: Object of BeautifulSoup.

        @Returns: Extracted text from the articles.

        """


        text = '' #Initialize empty string
        container_p = soup.findAll('p', {'class' : 'css-exrw3m evys1bk0'}) #Extracting the container that contains the text
        try:
            for txt in container_p:
                text = text + txt.text #Appending the text

        except:
            text = ''        
        
        return text

    def write_text(self):

        """
        Method to write the extracted text in a text file.
        Called in 'scrape_data_info' method.

        """


        text = '' #Initialize empty string
        text = text + str(self.df_check['Text'].values) 
        text = self.preprocess_text(text) #Calling the method 'preprocess_text'.
        if os.path.exists('.//WebScraping//Data//politics_text.txt'): #Check if the text file exists or not
            file = open('.//WebScraping//Data//politics_text.txt', 'w') #Import the text
            file.write(text) #Append the new text to the existing
            file.close()
            # self.save_text(text_data)
        
        else:
            file = open('.//WebScraping//Data//politics_text.txt', 'w') #Created txt file
            file.write(text) #Add the text
            file.close()
            

    def preprocess_text(self, txt):
        
        """
        Method to Preprocess Text.
        It removes the non-required tokens from the text.

        @param txt: Raw text extracted from the article.

        @Returns: Processed text.
        
        """


        txt = re.sub('/', '', txt) #Remove '/' from text
        txt = re.sub('nan', '', txt) #Remove 'nan' from text
        txt = txt.strip() #Remove whitespaces

        return txt
        