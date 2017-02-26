import requests, re, time
from bs4 import BeautifulSoup
import urllib.parse as parse
import numpy as np

main_link = "https://medium.com/"
# main_link = "http://kpfu.ru/"
searched_netloc = re.compile(r"medium\.com")
# searched_netloc = re.compile(r"\b(?!javascript:).*")


def collect(link, amount=100):
    i = 0
    queue = [link]
    links = set()
    links.add(link)
    while amount > len(links) != i:
        array = reformat(scan(queue[i]))
        queue.extend(array)
        links.update(array)
        i += 1
    return list(links)[:amount]


def scan(link):
    """
    Scans one page for all links
    :param link:
    :return:
    """
    r = requests.get(link)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        return soup.find_all("a")
    return []


def reformat(array):
    """
    Reformat all collected links from array to normal form
    :param array:
    :return:
    """
    global searched_netloc
    response = []
    for tag in array:
        link = tag.get("href", None)
        if link is not None:
            p = parse.urlparse(link)
            if re.match(searched_netloc, p.netloc):
                if p.scheme == "":
                    link = parse.ParseResult("http", *p[1:]).geturl()
                response.append(link)
    return response


def refill(array, matrix):
    for i in range(len(array)):
        links = reformat(scan(array[i]))
        amount = 0
        for j in range(len(array)):
            if array[j] in links:
                matrix[i][j] = 1
                amount += 1
        if amount == 0: amount = 1
        matrix[i] = np.divide(matrix[i], amount)
        matrix[i] = np.around(np.divide(matrix[i], amount), 3)

# time measurement
st_time = time.time()

links = collect(main_link, 10)
matrix = np.zeros((len(links), len(links)))
refill(links, matrix)

np.savetxt('matrix.csv', matrix, delimiter=',')

print("--- %s seconds ---" % (time.time() - st_time))
print(links)
print(matrix)


