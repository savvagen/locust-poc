import locust
import gevent
from locust.events import EventHook
from locust import runners, events


# Hooks asnd Conditions for Stress Testing quiting

def my_response_time_handler(request_type, name, response_time, response_length, **kw):
    # print("Successfully fetched: %s" % (name))
    if response_time > 4000:
        print("Stopping Requests! \n The Response time is > than 4000 ms. \n Stopping!")
        runners.logger.error(
            "STOPPING TESTS!!! Response time is {} ms. The maximal resp. time is 4000 ms".format(response_time))
        runners.locust_runner.stop()
        runners.locust_runner.quit()
    # print("Stats: \n {}".format(runners.global_stats.__dict__))
    # print("Start Time: \n {}".format(runners.global_stats.start_time))
    # print("Total Request Number: \n {}".format(runners.global_stats.total.num_requests))


def my_requests_number_handler(request_type, name, response_time, response_length, **kw):
    total_reqs = locust.runners.global_stats.total.num_requests
    # print("Successfully fetched: %s" % (name))
    if total_reqs > 10000:
        print("Stopping Requests! \n The Requests Number is: {}. \n Stopping!".format(total_reqs))
        runners.logger.error("STOPPING TESTS!!! \n The Requests Number is: {}. \n Stopping!".format(total_reqs))
        runners.locust_runner.stop()
        runners.locust_runner.quit()


def my_error_handler(request_type, name, response_time, exception, **kw):
    print("Got Exception: %s" % (exception))
    total_failures = runners.global_stats.errors
    if total_failures >= 1:
        runners.logger.error("STOPPING TESTS!!! ERROR FOUND: {}".format(exception))
        runners.locust_runner.stop()
        runners.locust_runner.quit()