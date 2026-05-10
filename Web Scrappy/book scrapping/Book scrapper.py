import requests
from bs4 import BeautifulSoup

print("...Scraping book data from the website...")

#the url where to get data from

url="https://books.toscrape.com/catalogue/category/books/science_22/index.html"

page=requests.get(url)

#gets the page content and parses it using BeautifulSoup

soup=BeautifulSoup(page.content,'html.parser')


#finds all the elements in the page with the specified tag and class name

soup.find_all('article', class_='product_pod')

#loops through the elements and extracts the title and price of each book

for book in soup.find_all('article', class_='product_pod'):
    title=book.find("h3").find("a")["title"]
    price=book.find("p", class_="price_color").text 
    print(f"Title: {title}, Price: {price}")
    availability=book.find("p", class_="instock availability").text.strip()
    print(f"Availability: {availability}")

try:
  with open("books.txt", "a") as file:
    file.write("...Scraping book data from the website...\n")
    for book in soup.find_all('article', class_='product_pod'):
        title=book.find("h3").find("a")["title"]
        price=book.find("p", class_="price_color").text 
        availability=book.find("p", class_="instock availability").text.strip()
        file.write("\n")
    
        file.write(f"Title: {title}, Price: {price}, Availability: {availability}\n")    
    file.write("\n")  # Add a newline after each scraping session

except AttributeError:
    print("Some information is missing for one or more books.")
except Exception as e:
    print(f"An error occurred: {e}")
