# OPENBUDGET
## About
Колекція скриптів для роботи з [openbudget api](https://confluence.spending.gov.ua/pages/viewpage.action?pageId=39553516). 

Перетворює накопичувальні дані у щомісячні і формує `.csv` таблиці для подальшого оновлення бази даних

## Usage
```
$ python -m venv env
$ source env/Scripts/activate
(env)$ pip install -r requirements.txt
(env)$ python openbudget/main.py
First month: [1]: 1
Last month: [12]: 8
Year: [2020]: 2020
2020-10-13 15:35:56,665 [INFO]: Downloading raw data...
2020-10-13 15:42:20,118 [INFO]: Transforming raw data into processed...
2020-10-13 15:52:24,136 [INFO]: Merging multiple tables into one...
2020-10-13 15:53:58,097 [INFO]: Saving data for the last month separately...
2020-10-13 15:54:49,604 [INFO]: Passed tests.
2020-10-13 15:54:49,604 [INFO]: Done.
```
