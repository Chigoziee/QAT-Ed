import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DynamoDBTable:
    def __init__(self, table_name: str):
        # Initialize a boto3 DynamoDB client
        self.dynamodb = boto3.client("dynamodb")
        self.table = table_name

    # ---------- Write ----------
    def write(self, item: dict) -> None:
        """
        Write a new item to the DynamoDB table.

        Parameters:
        item (dict): The item to insert into the table. Keys and values must follow DynamoDB format.
        """
        self.dynamodb.put_item(TableName=self.table, Item=item)

    # ---------- Read ----------
    def read(self, key: dict) -> dict | None:
        """
        Read an item from the DynamoDB table using its primary key.

        Parameters:
        key (dict): The primary key of the item to retrieve, formatted as expected by DynamoDB.

        Returns:
        dict | None: The item if found, else None.
        """
        try:
            response = self.dynamodb.get_item(TableName=self.table, Key=key)
        except ClientError as exc:
            raise RuntimeError(f"DynamoDB get_item failed: {exc}") from exc

        return response.get("Item")
