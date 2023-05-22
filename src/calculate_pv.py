from db.models import CalculatedOption
from db_ops import query_option_by_id
from scipy.stats import norm
import datetime
import pandas as pd
from numpy import sqrt, log, exp

class PVCalculator:

   @classmethod
   def calculate_present_value_for_one_option(cls, calc_input_dict: dict):
     pv = 0.0

     # Calculate time gap between today and the delivery date
     today = datetime.datetime.today()
     time_gap = (pd.to_datetime(calc_input_dict['delivery_date']) - today).days
     time_gap = round(time_gap / 365, 3)

     # Calculate d1
     d1 = (log(calc_input_dict['spot_price'] / calc_input_dict['strike_price']) \
            + (calc_input_dict['interest_rate'] + calc_input_dict['risk']**2 / 2) * time_gap)\
          / (calc_input_dict['risk'] * sqrt(time_gap))
     
     # Calculate d2
     d2 = d1 - calc_input_dict['risk'] * sqrt(time_gap)

     # Calculate PV for call scenario
     if calc_input_dict['option_type'] == 'Call':
        pv = calc_input_dict["spot_price"] * norm.cdf(d1) - calc_input_dict["strike_price"] * exp(-calc_input_dict["interest_rate"] * time_gap) * norm.cdf(d2)
      
     # Calculate PV for put scenario
     if calc_input_dict['option_type'] == 'Put':
        pv = calc_input_dict["strike_price"] * exp(-calc_input_dict["interest_rate"] * time_gap) * norm.cdf(-d2) - calc_input_dict["spot_price"] * norm.cdf(-d1)
        
     return round(pv, 2)
        