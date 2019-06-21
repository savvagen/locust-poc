
# Generate Locust test using swagger.json
https://github.com/lieldulev/swagger-to-locustfile

## Installation

Best option is:

  1. `$ git clone https://github.com/DataGreed/swagger-to-locustfile.git`
  2. `$ cd swagger-to-locustfile`
  3. `$ npm -g install`
  4. You are good to go.
  
  
Generate locust file:

``` 
cd locust-swagger

swagger2locust ./swagger.json > ../scenarios/my_locustfile.py

```