#Aiyana Chopra
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest



def get_titles_from_search_results(filename):
    
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    tup_list = []
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        books = soup.find_all('tr', {'itemtype':'http://schema.org/Book'})
        for book in books:
            bookTitle = getattr(book.find('a', {'class':'bookTitle'}), 'text')
            authorName = getattr(book.find('a', {'class':'authorName'}), 'text')
            tup = (bookTitle.strip(), authorName.strip())
            tup_list.append(tup)
    
    f.close()
    return tup_list

def get_search_links():

    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    search_links = []
    r = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.find_all('tr', {'itemtype':'http://schema.org/Book'}) #get the TR element which contains info for each book
    i = 0
    while i < 10:
        book = books[i] #go thru the top 10 books
        a = book.find('a', href=True)
        url = 'https://www.goodreads.com' + a['href']
        search_links.append(url)
        i += 1

    # print(search_links)
    return search_links



def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    pages = soup.find('span', {'itemprop':'numberOfPages'}).text
    pages = pages.split(' ')[0].strip()
    
    title = soup.find('h1', {'class':'gr-h1 gr-h1--serif'}) #finds the title
    title = title.text.strip() 
    
    all_names = ''
    authors = soup.find_all('a', {'class':'authorName'}) #gets all the authors
    for auth in authors:
        name = auth.find('span', {'itemprop':'name'}) #gets the span compotent of each author which has the name
        name = name.text.strip()
        all_names = all_names + ', ' + name 
    
    tupl = (title, all_names[2:], int(pages))
    return tupl

    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    summary = []
    with open(filepath, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        books = soup.find_all('div', {'class':'category clearFix'})
        for b in books: 
            cat = b.find('h4', {'class':'category__copy'}).text.strip()
            title = b.find('img', {'class':'category__winnerImage'})
            title = title['alt'].strip()
            url = b.find('a', href=True)
            url = url['href'].strip()
            tup = (cat, title, url)
            summary.append(tup)
    
    f.close()
    return summary


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["Book title", "Author name"])
        writer.writerows(data)
    fp.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """

    with open(filepath, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    d = soup.find_all('div', {'id':"descriptionContainer"})
    for elem in d: 
        desc = elem.find_all('span')[1].text.strip()
        break

    reg = "[A-Z][a-z]+. [A-Z][a-z]+"
    
    return re.findall(reg, desc)
    

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        local_var = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(local_var), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(local_var),list)

        # check that each item in the list is a tuple
        for i in local_var:
            self.assertEqual(type(i),tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(local_var[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(local_var[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))

    def test_get_search_links(self):
        
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls),list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls),10)


        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertEqual(type(url),str)
            
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            is_in = "https://www.goodreads.com/book/show/" in url
            self.assertEqual(is_in, True)
    

        

    def test_get_book_summary(self):
    
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        for i in TestCases.search_urls:
            summaries.append(get_book_summary(i))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in summaries:

            # check that each item in the list is a tuple
            self.assertEqual(type(url),tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(url),3)

            # check that the first two elements in the tuple are string
            self.assertEqual(type(url[0]),str)
            self.assertEqual(type(url[1]),str)

            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(url[2]),int)

            # check that the first book in the search has 337 pages 
            
        self.assertEqual(summaries[0][2],337)
        


    def test_summarize_best_books(self):
        
        # call summarize_best_books and save it to a variable
        var = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(var), 20)


        # assert each item in the list of best books is a tuple
        for item in var:
            self.assertEqual(type(item), tuple)
            self.assertEqual(len(item),3)
        
        self.assertEqual(var[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        self.assertEqual(var[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

        # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        


    def test_write_csv(self):
        
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results("search_results.htm")

        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles, "test.csv")

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', mode='r') as f:
            csv_lines = csv.reader(f)
            row_count = 0
            last_row = []
            for row in csv_lines:
                if row_count == 0:
                    # check that the header row is correct
                    self.assertEqual(row, ["Book title", "Author name"])
                    
                if row_count == 1: 
                    # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
                    self.assertEqual(row, ["Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"])

                row_count+= 1
                last_row = row
                
        # check that there are 21 lines in the csv
            self.assertEqual(row_count,21)

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
            self.assertEqual(last_row, ["Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"])
        



if __name__ == '__main__':
    get_titles_from_search_results("search_results.htm")
    get_search_links()
 

    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



