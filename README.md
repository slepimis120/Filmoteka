![PlaylistGenie](https://i.imgur.com/sj7DUsS.png)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

# Filmoteka
Filmoteka project for "Software Patterns and Components"

## Project goal
The goal of this project is to visualize graph-like structures, supporting multiple data sources and their visualization. The project aims to leverage the benefits of object-oriented programming, enabling easy modification and extension of software components through the use of plugins.

## Installing / Getting started
Follow these steps to set up and run the project:

1. Clone the repository
```shell
git clone git@github.com:slepimis120/Filmoteka.git
cd Filmoteka
```

2. Create and activate a virtual environment
```shell
python -m venv venv
source venv/bin/activate
```

3. Install the required packages
```shell
pip install -r filmoteka_api/requirements/requirements.txt
```

4. Navigate to the 'filmoteka_platform' directory and run the project
```shell
cd filmoteka_api/src/filmoteka_platform
python manage.py runserver
```

After that, navigate to http://localhost:8000/ where you can use the program itself.

## Licence 

PlaylistGenie is available under the GNU GPLv3 license.
