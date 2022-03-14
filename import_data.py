"""File import data from csv files into Azure CosmosDB."""

import os
import json
import pandas as pd
from typing import List, Tuple
from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos.database import DatabaseProxy

# Store the secrets from Azure Cosmos DB
# The secrets are environements variable that can be loaded in a .env file
# Read more here: https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
db_config = {
    "url": os.environ["DB_URL"],
    "primary_key": os.environ["DB_SECRET"],
    "database_name": os.environ["DB_NAME"]
}

def create_cosmos_container(db_proxy_client: DatabaseProxy, partition_key: str, container_name: str) -> None:
    """
    Create a Cosmos 'Container' if it doesn't exist yet. 
    A container is a table of records.

    :param client: The Comsmos client to connect the DB.
    :param database_name: The DB you want to connect to.
    :param partition_key: A key that act as a Primary Key. Read more here: https://www.c-sharpcorner.com/article/partitioning-in-cosmos-db/
    """
    # Object needed to create container (table)
    container = db_proxy_client.create_container_if_not_exists(
        id=container_name,
        partition_key={
            "paths": [f"/{partition_key}"],
            "kind": "Hash"
        },
        offer_throughput=400,
    )
    print(container)
    print("Container Created!")

def get_csv_file_paths(path: str) -> List[str]:
    """
    Get all the .csv files in a given path.

    :Param path: The folder where the .csv are located.
    :return: A list of csv paths.
    """
    files_path = []
    # Loop over each file located in {path}
    for _, _, files in os.walk(path):
        for file_name in files:
            # Create the file path
            file_path = os.path.join("./data", file_name)
            files_path.append(file_path)
    return files_path

def csv_to_dataframe(csv_path: str) -> Tuple[pd.DataFrame, str]:
    """
    Convert a CSV file to dataframe format.
    Used to get the required format for CosmosDB.

    :Param csv_path: The path were the .csv file is located.
    :Return: A tuple with (dataframe, the file name) 
    """
    # Get the file name (with file extension) from path
    file_name = os.path.basename(csv_path)
    # Remove file extension
    file_name = os.path.splitext(file_name)[0]
    # Create the dataframe from csv file.
    df = pd.read_csv(csv_path)
    # Rename id column if exist to avoid conflic with Cosmos ID
    df = df.rename(columns={'id': 'data_id'})
    # Reset index - creates a column called 'index'
    df = df.reset_index()
    # Rename that new column 'id' (Cosmos DB needs one column named 'id'. )
    df = df.rename(columns={'index':'id'})
    # Convert the id column to a string - this is a document database.
    df['id'] = df['id'].astype(str)
    
    return df, file_name

def write_dataframe_on_cosmosdb(db_proxy_client: DatabaseProxy, dataframe: pd.DataFrame, container_name: str) -> None:
    """
    Write each row of a dataframe in the DB.

    :Param db_proxy_client: Client required to connect the database.
    :Param dataframe: The dataframe to insert in the DB.
    :Param container_name: The name of the container (table) we want to insert data in.
    """
    # Create the container proxy client (will allow us to write to table)
    container_proxy_client = db_proxy_client.get_container_client(container_name)
    dataframe_row_len = dataframe.shape[0]
    for i in range(0, dataframe_row_len):
        # create a dictionary for the selected row
        row_json = dataframe.iloc[i,:].to_json()        
        # Write row in DB
        container_proxy_client.upsert_item(
            json.loads(row_json)
        )
        print(f'Record {i}/{dataframe_row_len} inserted successfully.')



if __name__ == "__main__":
    # Initialise connection with the cosmos client
    client = CosmosClient(
        url=db_config["url"], 
        credential=db_config["secret"]
    )
    
    # Get the list of csv paths
    csv_paths = get_csv_file_paths("./data")
    
    # Loop over the csv files
    for i, file_path in enumerate(csv_paths):
        print(f"----------- Starting file {i}/{len(csv_paths)} -----------")
        
        # Convert csv to dataframe
        df, table_name = csv_to_dataframe(file_path)
        # Take the first comumn as partition key
        partition_key = df.columns[0]
        # Create a database proxy client (needed to write in DB)
        db_proxy_client = client.get_database_client(db_config["database_name"])
        # Create Cosmos Container if it doesn't exist yet
        create_cosmos_container(db_proxy_client, partition_key, table_name)
        # Write all the rows on cosmos
        write_dataframe_on_cosmosdb(db_proxy_client, df, table_name)
        
        print(f"----------- DONE -----------")
