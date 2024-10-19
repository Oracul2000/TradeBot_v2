#!/bin/bash

poetry install
poetry shell


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

cd ui/ui/telegram
poetry lock
poetry install
cd ../..
poetry lock
poetry install
cd ..


python start/start/trade_teststart.py
python start/start/ui_telegram_teststart.py