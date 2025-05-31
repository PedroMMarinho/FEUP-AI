# FEUP-AI2
Group Members
1. Pedro Marinho (up202206854@up.pt)

2. Sérgio Nossa (up202206856@up.pt)

3. Xavier Martins (up202206632@up.pt)

## **Project Overview**
This project focuses on mental health analysis, aiming to detect whether an individual is likely to be depressed or not based on various personal and survey-based attributes. It uses several machine learning algorithms to train, evaluate, and compare classification performance in predicting depressive tendencies.

## **How to Run**
To set up and run the notebook locally, follow these steps:

### 1. Clone the repository
Clone this GitHub repository to your local machine.

### 2. Create a virtual environment
Run the following command in the root directory of the project:

For Windows:
`python -m venv venv
venv\Scripts\activate`

For macOS/Linux:
`python3 -m venv venv
source venv/bin/activate`

### 3. Install required packages
With the virtual environment activated, install the dependencies:

`pip install -r requirements.txt`

Make sure the requirements.txt file includes all the necessary libraries like:
numpy, pandas, matplotlib, seaborn, scikit-learn, xgboost, lightgbm, catboost, etc.

### 4. Run the notebook
Launch Jupyter Notebook:

`jupyter notebook`

Then open `notebook.ipynb` and run all the cells to see the full analysis.