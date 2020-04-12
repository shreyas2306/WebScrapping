from WebScraping.WebScraping import *
import schedule
import datetime


def job_scheduler():

    """
    Method to Run the tasks after every given interval.

    """

    print(datetime.datetime.now())
    webscraping_obj = WebScraping()
    webscraping_obj.get_url()
    webscraping_obj.scrape_url()
    webscraping_obj.scrape_data_info()
    

schedule.every(30).minutes.do(job_scheduler) #Schedule the task after every 30mins

while True:
    schedule.run_pending()
    time.sleep(1)



