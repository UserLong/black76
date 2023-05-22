from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_message():
    # Test root message return
    response = client.get("/")
    assert response.json() == {"message": "This is Black76 model."}

def test_display_all_options():
    # Test return all options
    response = client.get("/display_options")
    assert len(response.json()) == 10

def test_query_option_by_id():
    # Test query by id, make sure the fields are correctly returned
    response = client.get('/query_option/1')
    assert response['id'] == 1
    assert response['commodity_name'] == 'BRN'
    assert response['option_type'] == 'Call'
    assert response['exxpiry_date'] == 'Jan25'
    assert response['strike_price'] == 100.0
    assert response['measurement'] == 'USD/BBL'

def test_add_option():
    # Test to add dummy option
    dummy_option = {"commodity_name": "BRN", "strike_price": 160.0, "expiry_date": "Jul25", 
                    "option_type": "Call", "measurement": "USD/BBL"}
    response = client.post("/add_option", json=dummy_option)
    assert response['commodity_name'] == 'BRN'
    assert response['option_type'] == 'Call'
    assert response['exxpiry_date'] == 'Jul25'
    assert response['strike_price'] == 160.0
    assert response['measurement'] == 'USD/BBL'

def test_calculate_pv():
    # Test PV calculation
    dummy_input = {"id":1, 'spot_price': 100.0, "interest_rate": 0.05, "risk": 0.25}
    response = client.post("/get_pv_by_id", json=dummy_input)
    assert response.json()['present_value'] == 17.84

def test_truncate_options():
    # Test if truncate opertaion works
    response = client.get("/truncate_options")
    assert len(response.json()) == 0