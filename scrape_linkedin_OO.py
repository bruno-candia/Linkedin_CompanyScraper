# == BROWSER MODULES ==
from selenium import webdriver # selenium is a module that allows you to automate web browsing
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, ElementNotVisibleException
from webdriver_manager.chrome import ChromeDriverManager #webdriver_manager is a package that allows you to manage webdrivers
  
# == STATISTICS MODULES ==
import matplotlib.pyplot as plt # matplotlib is a module that allows you to plot the statistics
import pandas as pd # pandas is a module that allows you to create dataframes and make more statistics things
import numpy as np # numpy is a module that allows you to create arrays 

# == PYTHON MODULES ==
import re # re is a module that allows you to use regular expressions
import getpass # getpass is a module that allows you to hide your password
import parsel # parsel is a module that allows you to parse html
import csv # csv is a module that allows you to write to csv
import time # time is a module that allows you to wait for a certain amount of time


class scraping_linkedin:

  def __init__(self,username, password, chrome_profile_path):
    self.username = username
    self.password = password
    self.chrome_profile_path = chrome_profile_path
    self.options = self.open_webdriver()
    self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.options)

  def open_webdriver(self):
    self.options = webdriver.ChromeOptions() 
    # Set the chrome driver window size
    self.options.add_argument("window-size=1900,1000")
    # Set the chrome driver path
    self.options.add_argument(f"--user-data-dir={self.chrome_profile_path}")
    # Set the chrome driver profile to use 
    self.options.add_argument('--profile-directory=Default')
    
    return self.options

  def login(self):
    # Instance of Chrome webdriver
    # self.driver.set_window_position(0, 2000)
    self.driver.maximize_window()
    # Open login page of linkedin
    self.driver.get('https://www.linkedin.com/login')
    if self.driver.current_url == 'https://www.linkedin.com/login':
        # find the email input field and enter the email
        input_username = self.driver.find_element_by_id('username')
        input_username.click()
        input_username.clear()
        input_username.send_keys(self.username)
        # find the password input field and enter the password
        input_password = self.driver.find_element_by_id('password')
        input_password.click()
        input_password.clear()
        input_password.send_keys(self.password)
        # submit to login
        print(self.driver.find_element_by_xpath('//*[@type="submit"]'))
        self.driver.find_element_by_xpath('//*[@type="submit"]').submit()


    # get_company_posts_data is a function that allows you to get the data from the company posts
  def get_company_posts_data(self):
        
    # Search for the company button on the page
    wait = WebDriverWait(self.driver, 10, poll_frequency=2, ignored_exceptions=[ElementNotVisibleException, ElementNotInteractableException])
    company_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-control-name="pages_admin_module_name"]')))
    # get the company url on href attribute
    company_link = company_element.get_attribute('href')
    # go to the company page
    self.driver.get(company_link)
    # call scroll down function
    self.__scroll_down(self.driver)
    elements = self.driver.find_elements_by_xpath('//button[@class="org-update-analytics__toggle-details-btn t-14 t-black--light t-bold"]')
    
    for element in range(len(elements)):
        # click the button
        self.driver.execute_script(f"document.getElementsByClassName('org-update-analytics__toggle-details-btn t-14 t-black--light t-bold')[{element}].click()")

    sel = parsel.Selector(self.driver.page_source)
    date_post_company = self.__clean_company_data(sel.xpath('//span[@class="org-update-posted-by-selector__date"]/text()').extract())
    statistic_company = self.__clean_company_data(sel.xpath('//dt[@class="t-20 t-black--light t-normal"]/text()').extract())

    views = []
    likes = []
    comments = []
    click_rate = []
    share = []
    click = []
    engagement_rate = []

    self.data = [views, likes,click_rate, comments, share, click, engagement_rate, date_post_company]

    for i in range(len(statistic_company)//7):
        for j in range(7):
            self.data[j].append(statistic_company[i*7+j])

    return self.data

  # plot_statistics is a function that allows you to plot the statistics
  def plot_statistics(self):
    # Reverse the list so that the most recent data is on top
    for i in range(len(self.data)):
        self.data[i].reverse()
        # Create a dataframe
    arr = np.array(self.data)
    df = pd.DataFrame(arr.transpose(), columns=['views', 'likes','click_rate', 'comments', 'share', 'click', 'engagement_rate', 'date_post_company'])
    df[['views', 'likes','click_rate', 'comments', 'share', 'click', 'engagement_rate']] = df[['views', 'likes','click_rate', 'comments', 'share', 'click', 'engagement_rate']].apply(pd.to_numeric)
    
    # Plot the data
    df.plot(x='date_post_company', y=['likes', 'comments', 'share', 'click'], kind='line', figsize=(15,10),)
    plt.show()

    
    
    return df

  # clean_company_data is a function that allows you to clean the data from the company posts
  def __clean_company_data(self, data_array):
    data = []

    for tag in data_array:
        strtag = str(tag)
        #the first argument in findall (below) is a regular expression (accounts for commas in the number)
        list_of_matches = re.findall('[,0-9]+/[0-9]*/[0-9]*|[,0-9]+', strtag)
        #converts the last element (string) in the list to int, appends to like list
        if list_of_matches:
            last_string = list_of_matches.pop()
            without_commas = last_string.replace(',', '.')
            data_str = str(without_commas)
            data.append(data_str)
        
    return data

      
    # scroll_down is a function that allows you to scroll down the page
  def __scroll_down(self, driver):
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height




# main is a function that allows you to run the program
def main():
    # get login and password from user
    print('== LIKEDIN LOGIN ==')
    username = str(input('Email or phone: '))
    password = str(getpass.getpass('Password: ', stream=None))
    chrome_profile_path = str(input('Caminho do perfil do Chrome: '))
    try:
        bruno = scraping_linkedin(username=username, password=password
        ,chrome_profile_path=chrome_profile_path)
        bruno.login()
        bruno.get_company_posts_data()
        bruno.plot_statistics()

    except Exception as e:
        print(e)
        bruno.driver.quit()

# run main function if file is run directly
if __name__ == '__main__':
    main()
