# mainanalytics – Python Development Guide 

## ToC
- [mainanalytics – Python Development Guide](#mainanalytics---python-development-guide)
  * [Introduction](#Introduction)
  * [How to use the template](#how-to-use-the-template)
  * [Install enviroment from pyproject.toml file (poetry) - Recomended!](#install-enviroment-from-pyprojecttoml-file--poetry----recomended-)
  * [Add new dependencies and packages](#add-new-dependencies-and-packages)
  * [Virtual Enviroment handling with poetry](#virtual-enviroment-handling-with-poetry)
  * [VS Code COnfigurations:](#vs-code-configurations-)
  * [Formatter and Linter](#formatter-and-linter)
  * [Unit Tests](#unit-tests)
  * [Compilation (pyinstaller)](#compilation--pyinstaller-)
  * [Basic code quality agreements](#basic-code-quality-agreements)
  * [Commit style:](#commit-style-)
  * [Conda Enviroments (not recommended)](#conda-enviroments--not-recommended-)
    + [Install enviroment from enviroment.yml file](#install-enviroment-from-enviromentyml-file)
    + [Install new dependencies](#install-new-dependencies)

## Introduction

The mainanalytics team develops code that is developed, maintained, and used by multiple users. Therefore, we place higher demands on code quality that go beyond validation and testing to allow continuous development, deployment and maintenance. 

## How to use the template

### Use this as tempate repository
Follow the instructions here:
https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template

### By hand (more complicated)
- Create a new git repository

- Clone template : 
```bash
git clone https://github.com/biontech-qm/gbs-pytemp-simple.git
```

- remove git history from local repo
```bash
cd my-project
rm -rf .git 
```

- initialse new local repo and push to origin
```bash
git init           # start a fresh repo
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <link to new repo>
git push -u origin main
```

-  next step:
    - Create a new venv using Poetry (recommended)
    - Alternative: Create a new venv using conda (see next section)


## Install enviroment from pyproject.toml file (poetry) - Recomended!
1. Ensure that poetry is installed, if not do so by following information on the webside: https://python-poetry.org/ 
or use 
    ```bash
    pip install poetry
    ```
2. Recommendation: Ensure to create venv in project folder for easier handling of multiple projects
    ```bash
    poetry config virtualenvs.in-project true
    ```
3. Lock poetry file and install venv
    ```bash
    poetry lock
    poetry install
    ```


## Add new dependencies and packages
General
    ```bash
    poetry add  <mypackage>
    ```

Into groups (e.g. for dev)
    ```bash
    poetry add --group dev <mypackage>
    ```

- Run scrip: 
    ```bash
    poetry run <my-script>
    ```

- Run pytest: 
    ```bash
    poetry run pytest
    ```
Automatic validation reports are created via pytest-html. Configuration is handled by pytest.ini and the test/conftest.py file


- (Not required) Extract requirements.txt
(toml -> requirements (requires plugin))
    ```bash
    poetry export -f requirements.txt --without-hashes -o requirements.txt
    ```
       
## Virtual Enviroment handling with poetry 
Install Virtal Enviroment the first time
    ```bash
    poetry ini_options
    ```
        
Activate Poetry Venv 
    ```bash
    poetry env activate
    ```
    
Install VENV in workfolder
    ```bash
    poetry config virtualenvs.in-project true
    ```
        
Virtual Environment Informations
```bash
    poetry env info
    poetry env info --path
    poetry env info --executable
    poetry env list
    poetry env remove python
```




## VS Code COnfigurations:
Ensure to select the correct interpreter in VS Code by Ctrl+Shift+P >Python: Select Interpreter.
Maybe you neet to set the User settings by Ctrl+Shift+P >Preferences: Open User Settings (JSON) and add a correct pylint and interpreter path: e.g. like
```
{
   "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.autoFormatStrings": true,
    "python.analysis.completeFunctionParens": true,
    "python.analysis.extraPaths": [
        "${workspaceFolder}/.venv/Lib",
        "${workspaceFolder}/.venv/Lib/site-packages",
    ],
    "pylint.interpreter": [
        "${workspaceFolder}/.venv/Scripts/python.exe"
    ],
    "pylint.lintOnChange": true,
    "pylint.path": [
        "${workspaceFolder}/.venv/Lib",
        "${workspaceFolder}/.venv/Lib/site-packages",

    ],
}
```




## Formatter and Linter
Basic formatter and linter must be used. The pipeline enforces formatted code. We will use ruff as formatter (can also be used as linter and allows for auto-fixing). We will expect a pylint score of >0.9 and no critical issue

Run linter: 
```bash
poetry run pylint <myfile|module>.py 
```

Configuration file: .pylintrc 

 Run formatter:
```bash
poetry run python -m ruff format <myfile|module>
```

 Run ruff as linter
```bash
poetry run ruff check <myfile|module>
```

Run ruff as linter with auto-fixing
 ```bash
poetry run ruff check --fix <myfile|module>
 ```

Configuration file: pyproject.toml

## Unit Tests
Unit tests are stored in test folder and can be executed via pytest
 ```bash
poetry run pytest 
 ```
Configuration file: pyproject.toml


## Compilation (pyinstaller)
Two different options. 
1. Onefile compilation. 
    - Advantage: all binaries and resources are packed into a zip file. 
    - Disadvantage: longer start time, as the file is first unpacked into a temporary folder. This requires all local resources to be searched for in the temporary folder. See template resource_path function
    ```bash
    pyinstaller main_onefile.spec
    ```
2. Onedir compilation
    - Advantage: Application starts faster
    - Disadvantage: Application is a folder. Best practice to create a shortcut for endusers in a safe enviroment
    ```bash
    pyinstaller main_standard.spec
    ```



## Basic code quality agreements 

1. Typing has to be used! Type of arguments and return values 
2. Docstring documentation of all important functions and classes 
3. Separate logic & GUI & IO 
4. Avoid usage of global variables, no plain text variable declaration 
5. Avoid side effects 
6. Functional style with return values 
7. Always start in main.py with in if __name__ == "__main__": block 
8. All import at the start of the file 

## Commit style: 

Use specific tag 
- feat:  
- fix:
- refactor:
- release:

## Conda Enviroments (not recommended)

### Install enviroment from enviroment.yml file
Create Conda enviroment from enviroment.yml and overwritte venv name:
```bash
conda env create -f environment.yml -n <myenv>
```

Activate enviroment:
```bash
conda activate <my-env>
```
Create new enviroment.yml
```bash
conda env export --no-builds > environment.yml 
```

### Install new dependencies
All new dependencies should be installed via conda to ensure reusability

Ensure the correct venv
```bash
conda activate <my-env>
```

Install via conda
```bash
conda install package
```