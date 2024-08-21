# Dimitris Rizopoulos - email: dimrizopoulos@gmail.com

# import Python std libraries
import random
import time
import logging
import sys
import csv
import os

import scrape_for_news as scrapper
import upload_img_to_gcs as upload_img_to_gcs
import msg_sender_twilio_sms as msg_sender_twilio_sms

from hf_model_wrappers import hf_text_to_image
from hf_model_wrappers import hf_keyword_extraction
from hf_model_wrappers import hf_summarize

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def find_unique_random_article(list1, list2):
    titles_list2 = {item['title'] for item in list2}
    unique_elements = [item for item in list1 if item['title'] not in titles_list2]

    if unique_elements:
        return random.choice(unique_elements)
    else:
        return None

def rest_after_action():
    ''' Used to space out API function calls to HuggingFace'''
    sleep_time = random.randint(5, 10)
    time.sleep(sleep_time)
    logging.debug("Woke up from sleep.")

def main():
    # we include here a list of free-to-scrape sources, but ideally real news article could be used
    urls = [
        ('http://quotes.toscrape.com/author/Albert-Einstein/', 'test'),
        ('http://quotes.toscrape.com/author/J-K-Rowling/', 'test'),
        ('http://quotes.toscrape.com/author/Jane-Austen/', 'test'),
        ('http://quotes.toscrape.com/author/Marilyn-Monroe/', 'test'),
        ('http://quotes.toscrape.com/author/Andre-Gide/', 'test'),
        ('http://quotes.toscrape.com/author/Thomas-A-Edison/', 'test'),
        ('http://quotes.toscrape.com/author/Eleanor-Roosevelt/', 'test'),
        ('http://quotes.toscrape.com/author/Elie-Wiesel/', 'test'),
        ('http://quotes.toscrape.com/author/Douglas-Adams/', 'test'),
    ]

    news_articles = scrapper.scrape_news(urls)

    # check for already uploaded articles list, and select unique article
    uploaded_articles = read_csv('io_files/uploaded_articles.csv')
    selected_article = find_unique_random_article(news_articles, uploaded_articles)
    uploaded_articles.append(selected_article)
    write_csv('io_files/uploaded_articles.csv', uploaded_articles)

    # unpack article information
    article_title = selected_article['title']
    article_url = selected_article['url']
    article_text = scrapper.fetch_article_content(article_url)

    # create article summary
    # it is used to produced better images and keywords with HuggingFace,
    # and it can even be passed to the final msg
    summary = hf_summarize.bart_large_cnn(article_title + ". " + article_text)
    rest_after_action()

    # Printing out some info for debugging purposes
    print("Selected_article and url:")
    print(selected_article)
    print(article_url)
    print(summary)

    # after an article is selected, extarct the keywords and create hashtags by adding '#'
    keywords = hf_keyword_extraction.extract_keywords(article_title + ". " + summary)
    if not keywords:  # This is True if the list is empty
        print("The keywords list is empty, exiting the program.")
        sys.exit(1)  # Exiting the program with a status code of 1 to indicate an error
    final_hashtags = ["#" + string for string in keywords]
    print("Hashtags identified: ", keywords)
    rest_after_action()

    # Create image based on article title and description
    hf_text_to_image.sd_xl_base_with_refiner(article_title + ". " + summary)
    rest_after_action()

    source_file_name = 'io_files/non_refined_image.png'
    bucket_name = 'sm_auto_first'
    destination_blob_base_name = 'uploads/story'
    image_url = upload_img_to_gcs.upload_blob(bucket_name, source_file_name,
                                              destination_blob_base_name)

    # Numbers for Twillio (E.164 format assumed)
    from_phone_number = os.getenv('FROM_NUMBER')
    to_phone_number = os.getenv('TO_NUMBER')

    msg_body_txt = article_title + " " + " ".join(final_hashtags)
    msg_sender_twilio_sms.send_sms_message_with_link(from_phone_number, to_phone_number,
                                                     msg_body_txt, article_url, image_url)

if __name__ == "__main__":
    main()
  