"""File Read database table's content from Azure CosmosDB"""

import os
from typing import List, Dict
from dotenv import load_dotenv
from azure.cosmos.cosmos_client import CosmosClient


# Store the secrets from Azure Cosmos DB
# The secrets are environements variable that can be loaded in a .env file
# Read more here: https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
load_dotenv("./.env")


class DatabaseReader:
    def __init__(self, db_url: str, db_secret: str, db_name: str):
        self.database_name = db_name
        # Create the Cosmos client that establich the connection to Cosmos
        self.client: CosmosClient = CosmosClient(url=db_url, credential=db_secret)
        # Establish the connection with your database 
        self.database = self.client.get_database_client(db_name)


    def get_database_list(self) -> List[Dict[str, str]]:
        """
        Get the list of the existing DBs.
        
        :param client: A client object that establish the connection with the Cosmos.
        :return: A list of dicts. Each containing DB name, columns,...
        """
        # Get the list of the existing DBs. 
        # Return an iterator so convert it as list.
        dbs = list(self.client.list_databases())
        print("Your DBs: ", dbs)
        return dbs
    
    def query_table(self, table: str, query: str) -> List[str]:
        """
        Perform a SQL over a table.

        :Param table: The table you want to query. (Called 'container' in CosmosDB)
        :Param query: The SQL query you want to run. Ex: 'SELECT * FROM users'
        """
        # Establish the connexion to the table you want to query.
        container = self.database.get_container_client(table)
        # Execute query
        results = container.query_items(query, enable_cross_partition_query=True)
        # Convert the iterator as list.
        return list(results)

    def upsert_item(self, table: str, item: Dict[str, str]) -> None:
        """
        Insert or update the specified item.
        If the item already exists in the container, it is replaced. If the item does not already exist, it is inserted.
        
        :Param table: The table you want to update/create an item on.
        :Param item: A dict containing the item's values.
        """
        # Establish the connexion to the table you want to query.
        container = self.database.get_container_client(table)
        # Execute query
        container.upsert_item(item)
        print("Item Updated!")


if __name__ == "__main__":
    client = DatabaseReader(
        db_url=os.getenv("DB_URL"),
        db_secret=os.getenv("DB_SECRET"),
        db_name=os.getenv("DB_NAME")
    )
    # Get all the data from the table ODL_ALLERGY_CUSTOMER
    rows = client.query_table("ODL_ALLERGY_CUSTOMER", "SELECT * FROM ODL_ALLERGY_CUSTOMER")
    # Print the number or rows returned.
    print(len(rows))

