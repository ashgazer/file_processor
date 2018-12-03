# Product Feed

The following project uses ProductFeed class as to download and merge three different
streams of the product feed. The ProductFeed it self inherits from the base clase UtilTools.
A Generic Class that can download CSV, XML or Json in gz or zip formats.
 

## Getting Started

### Prerequisites

The following python libraries are required.

* Requests
* Pytest

```
pip install requirements.pip

```

## Product Feed


Instantiate the object using the ProductsFeeds() object. Then use the run method to start
the process to create the product feed 

```
data = ProductFeeds()
data.run()
```

## Running the tests
You are able to run tests using the command below.

```
pytest -v test_main

```

## Built With
Python 3 


## Authors

* **Ashik Pirmohamed** 



