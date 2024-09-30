#!/bin/bash

cd bybit
poetry lock
poetry install
cd ..
cd strategies
poetry lock
poetry install
cd ..
poetry lock
poetry install