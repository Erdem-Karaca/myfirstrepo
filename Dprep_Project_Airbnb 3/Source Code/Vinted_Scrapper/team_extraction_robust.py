

#START WITH UNPICKLING USER PAGES DONT FORGET TO SAVE THE FILE IN YOUR PC AND WRITE IT IN THE CODE INSTEAD OF MY DIRECTORY
#UN-PICKLING

import pickle 

#with open(r'YOUR DIRECTORY ON WINDOWS', 'rb') as f:  # HERE: ADD YOUR DIRECTORY IF WINDOWS
with open('/Users/zeynep/Tilburg_Uni/oDCM/user_pages_toShare', 'rb') as f:  # HERE: ADD YOUR DIRECTORY on MacOS
    user_pages = pickle.load(f)
    
    
#DOWNLOAD LIBRARIES

import selenium.webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import hashlib
import json
#IF YOU GET ERROR ON "jsonpicle module not found" WRITE "pip install jsonpickle" to console on the right
import jsonpickle



###############################################################################
###############################################################################
#                            FUNCTIONS   START                                #
###############################################################################
###############################################################################

#Cookie Monster accepts cookies :)
def cookie_monster(driver):
        
            time.sleep(1.5)
            cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_button.click()
            time.sleep(2)    # WAIT FOR HTML TO BE LOADED, OTHERWISE BS4 IS FAILING
 
#Under development (error prevention if needed)
def handle_NoneType_while(check):
    x=0   
    while check is None:   
        x += 1
        driver = selenium.webdriver.Chrome()
        time.sleep(1.5)
        driver.get(user_page)
        cookie_monster(driver)
     #  userHTML= BeautifulSoup(driver.page_source)      
        print("I am in the " + str(x) +" while loop, please help :(")
        if x > 4:
            break              
       
def handle_NoneType(driver):
            
            print("NoneType Handler Triggered")
            print("Trying to refresh the page")
            time.sleep(1)
            driver.refresh()
            time.sleep(3)
            driver.refresh()
            time.sleep(3)
            userHTML = BeautifulSoup(driver.page_source)
            relevant_section = userHTML.find('div',attrs={'class':'body-content'})
            
            if relevant_section is None:
                print("Refresh did not worked! Resetting the driver...")
                driver = selenium.webdriver.Chrome()
                time.sleep(1.5)
                driver.get(user_page)
                time.sleep(2)
                cookie_monster(driver)
                time.sleep(2)
        
        
#Hashing        
def generate_hash(salt, input_string):
    # Ensure the salt is a byte string
    salt_bytes = salt.encode()
    # Combine the salt with the input_string (username)
    salted_input = salt_bytes + input_string.encode()
    # Create a hash object, using a secure hash algorithm (e.g., sha256)
    hash_object = hashlib.sha256(salted_input)
    # Generate the hexadecimal representation of the digest
    hash_hex = hash_object.hexdigest()
    # Return the salt and hash, concatenated
    return hash_hex

###############################################################################
###############################################################################
#                            FUNCTIONS   END                                  #
###############################################################################
###############################################################################
    

# L U
#  O S
#   O E
#    P R
#       S

user_info= []
user_dict= []
i=0     
x=0

###############      UNHASTAG ONLY YOUR PART      ####################

for user_page in user_pages[0:2]:    #CHIEM: Open this code only 
#for user_page in user_pages[861:1722]:    #CATARINA: Open this code only  
#for user_page in user_pages[1722:2583]:    #REBECCA: Open this code only 
#for user_page in user_pages[2583::]:    #ZEYNEP: Open this code only

    i+=1
    user_id= user_page.split("/")[4].split("-")[0]
    user_name= user_page.split("/")[4].split("-")[1::]

#RESET DRIVER ONCE EVERY 100TH LOOP- (for WEBSITE BLOCK PREVENTION)
    if i % 100 == 0 or i == 1:
        driver = selenium.webdriver.Chrome()
        time.sleep(1.5)
        driver.get(user_page)
        cookie_monster(driver)
    else:                       #OPEN USER PAGE  
        driver.get(user_page)
        time.sleep(1.5)
        

#REFRESH THE PAGE ONCE EVERY 3OTH LOOP- WEBSITE BLOCK PREVENTION 
 #   if i % 30 == 0:
 #       driver.refresh()
 #       time.sleep(3)
 #       driver.refresh()
 #       time.sleep(3)        
 #       driver.refresh()
 #       time.sleep(3)
      
