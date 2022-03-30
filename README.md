<h1 align="center">
  Book Finder
</h1>

<p align="center">
 Book finder aims to help user to find desired books in Amazon store more quickly bases on the book review data. 
</p>

<div align="center">
  <img src="https://github.com/danielzheng-work/Book-Finder/blob/main/img/demo.png" width="100%" />
</div>


## About
Book Finder uses a Java based GUI to display information, while processing the input and output in Python.

![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=java&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Eclipse](https://img.shields.io/badge/Eclipse-FE7A16.svg?style=for-the-badge&logo=Eclipse&logoColor=white)

### Required python libraries:
  - pandas 
  - pickle
  - bs4 (beautifulsoup)
  - mechanize 
  - wordcloud
  - numpy 
  - nltk 
  - lxml

### How To Run 

Import the project folder into Eclipse IDE and run `index.java` within `src\frame` folder.

### Usage 

**ASIN Cloud**: Enter the ASIN value (eg. 0001050230) of a book you want and a word cloud will be displayed showcasing the most frequent words <br/>
**Keyword Freq**: Enter a keyword (eg. great) and a list of ASINS containing that word the most will be shown <br/>
**ASIN Convert**: Enter an ASIN value (eg. 0001050230) and the converted book name will be shown <br/>
**ASIN Relations**: Enter an ASIN value (eg. 0001050230) and a list of books with the most similar keywords will be shown <br/>

### Dataset 
Book Finder sources its information from (https://nijianmo.github.io/amazon/index.html), using the dataset labeled [Books](http://deepyeti.ucsd.edu/jianmo/amazon/categoryFilesSmall/Books_5.json.gz). There is data available in the pickles folder that was loaded, filtered and compressed to avoid having to download gigabytes worth of data.


