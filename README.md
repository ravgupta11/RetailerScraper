# Tesco_Amazon_Scraper

This project is concerned with automated retrieval of product information from retailer sites like amazon.com, tesco.com, asda.com, etc. The data retrieved can be used to train many machine learning algorithms like pricing approximation, image recognition etc. This project follows an object oriented approach in Python which gives it a bit generic functionality. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.x Interpreter (https://www.python.org/downloads/)
Scrapy Package library (https://pypi.org/project/Scrapy/)
Pillow Package library https://pypi.org/project/Pillow/2.2.1/)
Unittest Package library (Python standard library)
os Package library (Python standard library)
interface-python Package Library (https://pypi.org/project/python-interface/)
enum Package library (Python standard library)
```

### Installing

This guide will be limited to installing the project on PyCharm by JetBrains

* Clone the master directory Tesco_Amazon_Scraper.
* Open he directory as a project in PyCharm (Right click on folder and click on Open as project in PyCharm)
* Click on Files > Settings > Project: Tesco_Amazon_Scraper > Project Interpreter  
* Click on + button on right side of the dialog box.
* Search for all the pre-requisites libraries and install them using button Install Package 

### Deployment of an example of scraping amazon

This guide will show an example on running the project to scrape Amazon

* Open the master directory in terminal or command prompt.
* Run one of the command deending upon the output format required (CSV or JSON format)
```
scrapy crawl RetailerSpider -a output=json -a site=amazon -s LOG_ENABLED=False
or
scrapy crawl RetailerSpider -a output=csv -a site=amazon -s LOG_ENABLED=False
```
* Its recommended to have ```-s LOG_ENABLED=False``` as it significantly speeds up scraping process.
* Generally we don't want to scrape the whole amazon database so its recommended to add ```-s DEPTH_LIMIT=1``` or ```-s DEPTH_LIMIT=2 ``` etc depending upon how many products you require. More the products more are the chances of the ip being blocked by amazon.

* Use Ctrl + c keyboard shortcut to have a graceful shut-down of the process (It will take some time to closs all the files after using the shortcut).

This will create a directory of Files in the master directory. Replace ```-a site=tesco``` for scraping tesco.com.

### Deployment of Unit Testing on a specific product page
  
For running a unit test on a specific product page example.

* Download the html file and and place it in same directory as in ```test.py``` as ```html_sample4.html```
* Define your own unit test or re-configuire the already written ones.
* Open ```test.py``` and change the actual parameters of fake_response_from_file function with your own file name and url.
* Open test.py directory in Terminal/command prompt and type python -m unittest

## Modifying the project to scrape a new retailer domain

The new retailer site must not be build with JavaScript. Files ```RetailerDetails.py```, ```constants.py```, ```RetailerSpider.py``` needs to be modified for using the scraper.

* In ```constants.py``` redefine enums for the new retailer domain.
* Each new enums must have a new constant of ```[SITE_NAME]``` and constant value for the specific site (Domain URL, Xpath Queries and Product page regex are used as constant's values).
* In ```RetailerDetails.py``` define a class ```[SITE_NAME]Details``` extending interface ```Details```(replace [SITE_NAME] with name of the retailer).
* Define all functions of the ```Details``` interface in the new class.
* Use the function ```applyrespone(response_object, xpath_query_expression)``` in ```utilities.py``` returns a object that contains data of your xpath query.
* In ```RetailerSpider.py``` ammend ```makeObject(spider)``` function to check for equality of ```spider.site == [SITE_NAME] ``` and return an object of ```[SITE_NAME]Details``` class after importing it from ```RetailerDetails```.
* Run the command for running the ```RetailerSpider.py``` spider but with ```-a site=[SITE_NAME] ``` argument.

## Buit with

Scrapy API A web framework for Information retrieval.