#Get User page html
    userHTML= []                  #Delete previous user HTML
    relevant_section= []
    
    userHTML = BeautifulSoup(driver.page_source)
    relevant_section = userHTML.find('div',attrs={'class':'body-content'})   #BODY SECTION OF THE PAGE
    if relevant_section is None:
        print("Body Content not found! Resetting...")     #ERROR HANDLER IF PAGE IS NOT DOWNLOADED PROPERLY
        handle_NoneType(driver)
        userHTML = BeautifulSoup(driver.page_source)
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
   
#Get NUM OF ACTIVE LISTINGS

    listing_num = relevant_section.find('div',attrs={"class":"web_ui__Container__container"})
    if listing_num is None:               #ERROR HANDLER IF PAGE IS NOT DOWNLOADED PROPERLY try3x :)    
        userHTML = BeautifulSoup(driver.page_source)          
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        listing_num = relevant_section.find('div',attrs={"class":"web_ui__Container__container"})
        
        if listing_num is None:
            handle_NoneType(driver)
            userHTML = BeautifulSoup(driver.page_source)
            relevant_section = userHTML.find('div',attrs={'class':'body-content'})
            listing_num = relevant_section.find('div',attrs={"class":"web_ui__Container__container"})
            if listing_num is None:
                handle_NoneType(driver)
                userHTML = BeautifulSoup(driver.page_source)
                relevant_section = userHTML.find('div',attrs={'class':'body-content'})
                listing_num = relevant_section.find('div',attrs={"class":"web_ui__Container__container"})
    
    if len(listing_num.get_text())<1:
        user_info.append("User has no active listings")
        lst = "User has no active listings"
    else:    
        lst = listing_num.find("h2").get_text()
        user_info.append(lst)
        
 #GET USER LISTING CATEGORIES ONLY IF USER HAS LISTINGS

        cat_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/section/div/div[2]/section/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/div")
        cat_button.click()  ### Needs to be improved
        time.sleep(0.5)
        userHTML = BeautifulSoup(driver.page_source)    #DEBUGGING-this section is only retrievable when the category button is clicked, so refresh the user HTML 
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        cats=relevant_section.find_all("li",attrs={"class":"pile__element"}) #CATEGORIES
        time.sleep(0.5)
        
#Get CATEGORY INFO        
        categories=[]
        ii = 0
        for cat in cats:
            
            cat_name = cat.find("h2")   #category name
            cat_number = cats[ii].find("div", attrs = {"class":"web_ui__Cell__suffix"})   #Number of listings in that category
            categories.append({cat_name.get_text(), 
                               cat_number.get_text()})
            ii += 1


#Get number of Reviews

    reviews= userHTML.find("div", attrs={"class": "web_ui__Rating__label"})
    if reviews is None:
        user_info.append("No reviews yet")
    else:
        user_info.append(reviews.get_text())

#Get User Rating
    rating_section= relevant_section.find("div", attrs={"class": ("web_ui__Rating__rating", "web_ui__Rating__regular")})
    if rating_section.get("aria-label") is None:
        user_info.append("No ratings yet")
    else:
        rating = rating_section.attrs['aria-label']
        user_info.append(rating)

#Get Location Info

    location= relevant_section.find("div", attrs={"data-testid": "profile-location-info--content"})
    if location is None:                  #ERROR PREVENTION POINT
        user_info.append("No Location info")
    else:
        user_info.append(location.get_text())

# Get followers Info

    followers= relevant_section.find("a", attrs={"href": "/member/general/followers/"+user_id})
    if followers is None:
        handle_NoneType(driver)
        userHTML = BeautifulSoup(driver.page_source)
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        followers= relevant_section.find("a", attrs={"href": "/member/general/followers/"+user_id})

    user_info.append(followers.get_text() + " followers")
    
# Get following Info

    following= relevant_section.find("a", attrs={"href": "/member/general/following/"+user_id})
    if following is None:
        handle_NoneType(driver)
        userHTML = BeautifulSoup(driver.page_source)
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        following= relevant_section.find("a", attrs={"href": "/member/general/following/"+user_id})
    
    while following is None:   #the best ERROR PREVENTION POINT
        x += 1
        driver = selenium.webdriver.Chrome()
        time.sleep(1.5)
        driver.get(user_page)
        cookie_monster(driver)
        userHTML= BeautifulSoup(driver.page_source)
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        following= relevant_section.find("a", attrs={"href": "/member/general/following/"+user_id})
        print("I am in the " + str(x) +" while loop, please help :(")
        if x > 4:
            break
    x=0          
    user_info.append(following.get_text() + " following")
        
