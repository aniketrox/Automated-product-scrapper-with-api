import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import pandas as pd
import os
def download_image(image_url, save_folder, file_name):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    file_path = os.path.join(save_folder, file_name)
    
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)


def extract_numbers_from_url(url):
    pattern = r'\d+$'
    match = re.search(pattern, url)
    if match:
        numbers = match.group()
        return str(numbers)
    else:
        return None

val=0

main_url = 'https://themeforest.net/category'
reqs = requests.get(main_url)
soup = BeautifulSoup(reqs.text, 'html.parser')
main_div = soup.find('ul', class_ = "first")

urls = []
for link in main_div.find_all('a'):
    urls.append("https://themeforest.net/"+link.get('href')+"?sort=sales")
    
csv_file = 'themeforest.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Link'])
    for link in urls:
        writer.writerow([link])
p_list = []    
for url_i in urls:
    ureqs = requests.get(url_i)
    usoup = BeautifulSoup(ureqs.text, 'html.parser')
    url_div = usoup.find('div', id = "content")
    product_urls = []
    for link in url_div.find_all('a',class_="shared-item_cards-item_name_component__itemNameLink"):
        product_urls.append(link.get('href'))
    pcount = 0
    for purl_i in product_urls:
        
        pid = extract_numbers_from_url(purl_i)
        reqs = requests.get(purl_i)
        psoup = BeautifulSoup(reqs.text, 'html.parser')

        pname_raw = psoup.find('h1', class_ = "t-heading -color-inherit -size-l h-m0 is-hidden-phone")
        if pname_raw == None:
            pname = 0
        else:
            pname=pname_raw.get_text()
        
        img_box_raw = psoup.find("div",class_="content-s js-adi-data-wrapper")
        if img_box_raw == None:
            fimg = 0
        else:
            # img_box = img_box_raw.get_text()
            # print(img_box)
            for link in img_box_raw.find_all('img'):
                fimg=link.get("src")
                n = str(datetime.now())+"jpg"
                download_image(fimg, "img", n)
                fimg_path = "img/n"
            
        product_url = purl_i
        
        author_div = psoup.find("div",class_="item-header__author-details")
        author_raw = author_div.find("a")
        if author_raw == None:
            author = 0
        else:
            author = author_raw.get_text()
        # print(author_div.find("a"))
        author_link_raw = author_div.find("a")
        if author_link_raw == None:
            author_link = 0
            author_port = 0
            author_review = 0
        else:
            author_link = "https://themeforest.net"+author_link_raw.get("href")
            author_port = author_link+"/portfolio"
            author_reqs = requests.get(author_link)
            author_soup = BeautifulSoup(author_reqs.text, 'html.parser')
            author_review_raw = psoup.find("span",class_="item-navigation-reviews-comments")
            if author_review_raw == None:
                author_review = 0
            else:
                author_review = author_review_raw.get_text()
        
        type_author_raw = author_soup.find("span",class_="user-info-header__author-level")
        if type_author_raw == None:
            type_author = 0
        else:
            type_author = type_author_raw.get_text()
        
        sales_count_info = psoup.find("div", class_="item-header__sales-count")
        sales_count_raw = sales_count_info.find("strong")
        if sales_count_raw == None:
            sales_count = 0
        else:
            sales_count = sales_count_raw.get_text()
        
        sales_price_raw = psoup.find("div",class_="js-purchase-heading purchase-form__price t-heading -size-xxl")
        if sales_price_raw == None:
            sales_price = 0
        else:
            sales_price = sales_price_raw.find("span").get_text()
        
        last_update_raw = psoup.find("tbody").find("tr",class_="js-condense-item-page-info-panel--last_update").find("time",class_="updated")
        if last_update_raw == None:
            last_update = 0
        else:
            last_update = last_update_raw.get_text()
        
        tags_raw = psoup.find("tbody").find("span",class_="meta-attributes__attr-tags")
        if tags_raw == None:
            tags = 0
        else:
            tags = tags_raw.get_text()

        avg_rat = psoup.find("tbody").find("span",class_="rating-detailed-small__stars")
        if avg_rat == None:
            average_ratings = 0
        else:
            average_ratings = avg_rat.get_text()

        rec_update = psoup.find("tbody").find("strong",class_="item-header__envato-highlighted")
        if rec_update == None:
            recent_update = "No"
        else:
            recent_update = "Yes"
        
        no_sales = psoup.find("tbody").find("strong",class_="item-header__sales-count")
        if no_sales == None:
            number_sales = 0
        else:
            number_sales = no_sales.get_text()


        live_preview_raw = psoup.find("div", class_="item-preview__preview-buttons")
        if live_preview_raw:
            live_preview_url = live_preview_raw.find('a', class_='live-preview').get('href')
        else:
            live_preview_url = None

        price_raw = psoup.find("div", class_="js-purchase-heading purchase-form__price t-heading -size-xxl")
        if price_raw:
            price = price_raw.find('span', class_='js-purchase-price').get_text()
        else:
            price = None

        sales_price_raw = psoup.find("span", class_="js-renewal__price")
        if sales_price_raw:
            sales_price = sales_price_raw.get_text()
        else:
            sales_price = None

        last_update_raw = psoup.find("tr", class_="js-condense-item-page-info-panel--last_update")
        if last_update_raw:
            last_update = last_update_raw.find("time").get_text()
        else:
            last_update = None

        published_date_raw = psoup.find("tr", text=re.compile('Published'))
        if published_date_raw:
            published_date = published_date_raw.find("span").get_text()
        else:
            published_date = None


        gutenberg_optimized_raw = psoup.find("tr", text=re.compile('Gutenberg Optimized'))
        if gutenberg_optimized_raw:
            gutenberg_optimized = gutenberg_optimized_raw.find("a").get_text()
        else:
            gutenberg_optimized = None

        high_resolution_raw = psoup.find("tr", text=re.compile('High Resolution'))
        if high_resolution_raw:
            high_resolution = high_resolution_raw.find("span").get_text()
        else:
            high_resolution = None

        widget_ready_raw = psoup.find("tr", text=re.compile('Widget Ready'))
        widget_ready = widget_ready_raw.find("a").get_text() if widget_ready_raw else None

        compatible_browsers_raw = psoup.find("tr", text=re.compile('Compatible Browsers'))
        if compatible_browsers_raw:
            compatible_browsers = [a.get_text() for a in compatible_browsers_raw.find_all("a")]
        else:
            compatible_browsers = None

        compatible_with_raw = psoup.find("tr", text=re.compile('Compatible With'))
        if compatible_with_raw:
            compatible_with = [a.get_text() for a in compatible_with_raw.find_all("a")]
        else:
            compatible_with = None

        software_version_raw = psoup.find("tr", text=re.compile('Software Version'))
        if software_version_raw:
            software_version = [a.get_text() for a in software_version_raw.find_all("a")]
        else:
            software_version = None
        themeforest_files_included_raw = psoup.find("tr", text=re.compile('ThemeForest Files Included'))
        if themeforest_files_included_raw:
            themeforest_files_included = [a.get_text() for a in themeforest_files_included_raw.find_all("a")]
        else:
            themeforest_files_included = None

        columns_raw = psoup.find("tr", text=re.compile('Columns'))
        columns = columns_raw.find("span").get_text() if columns_raw else None

        documentation_raw = psoup.find("tr", text=re.compile('Documentation'))
        documentation = documentation_raw.find("a").get_text() if documentation_raw else None

        layout_raw = psoup.find("tr", text=re.compile('Layout'))
        layout = layout_raw.find("span").get_text() if layout_raw else None



        tags_raw = psoup.find("tr", text=re.compile('Tags'))
        if tags_raw:
            tags = [a.get_text() for a in tags_raw.find_all("a")]
        else:
            tags = None

        video_preview_resolution_raw = psoup.find("tr", text=re.compile('Resolution'))
        video_preview_resolution = video_preview_resolution_raw.find("a").get_text() if video_preview_resolution_raw else None

        files_included_raw = psoup.find("tr", text=re.compile('ThemeForest Files Included'))
        if files_included_raw:
            files_included = [a.get_text() for a in files_included_raw.find_all("a")]
        else:
            files_included = None

        files_included_raw = psoup.find("tr", text=re.compile('ThemeForest Files Included'))
        if files_included_raw:
            files_included = [a.get_text() for a in files_included_raw.find_all("a")]
        else:
            files_included = None

        well_doc = psoup.find("tbody").find("strong",class_="item-header__envato-highlighted")
        if well_doc == None:
            well_document = "NO"
        else:
            well_document = "Yes"






            
        n_l = [
            pid, pname, fimg, product_url, author, author_link, author_port, author_review, 
            type_author, sales_count, sales_price, last_update, tags, average_ratings, 
            recent_update, number_sales, live_preview_url, price, sales_price, last_update, 
            published_date, gutenberg_optimized, high_resolution, 
            widget_ready, compatible_browsers, compatible_with, software_version, 
            themeforest_files_included, columns, documentation, layout, tags, 
            video_preview_resolution, files_included, well_document
        ]
        # print(n_l)
        p_list.append(n_l)
        print("============"+str(val+1)+"<->"+str(pcount)+"============")
        pcount=pcount+1
        #break
    
    # if val == 5:
    #     break
    
    val = val+1
    
        
        
csv_file = 'normal.csv'
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    for i in p_list:
        writer.writerow(i)
        
        

current_datetime = [datetime.now()]
df = pd.read_csv("date.csv")
l = len(df)

date_file = 'date.csv'
with open(date_file, 'a', newline='') as file:
    dwriter = csv.writer(file)
    for link in current_datetime:
        dwriter.writerow(["scrap-"+str(l+1),link])