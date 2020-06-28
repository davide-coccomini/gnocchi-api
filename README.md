# Gnocchi project

## consumer.py
It contains the consumer code, which periodically (every 20 seconds) retrieves the saved data from a metric.
It must be specified the type of aggregation to use for the data and the metric we want to recover it from.
```
python consumer.py aggregation_type metric_name
```
## getMetrics.py
Used to view the list of available metrics.

## newPolicy.py
It is used to enter a new metric in which to save the recorded data. The name, granularity, which is the level of precision that must be kept when aggregating data, and the maximum number of points to be aggregated must be specified.
```
python newPolicy.py metric_name granularity points
```
## producer.py
Once called save periodically (every 5 seconds) a value in the specified metric.
```
python producer.py metric_name 
```
