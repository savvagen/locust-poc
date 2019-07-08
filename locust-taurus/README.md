### Run taurus with docker 

1. Go to script directory:

```
cd ~/locust-poc/locust-taurus/bzt_script

```

2. Run command:

``` 
docker run --rm -v $PWD:/bzt-configs -v $PWD/../bzt_artifacts:/tmp/artifacts --name "taurus" blazemeter/taurus stress_test.yml
```