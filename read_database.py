"""File Read database table's content from Azure CosmosDB"""

import os
from typing import List, Dict
from azure.cosmos.cosmos_client import CosmosClient


class DatabaseReader:
    def __init__(self, db_url: str, db_secret: str, db_name: str):
        self.database_name = db_name
        # Create the Cosmos client that establich the connection to Cosmos
        self.client: CosmosClient = CosmosClient(url=db_url, credential=db_secret)

    def get_database_list(self) -> List[Dict[str, str]]:
        """
        Get the list of the existing DBs.
        
        :param client: A client object that establish the connection with the Cosmos.
        :return: A list of dicts. Each containing DB name, columns,...
        """
        # Get the list of the existing DBs. 
        # Return an iterator so convert it as list.
        dbs = list(self.client.list_databases())
        print(dbs)
        return dbs
    
    def print_database_content(self):
        query = f"SELECT * FROM {self.database_name}"
        result = self.client.query_databases(query)
        print(list(result))



if __name__ == "__main__":
    client = DatabaseReader(
        db_url=os.environ["DB_URL"],
        db_secret=os.environ["DB_SECRET"],
        db_name=os.environ["DB_NAME"]
    )
    client.print_database_content()
