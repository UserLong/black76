from db.database import Session
from db.models import Option

def query_all_optioins():
    """
    return all available options in the table
    """
    session = Session()
    results = session.query(Option).all()
    return results

def query_option_by_id(option_id: int):
    """
    return one option that matches the option id
    """
    session = Session()
    result = session.query(Option).filter(Option.id == option_id).first()
    return result

def query_option_by_name(commodity_name: str):
    """
    return one option that matches the option name
    """
    session = Session()
    result = session.query(Option).filter(Option.commodity_name == commodity_name).first()
    return result

def insert_new_option(new_option: Option):
    """
    insert one option into the table
    """
    session = Session()
    session.add(new_option)
    session.commit()
    print("New option added.")
    return

def delete_option_by_id(option_id: int):
    """
    delete one option that matches the option id
    """
    session = Session()
    session.query(Option).filter(Option.id == option_id).delete()
    session.commit()
    print("Option ", option_id, " deleted.")
    return

def delete_option_by_name(commodity_name: str):
    """
    delete one option that matches the option nae
    """
    session = Session()
    rec_num = session.query(Option).filter(Option.commodity_name == commodity_name).count()
    session.query(Option).filter(Option.commodity_name == commodity_name).delete()
    session.commit()
    print(rec_num, " of option ", commodity_name, " have been deleted.")
    return

def delete_all_options():
    """
    delete all options in the table.
    """
    session = Session()
    session.query(Option).delete()
    session.commit()
    return

