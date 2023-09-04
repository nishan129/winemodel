import sys
from typing import Optional

import numpy as np
import pandas as pd

from src.configuration.mongo_db_connection import MongoDBClient
from src.constant.database import DATABASE_NAME
from src.exception import ModelException
from src.logger import logging

class WineData:
    """
    This class help to export entire mongodb record as pandas dataframe
    """
    
    def __init__(self):
        """
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            
        except Exception as e:
            raise ModelException(e,sys)
        
    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        
        try:
            """
            export entire collection as dataframe:
            return pandas.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
                
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                
            return df
        except Exception as e:
            raise ModelException(e,sys)
