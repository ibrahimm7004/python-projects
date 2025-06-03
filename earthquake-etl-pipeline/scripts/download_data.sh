#!/bin/bash

mkdir -p data

curl -o data/earthquake_data.csv https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv

echo "Download complete: data/earthquake_data.csv"  # confirmation
