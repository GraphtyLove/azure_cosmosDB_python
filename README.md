# Azure CosmosDB

In this repo, you will find code to interact in python with [Azure CosmosDB](https://azure.microsoft.com/fr-fr/free/cosmos-db).
## Files
### Import data
In [import_data.py](./import_data.py) you will find the code used to import the data (.csv format) in CosmosDB.

### Read Database
In [read_database.py](./read_database.py) you will find the code used to read a table from the databse in CosmosDB.

## Resources
To write this code I used some resources:
- This [article](https://towardsdatascience.com/python-azure-cosmos-db-f212c9a8a0e6) but it seams outdated. I used to for the global logic but the code wasn't working with the latest Azure-Cosmos python SDK. I had to look into the Microsoft documentation to correct it.
- The [Azure-Cosmos official documentation](https://docs.microsoft.com/en-us/python/api/overview/azure/cosmosdb?view=azure-python). Which is really great!