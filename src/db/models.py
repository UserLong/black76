from typing import Any
from sqlalchemy import Column, Integer, String, Float, Date
from db.database import Base
import calendar
from datetime import datetime, timedelta
from pydantic import BaseModel


class Option(Base):
    """
    Database model for option
    """
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True, index=True)
    commodity_name = Column(String)
    expiry_date = Column(String)
    strike_price = Column(Float)
    option_type = Column(String)
    measurement = Column(String)
    delivery_date = Column(Date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delivery_date = self.get_delivery_date()

    @staticmethod
    def contract_rules(commodity_name, year, month):
        """
        Rule dictionary for delivery date calculation.
        Depends on how are the contract rules look like, the data structure could be either dict or list.
        """
        rules = {'BRN': 2, 'HH': 1}
        month += rules[commodity_name]
        
        if month > 12:
            return year+1, month-12
        
        return year, month
    
    def get_delivery_date(self):
        """
        Calculate future delivery date based on contract rules.
        """
        months_dict = {
            "Jan": 1,   "Feb": 2,   "Mar": 3,   "Apr": 4,   "May": 5,   "Jun": 6,
            "Jul": 7,   "Aug": 8,   "Sep": 9,   "Oct": 10,  "Nov": 11,  "Dec": 12
        }

        # convert year to 4-digit format and convert month from string to integer
        year = int("20" + self.expiry_date[-2:])
        month = months_dict[self.expiry_date[:3].capitalize()]

        # go through contract rules to get delivery date
        year, month = Option.contract_rules(self.commodity_name, year, month)

        # find delivery date of the underlying future
        last_day_of_month = calendar.monthrange(year, month)[1]
        delivery_date = datetime(year, month, last_day_of_month)

        # make sure it is the last business day
        back_days = {5:1, 6:2}
        if delivery_date.weekday() >= 5:
            delivery_date -= timedelta(days=back_days[delivery_date.weekday()])

        return delivery_date
    

class OptionBase(BaseModel):
    # Base class of option. 
    id: str
    commodity_name: str
    expiry_date: str
    strike_price: float
    option_type: str
    delivery_date: str
    measurement: str
    

class CalculationExtraInput(BaseModel):
    # Class for calculation input arguments, such as
    # commodity ID, spot price, interest rate, risk and etc..
    id: int
    spot_price: float
    interest_rate: float
    risk: float


class CalculatedOption(OptionBase):
    # Class for the option after PV calculation
    spot_price: float = 0.0
    interest_rate: float = 0.0
    risk: float = 0.0
    present_value: float = 0.0