# gptravel

This library uses the package manager poetry. To install poetry then run
```
pip install poetry 
```
After installing poetry then you must config the following flag
```
poetry config virtualenvs.in-project true
```
To intall the dependendencies then run the command
```
poetry install
```
To activate the virtual environment then run 
```
poetry shell
```
To add a new core library package then run the command
```
poetry add <package>
```
To add a new developer library patckage then run the command
```
poetry add --group dev <package>
```
To remove a package then run the command
```
poetry remove <package>