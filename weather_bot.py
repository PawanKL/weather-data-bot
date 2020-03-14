import time
import pandas as pd
import numpy as np
from selenium import webdriver
import datetime, calendar
geckodriver = 'E:\\Softwares\\geckodriver-v0.26.0-win64\\geckodriver.exe' # add your geckodriver path
url = 'https://www.wunderground.com/history/daily/pk/karachi/OPKC/date/'
class Bot:
    def __init__(self, geckoDriver, url):
        self.geckoDriver = geckoDriver
        self.url = url
        self.days = []
        self.temp = []
        self.dataFile = 'weather_data.csv'
    def getDriver(self):
        return webdriver.Firefox(executable_path=self.geckoDriver)
    def delay(self, seconds):
        time.sleep(seconds)
    def getDates(self):
        year = 2019
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        for i in range(len(months)):
            num_days = calendar.monthrange(year, months[i])[1]
            days = [datetime.date(year, months[i], day) for day in range(1, num_days+1)]
            for day in days:
                self.days.append(str(day))
    def startScrape(self, driver):
        for day in self.days:
            new_url = self.url + day
            print(new_url)
            driver.get(new_url)
            self.delay(20)
            td_actual = driver.find_element_by_xpath('/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[1]/td[1]')
            self.temp.append(td_actual.text)
    def saveData(self):
        data = pd.DataFrame()
        data['Date'] = np.array(self.days)
        data['Temp'] = np.array(self.temp)
        data.to_csv(self.dataFile, index=False)

if __name__ == "__main__":
    bot = Bot(geckodriver, url)
    bot.getDates()
    driver = bot.getDriver()
    bot.delay(5)
    bot.startScrape(driver)
    bot.saveData()
    driver.close()