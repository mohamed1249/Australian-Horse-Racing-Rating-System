# Australian Horse Racing Rating System

This project involves the development of a sophisticated rating system for Australian horse racing. The system is designed to provide accurate and reliable ratings for each horse, reflecting their performance and potential. It integrates machine learning models and data analysis techniques to generate these ratings, and is built to integrate seamlessly with existing horse racing platforms.

## Table of Contents

1. [Job Description](#job-description)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Data](#data)
6. [Model Training](#model-training)
7. [Evaluation](#evaluation)
8. [Prediction](#prediction)
9. [Contributing](#contributing)
10. [License](#license)

## Job Description

We are seeking an experienced professional to assist in the development of this rating system. The successful candidate will be responsible for designing and implementing the rating algorithm, as well as integrating the system with our existing horse racing platform. Strong knowledge of Australian horse racing and the ability to analyze and interpret race data is essential for this role.

## Features

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning Models:
  - XGBoost Regressor
  - LSTM and GRU Neural Networks
- Model Evaluation and Hyperparameter Tuning
- Prediction and Integration with Existing Platforms

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/australian-horse-racing-rating-system.git
   ```
2. Navigate to the project directory:
   ```sh
   cd australian-horse-racing-rating-system
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the necessary datasets (`PF2021-23-Cleaned1.csv` and `2023-11-11-TestFile.csv`).
2. Run the Jupyter notebook or the Python script to process the data and train the models:
   ```sh
   jupyter notebook Horse_Racing_Rating_System.ipynb
   ```
3. To make predictions, use the `predict()` function provided in the script.

## Data

The dataset includes various features related to horse racing, such as:
- Starters
- Distance
- Position
- Margin
- Horse
- Trainer
- Jockey
- Weight
- Barrier
- Price
- Rating
- HorseId
- Sex
- Age
- Race Number (Rno)
- JockeyId
- TrainerId
- Settling Position
- Opening Price
- Market Rank

Ensure the data files are properly formatted and located in the correct directory before running the scripts.

## Model Training

The project uses both XGBoost and neural network models for predicting horse ratings. The following steps outline the training process:

1. Data Cleaning and Preprocessing:
   - Handling missing values
   - Removing irrelevant or redundant features
   - Encoding categorical variables

2. Feature Engineering:
   - Selecting important features
   - Balancing the dataset for binary classification

3. Model Training:
   - Training XGBoost Regressor
   - Training LSTM and GRU Neural Networks

4. Hyperparameter Tuning:
   - Using GridSearchCV for XGBoost to find the best parameters

## Evaluation

The models are evaluated using the following metrics:
- Accuracy
- Precision
- Recall
- F1 Score

The evaluation script prints detailed metrics for each class and displays confusion matrices.

## Prediction

The trained models are used to predict the ratings for new data. The `predict()` function combines the predictions from XGBoost and LSTM models to provide final ratings.

To make predictions:
1. Prepare the test data in the required format.
2. Use the saved models and encoders to transform and predict the ratings.

```python
predictions = predict(test_data)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
