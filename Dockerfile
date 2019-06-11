#FROM python:2.7.13
FROM python:3

MAINTAINER Savva Genchevskiy

# Add the external tasks directory into /locust-tasks
RUN mkdir locust-tasks
ADD /hooks /locust-tasks/hooks
ADD /scenarios /locust-tasks/scenarios
ADD /requirements.txt /locust-tasks/requirements.txt
ADD /run.sh /locust-tasks/run.sh

WORKDIR /locust-tasks

# Install the required dependencies via pip
RUN pip install -r /locust-tasks/requirements.txt

# Set script to be executable
RUN chmod 755 run.sh

# Expose the required Locust ports
EXPOSE 5557 5558 8089

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["./run.sh"]

#CMD /usr/local/bin/locust -f scenarios/random_scenarios.py $LOCUST_TEST --host=$TARGET_HOST -c $NUM_CLIENTS -r $HATCH_RATE --no-web
