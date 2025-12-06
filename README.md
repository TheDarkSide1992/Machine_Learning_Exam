Machine_learning_Exam

## DEVS
* Jens
* Andreas
* Emil

## Purpose
This Project is a school exam project at EASV(erhvervsakademi sydvest | business academy southwest). 
This project where made for purely educational purposes and should not be used for any monetary gains.

We are using the open food tox database from efsa (european food and safety agency)

> The following link will tell you more about the OpenFoodTox dataset
>https://www.efsa.europa.eu/en/discover/infographics/openfoodtox-chemical-hazards-database

## Setup
Install the Python dependencies.

## set up venv

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

## Run postgres in docker
```bash
cd xlsx_to_sql_database_converter && docker compose up -d && cd ..
```

download the OpenFoodTox data set from folowing link 
> https://zenodo.org/records/8120114/files/OpenFoodToxTX22809_2023.xlsx?download=1

and place it in the folder named data
set up the database tables and data with the xlsx to sql database converter

## Run xlsx converter

```bash
python -m xlsx_to_sql_database_converter.converter
```

## Requirements

- Python 3.10+
- autogen-agentchat
- gemini
- autogen
- ollama
- fix-busted-json

## Create config
> [!NOTE]
> the config file should be placed in the evaluate_agent folder and named config.py
> It is important that this file never is commited.
> It is necessary for running the application.
> For ai We recommend using gemini ai.
> You can get access to a free version at https://aistudio.google.com/api-keys
> Replace <YOUR_API_KEY> with your actual api key.
```python
_MODEL_NAME = "gemini-2.5-flash"
_API_KEY = "YOUR_API_KEY"

LLM_CONFIG = {
    "config_list": [
        {
            
            "model": f"{_MODEL_NAME}",
            "api_key": f"{_API_KEY}",
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
        }
    ]
}

DATABASE = {
    "database": "openfoodtox_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5001
}

```

## Run

```bash
python -m exam_agent -C
```