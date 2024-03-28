# miniproject3SergioGabrielJiaweiKun
Practice program / Base template using Flask and SQLite to create a blog web application.

### INF601 - Advanced Programming in Python
### Sergio Gabriel Jiawei Kun
### Mini Project 3

## Description
## Getting Started

### pip install instructions
Ensure that the following lines are run for the program to function.
This pip installs all the required packages listed in the requirements.txt file.
```python
pip install -r requirements.txt
```

### Dependencies

* This version was developed using Python 3.11, and will run best in this version.

### Installing
* Python 3.11
* the following installs the application onto your virtual environment
```python
pip install -e .
```

### Executing program
* The first line is to initialise the sql database, and the 2nd 
asks flask to run the program for dev purposes.
* Remember that the first line needs to be re-run every time that changes are made to the schema.sql file.

```python
flask --app flaskr init-db 
flask --app flaskr run --debug
```
once running, you should be able to see the web application run in:
http://127.0.0.1:5000
* If there is an error, please refer to the above required packages in order for the program to run smoothly.

## Help

## Authors

Contributors names and contact info
* Sergio Gabriel Jiawei Kun
  * kunsergio117@outlook.com

## Version History
* 0.1
    * Initial Release

## License
* No licencing
## Acknowledgments
* [Matplotlib](https://matplotlib.org/stable/tutorials/pyplot.html)
* [Plotly](https://plotly.com/python/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
