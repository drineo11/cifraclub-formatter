import requests
from bs4 import BeautifulSoup

url = "https://www.cifraclub.com.br/julliany-souza/quem-e-esse/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
pre = soup.find('pre')

with open('dumped_cifra.html', 'w', encoding='utf-8') as f:
    if pre:
        f.write(str(pre))
    else:
        f.write("No pre tag found")
