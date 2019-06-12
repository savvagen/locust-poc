### Locust Demo Project

![](https://cdn2.hubspot.net/hubfs/208250/Blog_Images/locustjava1.png)

## Writing tasks
1. Write your custom tasks using `TaskSet` class:
```
from locust import TaskSet

class UserScenario(TaskSet):

    ### Standart way to define tasks 
    # In this task get_specific_post() method will be executed 
    # 2-times rarely than get_post() method
    
    @task(1)
    def get_posts(self):
        self.client.get("/posts")
        
    @task(2)
    def get_specific_post(self):
        self.client.get("/posts/1")
        

```
2. Write tasks using predefined methods:

``` 
from locust import TaskSet

def get_posts(l):
    l.client.get("/posts")
    
def get_post(l):
    l.client.get("/posts/1")


class UserScenario(TaskSet):

    ### Another way to define tasks 
    # In this task get_post() method will be executed 
    # 2-times rarely than get_post() method
    
    tasks = {get_posts: 1, get_post: 2}


```

3. Setting up Locust Tests

``` 

class LoadTests(HttpLocust):
    host = "http://example.com"
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 30

```
## Writing Task Sequence
Let's create tasks to be executed in order according to @seq_task() priority:
In this example tasks should be executed in such way as:
1. get_all_posts()
2. create_custom_post()
3. watch_post() x 10

``` 
from locust import HttpLocust, task, events, seq_task, TaskSequence

class UserScenario(TaskSequence):
    @seq_task(1)
    def get_all_posts(self):
        self.client.get("/posts")

    @seq_task(2)
    def create_custom_post(self):
        self.client.post("/posts", {"title": 'foo', "body": 'bar', "userId": self.uuid})

    @seq_task(3)
    @task(10)
    def watch_post(self):
        self.client.get("/posts/1")

```

In this example @task decorator can be used to show the number tasks to be executed one after another.
Finally tasks will be executed in such order: first will be get_all_posts() --> second is create_custom_post() task --> and the last 10 times watch_post() task


### Running locust
```
locust -f reporting_test.py --host https://jsonplaceholder.typicode.com --no-web -c 20 -r 2 -t30s --logfile=locust.log


locust --host https://jsonplaceholder.typicode.com \      # Base URL
       -f locust_file.py WebsiteUser \                    # file with tasks and Test instance
       --no-web \                                         # without web console
       --csv=report                                       # will generate a report in csv format
       --logfile=locust.log                               # will write locust tasks log to specific file
       -c 20 \                                            # specifies the number of Locust users to spawn
       -r 2 \                                             # specifies the hatch rate (number of users to spawn per second).
       --run-time 30 \                                    # if you want to specify the run time for a test
       --print-stats                                      # print statistics in the console


```


### Run tests from slaves


#### Init master
``` 
 locust -f clients/api/api_client.py --master --master-host=localhost
```
#### Connect 2 slaves
```
locust -f clients/api/api_client.py --slave --master-host=localhost
locust -f clients/api/api_client.py --slave --master-host=localhost

```


#
### Running Stress and load testing for RANDOM SCENARIOS using CLI
#### Load Testing with stable 100 RPS

```
  locust -f scenarios/random_scenarios.py LoadTests --no-web -c 100 -r 20
```

#### Stress Testing with stable 100 RPS

```
  locust -f scenarios/random_scenarios.py StressTests --no-web -c 1000 -r 20

```

#
### Running Stress and load testing for SEQUENCE SCENARIOS using CLI
#### Load Testing with stable 100 RPS

```
  locust -f scenarios/sequence_scenarios.py --no-web -c 100 -r 20
```

#### Stress Testing with stable 100 RPS

```
  locust -f scenarios/sequence_scenarios.py --no-web -c 1000 -r 20

```

### Running Tests on master
1. Init master with command:
``` 
locust -f scenarios/random_scenarios.py LoadTests \
        --no-web -c 50 -r 10 \
        --master \
        --master-host localhost \
        --expect-slaves 2 \
        --run-time 30
```
The master will be initialized and will be waiting minimum for 2 slaves to be connected to the master

2. Init slaves with commands:
``` 
locust -f scenarios/random_scenarios.py --slave --master-host=localhost
locust -f scenarios/random_scenarios.py --slave --master-host=localhost
```
After slaves initialization, the testing will be started.



#
## Run Locust in Docker containers

1. Create network for locust tests: `docker network create --driver bridge locustnw`

2. Check network was created: `docker network inspect locustnw`


3. Copy files from `locust-docker` dir to the project root directory. 
Build Docker image `locust-tasks:latest` with command:
``` 
docker build -t locust-tasks:latest -f Dockerfile .
```

#### Run tests in docker container
1. Run Docker container with locust with web client:

``` 

 docker run -it --rm -p=8089:8089 \
    -e "TARGET_HOST=https://jsonplaceholder.typicode.com" \
    -e "ADD_OPTIONS=-c 100 -r 20" \
    -e "LOCUSTFILE_PATH=scenarios/random_scenarios.py" \
    -e "LOCUST_TEST=LoadTests" \
    --network=locustnw test/locust-tasks:latest
    
   OR
   
   docker run -it --rm -p=8089:8089 \
    -e "TARGET_HOST=https://jsonplaceholder.typicode.com" \
    -e "ADD_OPTIONS=-c 100 -r 20" \
    -e "LOCUST_TEST=LoadTests" \
    -e "LOCUSTFILE_PATH=scenarios/random_scenarios.py" \
    test/locust-tasks:latest
    

```


### Run tests using master and slaves

1. Run Docker container with master:

``` 

 
docker run --name master --hostname master -it --rm -p=8089:8089 \
   -e "TARGET_HOST=https://jsonplaceholder.typicode.com" \
   -e "LOCUSTFILE_PATH=scenarios/random_scenarios.py" \
   -e "LOCUST_TEST=LoadTests" \
   -e "LOCUST_MODE=master" \
   -e "EXPECT_SLAVES=2" \
   -e ADD_OPTIONS="-c 100 -r 20 --no-web" \
   --network=locustnw test/locust-tasks:latest


```
2. Run testing with spinning up 2 slaves:
```

 
docker run --name slave1 -it --rm \
   --link master --env NO_PROXY=master \
   -e "TARGET_HOST=https://jsonplaceholder.typicode.com" \
   -e "LOCUSTFILE_PATH=scenarios/random_scenarios.py" \
   -e "LOCUST_TEST=LoadTests" \
   -e "LOCUST_MODE=worker" \
   -e "LOCUST_MASTER=master" \
   --network=locustnw test/locust-tasks:latest

docker run --name slave2 -it --rm \
   --link master --env NO_PROXY=master \
   -e "TARGET_HOST=https://jsonplaceholder.typicode.com" \
   -e "LOCUSTFILE_PATH=scenarios/random_scenarios.py" \
   -e "LOCUST_TEST=LoadTests" \
   -e "LOCUST_MODE=worker" \
   -e "LOCUST_MASTER=master" \
   --network=locustnw test/locust-tasks:latest

```


## Running Locust In Docker mounting scenarios in volumes
Copy files from `locust-docker2` dir to the project root directory
1. Building image: `docker build -t test/locust:latest -f Dockerfile .`

2. Running simple web:
``` 

docker run -it --rm --name locust --hostname locust \
    -p=8089:8089 \
    -e "ATTACKED_HOST=https://jsonplaceholder.typicode.com" \
    -e "LOCUST_FILE=scenarios/random_scenarios.py" \
    -e "LOCUST_OPTS=-c 100 -r 20 --no-web" \
    -e "LOCUST_TEST=LoadTests" \
    -v `pwd`:/locust \
    test/locust:latest
    
```
    
3. Running master with 2 slaves:

``` 
  
docker run -it --rm --name master --hostname master \
    -p=8089:8089 \
    -v `pwd`:/locust \
    -e "ATTACKED_HOST=https://jsonplaceholder.typicode.com" \
    -e "LOCUST_MODE=master" \
    -e "LOCUST_FILE=scenarios/random_scenarios.py" \
    -e "LOCUST_OPTS=-c 100 -r 20 --no-web --expect-slaves 2" \
    -e "LOCUST_TEST=LoadTests" \
    test/locust:latest
    
docker run -it --rm --name slave1 --hostname slave1 \
    --link master --env NO_PROXY=master \
    -v `pwd`:/locust \
    -e "ATTACKED_HOST=https://jsonplaceholder.typicode.com" \
    -e "LOCUST_MODE=slave" \
    -e "LOCUST_MASTER=master" \
    -e "LOCUST_FILE=scenarios/random_scenarios.py" \
    -e "LOCUST_TEST=LoadTests" \
    test/locust:latest
    
    
docker run -it --rm --name slave2 --hostname slave2 \
    --link master --env NO_PROXY=master \
    -v `pwd`:/locust \
    -e "ATTACKED_HOST=https://jsonplaceholder.typicode.com" \
    -e "LOCUST_MODE=slave" \
    -e "LOCUST_MASTER=master" \
    -e "LOCUST_FILE=scenarios/random_scenarios.py" \
    -e "LOCUST_TEST=LoadTests" \
    test/locust:latest
```


## Run Locust in Kubernetes cluster

1. Setup kubectl configuration and connect to the cluster

2. Deploy master container `locust-master` in separated `locust` namespace:

``` 
kubectl apply -f locust-master.yml

```

3. Deploy slaves using command:
``` 
kubectl apply -f locust-master.yml

```
4. Watch the Locust Web UI on the `locust-master` Service: `http://<load_balancer_ip>:8089`
 
