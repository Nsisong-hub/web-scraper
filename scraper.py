
import requests
from bs4 import BeautifulSoup
import mysql.connector
import boto3
import os

def scrape_website():
    url = "https://example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all('h1')
    return [title.get_text() for title in titles]

def store_data_in_rds(titles):
    try:
        db = mysql.connector.connect(
            host="terraform-20241122121318538300000008.cnyma4w68457.us-east-1.rds.amazonaws.com",
            port=3306,
            user="admin",
            password="SecurePassword123!",
            database="scraperdb"
        )
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Titles (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))")
        for title in titles:
            cursor.execute("INSERT INTO Titles (title) VALUES (%s)", (title,))
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def store_data_in_s3(titles):
    try:
        s3 = boto3.client('s3')
        bucket_name = 'web-scraper-data-bucket'
        
        # Use a writable directory if /tmp causes issues
        file_path = "/home/ec2-user/titles.txt"
        
        with open(file_path, "w") as f:
            for title in titles:
                f.write(f"{title}\n")
        
        s3.upload_file(file_path, bucket_name, "scraped_titles.txt")
    except Exception as e:
        print(f"Error storing data in S3: {e}")

if __name__ == "__main__":
    titles = scrape_website()
    store_data_in_rds(titles)
    store_data_in_s3(titles)
