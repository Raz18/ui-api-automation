import pytest
from playwright.sync_api import APIRequestContext, expect
from utils.logger import setup_logger

logger = setup_logger("API_Tests")


@pytest.mark.api
def test_airport_count_is_30(api_request_context: APIRequestContext):
    """Scenario 1: Verify Airport Count"""
    logger.info("Starting test: Verify Airport Count")
    
    logger.info("Making GET request to /api/airports")
    resp = api_request_context.get("/api/airports")
    
    logger.info(f"Request URL: {resp.url}")
    logger.info(f"Response status: {resp.status}")
    
    expect(resp).to_be_ok()
    logger.info("Response status validation passed")
    
    data = resp.json()
    logger.info(f"Successfully parsed JSON response")
    
    assert 'data' in data
    actual_count = len(data['data'])
    logger.info(f"Found {actual_count} airports in response")
    
    assert actual_count == 30, f"Expected 30 airports, but found {actual_count}"
    logger.info("✅ Airport count validation passed: 30 airports found")

@pytest.mark.api
def test_specific_airports_present(api_request_context: APIRequestContext, airports_test_data):
    """Scenario 2: Verify Specific Airports"""
    logger.info("Starting test: Verify Specific Airports")
    
    expected_airports = airports_test_data.expected_airports
    logger.info(f"Looking for airports: {expected_airports}")
    
    logger.info("Making GET request to /api/airports")
    resp = api_request_context.get("/api/airports")
    expect(resp).to_be_ok()
    
    logger.info(f"Response status: {resp.status}")
    
    data = resp.json()
    names = {item['attributes']['name'] for item in data.get('data', [])}
    logger.info(f"Found {len(names)} airport names in response")

    missing_airports = set(expected_airports) - names
    if missing_airports:
        logger.error(f"❌ Missing required airports: {missing_airports}")
        logger.info(f"Available airports: {sorted(names)}")
    else:
        logger.info(f"✅ All expected airports found: {expected_airports}")
        
    assert not missing_airports, f"Missing required airports: {missing_airports}"

@pytest.mark.api
def test_distance_between_airports_greater_than_400_km(api_request_context: APIRequestContext, airports_test_data):
    """Scenario 3: Verify Distance Between Airports"""
    logger.info("Starting test: Verify Distance Between Airports")
    
    from_airport = airports_test_data.distance_from
    to_airport = airports_test_data.distance_to
    logger.info(f"Calculating distance from {from_airport} to {to_airport}")
    
    payload = {"from": from_airport, "to": to_airport}
    logger.info(f"POST payload: {payload}")
    
    resp = api_request_context.post("/api/airports/distance", data=payload)
    logger.info(f"Response status: {resp.status}")
    expect(resp).to_be_ok()
    
    data = resp.json()
    logger.info(f"Distance response data: {data}")
    
    # The key is 'kilometers', not 'km'
    distance_km = float(data['data']['attributes']['kilometers'])
    logger.info(f"Distance calculated: {distance_km} km")
    
    if distance_km > 400:
        logger.info(f"✅ Distance validation passed: {distance_km} km > 400 km")
    else:
        logger.error(f"❌ Distance validation failed: {distance_km} km <= 400 km")
        
    assert distance_km > 400, f"Expected distance > 400 km, but got {distance_km}"