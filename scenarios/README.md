
### Running Stress and load testing for RANDOM SCENARIOS using CLI

#### Load Testing with stable 100 RPS

```
  locust -f scenarios/random_scenarios.py --no-web -c 100 -r 20
```

#### Stress Testing with stable 100 RPS

```
  locust -f scenarios/random_scenarios.py --no-web -c 1000 -r 20

```