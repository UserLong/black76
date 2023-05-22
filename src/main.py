from fastapi import FastAPI, HTTPException
import db_ops
from db.models import OptionBase, Option, CalculatedOption, CalculationExtraInput
from calculate_pv import PVCalculator 
from db.models import CalculationExtraInput
# from sqlalchemy.exc import OperationalError

app = FastAPI()


@app.get("/")
def root():
    """
    Default page that displays introduction information
    """
    return {"message": "This is Black76 model."}


@app.get("/display_options")
def display_all_options():
    """
    Display all options in the database
    """
    result = db_ops.query_all_optioins()
    if result is None:
        raise HTTPException(status_code=404, detail="No option data available")
    return result
    

@app.get("/query_option/{id}")
def query_option(id):
    """
    Query options by id. 
    Return the result if found, otherwise raise 404.
    """
    result = db_ops.query_option_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="No option data available")
    return result


@app.get("/truncate_options")
def delete_all_options():
    """
    Delete all options in the table.
    If database not there, then return 404.
    """
    try:
        db_ops.delete_all_options()
        return {"message": "Table truncated"}
    except:
        raise HTTPException(status_code=400, detail="Unable to truncate table.")


@app.post("/add_option/")
def add_one_option(new_option: OptionBase):
    """
    Insert one option into the options table.
    If the operation failed, return 400 bad request.
    """
    try:
        option = Option(**new_option.dict())
        db_ops.insert_new_option(option)
    except:
        raise HTTPException(status_code=400, detail="Cannot add new optio.")
    

@app.get("/get_pv_by_id")
def get_pv_by_id(input: CalculationExtraInput):
    """
    Calculate the present value of a given option, query by its ID.
    """
    try:
        option = db_ops.query_option_by_id(int(input.dict()['id']))
        if option is None:
            return {"message": "No option found. Calculation terminated"}
    except:
        raise HTTPException(status_code=400, detail="Something wrong with query operation, please double check.")
    
    # based on the given option and input, convert it to a dictionary and pass it to calculation function.
    option_dict = option.__dict__
    print(option_dict)
    calc_option_dict = input.dict()
    calc_option_dict['commodity_name'] = option_dict['commodity_name']
    calc_option_dict['expiry_date'] = option_dict['expiry_date']
    calc_option_dict['strike_price'] = option_dict['strike_price']
    calc_option_dict['option_type'] = option_dict['option_type']
    calc_option_dict['delivery_date'] = str(option_dict['delivery_date'])
    calc_option_dict['measurement'] = option_dict['measurement']
    pv = PVCalculator.calculate_present_value_for_one_option(calc_option_dict)

    result_dict = calc_option_dict
    result_dict['present_value'] = pv

    calculated_option = CalculatedOption(**result_dict)

    return calculated_option
