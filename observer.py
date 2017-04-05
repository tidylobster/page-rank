import numpy as np
import urllib.parse as parse
import requests, re, time, pickle
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from page_rank.compress import SparseMatrix

main_link = "https://medium.com/"
searched_netloc = re.compile(r"medium\.com")


def collect(link, amount=100):
    i = 0
    queue = [link]
    links = set()
    links.add(link)
    while amount > len(links) != i:
        array = reformat(scan(queue[i]))
        queue.extend(array)
        links.update(array)
        print(len(links))
        i += 1
    return list(links)[:amount]


def scan(link):
    """
    Scans one page for all links
    """
    try:
        r = requests.get(link)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.find_all("a")
    except ConnectionError as e:
        print("Connection error occurred while trying to reach the page")
        print(e)
    return []


def reformat(array):
    """
    Reformat all collected links from array to normal form
    """
    global searched_domain
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
        print(i, array[i])
        links = reformat(scan(array[i]))
        for j in range(len(array)):
            if array[j] in links:
                matrix[i][j] = 1


if __name__ == "__main__":
    st_time = time.time()

    links = collect(main_link, 100)
    matrix = np.zeros((len(links), len(links)))
    refill(links, matrix)

    np.savetxt('data\\matrix.csv', matrix, delimiter=',')
    smatrix = SparseMatrix(matrix)

    with open('data\\matrix.txt', 'wb') as fp:
        pickle.dump(smatrix, fp)
    with open('data\\legend.txt', 'wb') as fp:
        pickle.dump(links, fp)

    print("--- %s seconds ---\n" % (time.time() - st_time))
    print(links)
    print(smatrix)