# Verified Channels   

    verified= relevant_section.find_all("li", attrs={"class" : "web_ui__Item__item"})
    if verified is None:
        handle_NoneType(driver)
        userHTML = BeautifulSoup(driver.page_source)
        relevant_section = userHTML.find('div',attrs={'class':'body-content'})
        verified= relevant_section.find_all("li", attrs={"class" : "web_ui__Item__item"})
        
    verified_channels=[]
    for item in verified:
        if 'Google' in item.text or 'E-mail' in item.text or 'Facebook' in item.text:
            verified_channels.append(str(item.text.strip()))
    user_info.append(verified_channels)
  
    
# USER LAST SEEN W/ TIMESTAMP

    seen=[]    
    for link in relevant_section.find_all("span"):
        if 'title' in link.attrs: 
            s =link.attrs['title']
            seen.append(s)
        
    s= relevant_section.find("span", attrs={"title": seen})
    seen.append(s.get_text())
    user_info.append(seen)
    

# User Listing Details

    if len(listing_num.get_text())<1:
        user_info.append("User has no active listings")
        list_of_article_info = "User has no active listings"
    else:
        
        prev_article_count = 0
        while True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)
        
            userHTML = BeautifulSoup(driver.page_source, 'html.parser')
        
            articles = userHTML.find('div', class_='body-content') \
                .find('div', class_='profile__items-wrapper') \
                .find('div', class_='u-ui-margin-horizontal-regular@portables') \
                .find('div', class_='feed-grid') \
                .find_all('div', attrs={'data-testid': 'grid-item'})
        
            current_article_count = len(articles)
            if current_article_count == prev_article_count:
                break
        
            prev_article_count = current_article_count
        
        list_of_article_info = []
        for article in articles:
            article_info = article.find('div', class_='web_ui__Cell__cell web_ui__Cell__narrow')
            if article_info:
                list_of_article_info.append(article_info.get_text())
        
        #print(list_of_article_info)
    user_info.append(list_of_article_info)

    salt = "welovescrapping"
    hashed_id = generate_hash(salt, user_id)
    hashed_username = generate_hash(salt, str(user_name)) 

   
    user_dict.append({"User ID": hashed_id,
                      "User Name": hashed_username,
                      "User Page": user_page,
                      "Number of Reviews": reviews.get_text(),
                      "Rating": rating,
                      "Location": location.get_text(),
                      "Number of Followers": followers.get_text(),
                      "Number of Following": following.get_text(),
                      "Verified Channels": verified_channels,
                      "Last Seen Info":seen,
                      "Number of Active Listings": lst,
                      "Categories of Listings": categories,
                      "Article Details": list_of_article_info
                      })
    print("User " + str(i) + " scrapped")
    #To-do: Add category that user has found


#Save the list just in case

from datetime import date
import pickle 

today = str(date.today())   
filename="user_dict_toShare_" + today + "WRITE YOUR NAME HERE"  # WRITE YOUR OWN NAME HERE 
with open (filename, "wb") as fi:
    pickle.dump(user_dict, fi)
    

    
#WRITE TO CSV

import csv

myFile = open('vinted_demo_file.csv', 'w')
writer = csv.writer(myFile)
writer.writerow(["User ID", "User Name", "User Page", 
                 "Num of Reviews", "User Rating", "Location", 
                 "Num of Followers", "Num of Following", 
                 "Verified Channels", "Last seen", "Num of Active Listings",
                 "Categories of Listings"])

for dictionary in user_dict:
    writer.writerow(dictionary.values())
myFile.close()
myFile = open('demo_file.csv', 'r')
myFile.close()


#WRITE TO JSON FILE     ####ASK TO HANNES: HOW TO PROPERLY READ JSON FILE (?REMOVE /// AND TURN IT TO LIST FORMAT)
#Encode set into JSON using jsonpickle
sampleJson = jsonpickle.encode(user_dict)

with open('vintedSample.json', 'w', encoding='utf-8') as f:
    json.dump(sampleJson, f, ensure_ascii=False, indent=4)


#Read JSON File
time.sleep(3)
with open('vintedSample.json') as user_file:
  json_file = user_file.read()

decodedSet = jsonpickle.decode(json_file)
#print(decodedSet)

