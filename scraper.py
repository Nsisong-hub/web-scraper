import requests
from bs4 import BeautifulSoup
import mysql.connector
import boto3

def scrape_website():
    url = "https://example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all('h1')
    return [title.get_text() for title in titles]

def store_data_in_rds(titles):
    db = mysql.connector.connect(
        host="terraform-20241121110455983200000007.cnyma4w68457.us-east-1.rds.amazonaws.com",
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

def store_data_in_s3(titles):
    s3 = boto3.client('s3')
    bucket_name = 'web-scraper-data-bucket'
    with open("/tmp/titles.txt", "w") as f:
        for title in titles:
            f.write(f"{title}\n")
    s3.upload_file("/tmp/titles.txt", bucket_name, "scraped_titles.txt")

if __name__ == "__main__":
    titles = scrape_website()
    store_data_in_rds(titles)
    store_data_in_s3(titles)
