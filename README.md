# OPENBUDGET
## About
Колекція скриптів для роботи з [openbudget api](https://confluence.spending.gov.ua/pages/viewpage.action?pageId=39553516). 

Перетворює накопичувальні дані у щомісячні і формує `.csv` таблиці для подальшого оновлення бази даних

## Usage
```bash
$ python -m venv env
$ source env/Scripts/activate
(env)$ pip install -r requirements.txt
(env)$ python openbudget/main.py
First month: [1]: 
Last month: [12]: 
Year: [2020]:
```
