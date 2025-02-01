from bs4 import BeautifulSoup

with open('home.htm', 'r') as html_file:
    content = html_file.read()
    # print(content)

soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())
tags = soup.find('h5')
print(tags)