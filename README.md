# mlflow-report
A simple script created to convert mlflow logs to a csv report.

## Description
When reading log files, it may occur that some frameworks run into problems (internal errors,memory errors, etc.). 
The script create-report.py of this repository allows you to recover the mlflow log files by writing them into a csv file, that is easy manageable by standard data manipulation and analysis libraries and softwares such as Pandas and Excel.

## Usage
create-report.py mlruns

Where mlruns is the mlflow folder name.

Notice that the mlflow folder may contain more than 1 subfolders, i.e. more experiments.
