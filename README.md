# bikeshareapi

This is an API service to connect 3rd party user with data using HTTP request. The data is real time data related to bike sharing app in Austin, Texas

**Available Endpoints**:
- Get all data related to stations: /stations/
- Get all data for each trips: /trips/
- Get data related to specific stations: /stations/<station_id>
- Get all data related to a specific trip: /trips/<trip_id>
- Get average duration for all bikes by subscriber type: /trips/average_duration
- Get average duration for specific bike id by subscriber type: /trips/average_duration/<bike_id>
- Get aggregated table on trips and station details based on start time: /aggregation/
