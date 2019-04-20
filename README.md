# Heart-Disease-Analysis
COMP9321 19T1 Assignment 3

Group: Master Branch

## Introduction
A machine learning project based on [UCIrvine ML dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/), including machine learning implementation, backend and frontend, which allows users to input attributes to predict heart diseases. The project has such key function: dataset display, attribute correlations display, training accuracy display and prediction.

## How to run this project
1. **Install requirements:** `pip3 install -r requirements.txt`
2. **Run backend:** `python3 run.py`
3. **Open another terminal, and:** `cd frontend`
4. **Install React framework and modules:** `npm i`
5. **Run frontend:** `npm start`

## How to reproduce prediction models
**Please Note:** You must run following codes in **its** directory, NOT the root directory.

1. **For 0-1 Prediction model:** We use linear regression with K-fold cross validation to predict the whether the user may suffer from heart disease. The final accuracy is 90.9%.
To reproduce the model, using `cd machine_learning` and `python3 kfold.py`.


2. **For Multi Prediction model:** We use KNN algorithm to predict the **exact** target numbers (0-4) for different types of heart diseases. The final accuracy is almost 70%.
To reproduce the model, using `cd machine_learning` and `python3 multi_classification.py`.


3. **For Feature Selection:** We use Pearson correlation coefficients to select the top five most important factors.
To see the correlation coefficients ranking, using `cd machine_learning` and `python3 feature_selection.py`.

## Prediction Accuracy
![LR](/data/LR.png)
![KNN](/data/KNN.png)
![FS](/data/FS.png)

## Graph Display Sample
![Sample Graph](/data/Graph.png)

## API Specification

**Get data to plot charts**

- GET data of two attributes (each for all values) from the database to plot a chart.

    ```
    GET /attr?name=<AttributeName>
    
    Sample Request
    GET /attr?name=cp
    
    Sample Response
    {
        "cp" : "[[63, 1, 1], [67, 1, 4] ...]"
    }
    ```
- If any attributes does not exist in database, return message and **404 Error**.

    ```
    Response
    {
        "message" : "<AttributeName> not found in database!"
    }
    ```
- If no attribute is given, return message and **400 Error**.

    ```
    Response
    {
        "message": "Please ensure you provide a coordinate!"
    }
    ```

**Get important factors**
 
- GET the potential important factors analyzed by machine learning algorithms.
- Note the number of important factors can be changed.

    ```
    GET /factors
    
    Sample Response
    {
        "importantFactor1": "sex",
        "importantFactor2": "age"
        ...
    }
    ```
- If the important factors are not yet determined (NOT happen when finished), return message and **404 Error**.

    ```
    Response
    {
        "message": "The important factors are not yet determined!"
    }
    ```

**Predict users' risks of suffering heart diseases**

- POST the important factors to backend from user input.
- Predict the result based on `PredictType`.
- If `PredictType` = 1, it means 0-1 classification
- If `PredictType` = 2, it means multiple classification

    ```
    POST /predict?type=<PredictType>
    
    POST Payload
    {
        "ca": "0",
        "oldpeak": "2.3"
        ...
    }
    
    Sample Response
    {
        "message": "No Disease"
        "level": "0"
    }
    ```
- If the `PredictType` is not either 1 or 2, return message and **400 Error**.

    ```
    Response
    {
        "message" : "Bad Request, please check your argument is either 1 or 2!"
    }
    ```

- If any attributes in POST payload are not **Important Factors**, return message and **404 Error**.

    ```
    Response
    {
        "message" : "<AttributeName> is not an important factor!"
    }
    ```
    
- If any attributes in POST payload is malformed (e.g. empty payload), return message and **400 Error**.

    ```
    Response
    {
        "message" : "Bad Request, please check your payload format!"
    }
    ```
