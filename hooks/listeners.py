from statistics import median

import locust
from locust import runners, events
from locust.events import EventHook


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





total_rps_number = 0

def set_rps_number(rps):
    global total_rps_number
    total_rps_number = rps

def get_rps_number():
    global total_rps_number
    return total_rps_number


##### Every slave will spin up 2 users
####### The users count and desire_rps should be counted according to the slaves number
def on_report_to_master(client_id, data, **kw):
    # Executes before on_slave_report
    # Validate data statistics on slave
    clients_number = runners.locust_runner.num_clients
    hatch_rate = runners.locust_runner.hatch_rate
    print("Clients number: {}".format(clients_number))
    rps_mid = data['stats_total']['num_reqs_per_sec'].values()
    print(rps_mid)
    if len(rps_mid) >= 1:
        rpss = list(rps_mid)
        rpss.sort()
        print("Max {}".format(max(rpss)))
        print("Mid {}".format(median(rpss)))
        if max(rpss) < 100:
            clients_number += 2
            runners.locust_runner.start_hatching(clients_number, hatch_rate)
            events.hatch_complete.fire(user_count=clients_number)
        if max(rpss) >= 103:
            clients_number -= 1
            runners.locust_runner.start_hatching(clients_number, hatch_rate)
            events.hatch_complete.fire(user_count=clients_number)


def on_slave_report(client_id, data, **kw):
    # Executes after on_report_to_master
    # Print data statistics on master
    rps_number = runners.global_stats.total.current_rps
    clients_number = runners.locust_runner.num_clients
    hatch_rate = runners.locust_runner.hatch_rate
    print("Users number: {}".format(data['user_count']))
    # print("Clients number: {}".format(clients_number))
    # print("RPS number: {}".format(rps_number))
    clients_number += data['user_count']
    set_rps_number(rps_number)
    # if rps_number < 100:
    #     clients_number += 2
    #     runners.locust_runner.start_hatching(clients_number, hatch_rate)
    #     events.hatch_complete.fire(user_count=clients_number)


def on_slave_report_latency_handler(client_id, data, **kw):
    # Executes after on_report_to_master
    # Print data statistics on master
    current_95_percentile_latancey = runners.global_stats.total.get_current_response_time_percentile(95)
    overall_95_percentile_latancey = runners.global_stats.total.get_response_time_percentile(95)
    # print("Overall latency: {}".format(runners.global_stats.total.avg_response_time))
    # print("Current 95% latency: {}".format(runners.global_stats.total.get_current_response_time_percentile(95)))
    print("Overall 95% latency: {}".format(runners.global_stats.total.get_response_time_percentile(95)))
    if overall_95_percentile_latancey is not None:
        if overall_95_percentile_latancey > 1000:
            runners.logger.error("STOPPING TESTS!!!\n RESPONSE TIME TRIGGER:\n 95% of requests is > than 1000 ms")
            runners.locust_runner.stop()
            runners.locust_runner.quit()
