import glob
import numpy as np
import ntpath
import os
import pandas as pd
import sys
import time


def extract_file_name(path):
    return ntpath.basename(path)

def create_dataframe(params_path, metrics_path):
    """
    # Creates an empty pandas dataframe having as column the names of the files existing in the specified folders
    # Parameters:
    #    params_path: path of the folder containing the parameters
    #    metrics_path: path of the folder containing the metrics
    # Return:
    #    An empty Pandas dataframe having as column the names of the files existing in the specified folders
    """
    # Add params columns
    params = glob.glob(params_path + '*')
    param_names = [extract_file_name(param) for param in params]
    params = ['param-' + param for param in param_names]

    # Add metrics columns
    metrics = glob.glob(metrics_path + '*')
    metric_names = [extract_file_name(metric) for metric in metrics]
    metrics = ['metric-' + metric for metric in metric_names]
    
    # Column name unions
    column_names = params + metrics

    return pd.DataFrame(columns= column_names), param_names, metric_names

def create_report(mlflow_folder):
    """
    # Creates a pandas dataframe from the mlflow logs of the input folder
    # Parameters:
    #    mlflow_folder: path of the folder containing the mlflow logs
    # Effects:
    #    It creates a Pandas dataframe for each experiment of the specified folder
    """
    exp_n = next(os.walk(mlflow_folder))[1]
    print("Converting " + str(len(exp_n) - 1) + " experiments")

    for i, exp in enumerate(exp_n[1:]):
        
        runs = next(os.walk(mlflow_folder + '/' + exp))[1]

        df = param_names = metric_names = None
        n_runs = len(runs) - 1

        print("Saving " + str() + " runs ...")
        start = time.time()

        for j, run in enumerate(runs[1:]):
            sys.stdout.flush()
            print("Runs: " + str(j + 1) + "/" + str(n_runs))

            row = {}
            
            params_folder = mlflow_folder + '/' + exp + '/' + run + '/params/'
            metrics_folder = mlflow_folder + '/' + exp + '/' + run + '/metrics/'

            if(j == 0): #
                df, param_names, metric_names = create_dataframe(params_folder, metrics_folder)

            # Adding parameters
            for param in param_names:
                # Reading param
                f = open(params_folder + param)
                row['param-' + param] = f.read()

            for metric in metric_names:
                # Reading metrics
                f = open(metrics_folder + metric)
                row['metric-' + metric] = f.read()

            df.append(row, ignore_index = True)

        stop = time.time()
        df.to_csv('report-' + str(i) + '.csv')

        print("Saved. Time elapsed: " + str(stop-start) + " seconds")
    return



if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('Usage: ' + sys.argv[0] + ' mlflow_folder')
        exit(1)
    create_report(sys.argv[1])