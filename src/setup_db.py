from db.database import Session, Base, engine
from sqlalchemy import inspect
from db.models import Option
import pandas as pd

def load_data():
    """
    Load data from csv file.
    """
    raw_data = pd.read_csv('../upload/data.csv')
    
    session = Session()
    for row in raw_data.to_dict(orient='records'):
        new_option = Option(commodity_name=row['commodity_name'], 
                            expiry_date=row['expiry_date'], 
                            strike_price=row['strike_price'], 
                            option_type=row['option_type'], 
                            measurement=row['measurement'])
        session.add(new_option)

    session.commit()

def setup_db():
    """
    Create database. 
    If no such database exists, then create and load data from upload folder. 
    Otherwise remind user the database has been created already.
    """
    session = Session()

    if not inspect(engine).has_table("options"):
        Base.metadata.create_all(engine)
        session.commit()
        load_data()
        print("The database has been created successfully.")
    else:
        print("The database has been created already.")

    
if __name__ == "__main__":
    setup_db()