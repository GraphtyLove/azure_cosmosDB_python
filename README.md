# Azure CosmosDB

In this repo, you will find code to interact in python with [Azure CosmosDB](https://azure.microsoft.com/fr-fr/free/cosmos-db).

## Why?
It has been created for the purpose of a Use-Case project in a BeCode AI class. (Bouman4)

## Provide read access to learners
To provide a read-only access to the learners you can give them the credentials that are stored in:

`Azure` -> `CosmosDB` -> `<Your Cosmos instance>` -> `Keys` -> `Read-Only Keys`.

The `PRIMARY READ-ONLY CONNECTION STRING` should be enough, but you can also provide the `URI` and the `PRIMARY READ-ONLY KEY`.

## Installation
In order for the project to run, you need to:

Install `python 3.9.2`

Install the requirements with:

```bash
pip install -r requirements.txt
```

Then you need to create a `.env` file at the root of the project and add the following keys:

```.bash
DB_NAME=<YOUR DB NAME> # You need to create this one in: `Azure` -> `CosmosDB` -> <your Cosmos Instance> -> `Create`
DB_URL=<YOUR DATABSE URL> # See Azure portal: `Azure` -> `CosmosDB` -> <your Cosmos Instance> -> `Keys` -> `URI`
DB_SECRET=<YOUR PRIMARY KEY> # See Azure portal: `Azure` -> `CosmosDB` -> <your Cosmos Instance> -> `Keys`-> `PRIMARY KEY`
```

## Files

### Data
The data are divided in 6 `.csv` files:
- [ODL_ALLERGY.csv](./data/ODL_ALLERGY.csv)
- [ODL_ALLERGY_CUSTOMER.csv](./data/ODL_ALLERGY_CUSTOMER.csv)
- [ODL_ORDER.csv](./data/ODL_ORDER.csv)
- [ODL_ORDER_ITEM.csv](./data/ODL_ORDER_ITEM.csv)
- [ODL_ORDERABLES.csv](./data/ODL_ORDERABLES.csv)
- [ODL_RESTAURANT.csv](./data/ODL_RESTAURANT.csv)

### Import data
In [import_data.py](./import_data.py) you will find the code used to import the data (.csv format) in CosmosDB.

### Read Database
In [read_database.py](./read_database.py) you will find the code used to read a table from the databse in CosmosDB.

## Resources
To write this code I used some resources:
- This [article](https://towardsdatascience.com/python-azure-cosmos-db-f212c9a8a0e6) but it seams outdated. I used to for the global logic but the code wasn't working with the latest Azure-Cosmos python SDK. I had to look into the Microsoft documentation to correct it.
- The [Azure-Cosmos official documentation](https://docs.microsoft.com/en-us/python/api/overview/azure/cosmosdb?view=azure-python). Which is really great!

## Who?
Written by *Maxim Berge* the *14/03/2022*.