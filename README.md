# Online Shoppers Purchasing Intention Analysis

This repository contains Python code for analyzing the Online Shoppers Purchasing Intention dataset of UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)

## Task Summary
The dataset comprises 12,330 sessions, each associated with a distinct user over a one-year period. Among these sessions, 84.5% (10,422) represent negative class samples, indicating sessions that did not conclude with a shopping event. The remaining 15.5% (1,908) constitute positive class samples, signifying sessions that concluded with a shopping event. The dataset consists of feature vectors capturing various attributes for each of the 12,330 sessions. The intentional design ensures diversity by assigning each session to a different user, aiming to mitigate biases related to specific campaigns, special days, user profiles, or time periods.

The goal of our notebook is to find trends among online shoppers using data pre-processing, data visualization, and modeling techniques.

## Code Overview

The Python code includes:

- Data pre-processing
- Data visualization using matplotlib, plotly and seaborn
- Modeling with scikit-learn, trying several algorithms, and performing hyperparameter tuning with grid search

To make the data interactive and easy to explore, we used the Shapash library. It simplifies the creation of a web application to interact with the results of our analysis. This webapp offers an intuitive user experience and a better understanding of the insights extracted from the dataset.
We also developed an interface using the Django framework to visualize the graphs generated during our analysis.

## Results

The results of different models, including best parameters, training accuracy, classification report, and confusion matrix, are provided in the code.
-------A COMPLETER--------- (avec ce paragraphe)
This data visualization provides an in-depth view of visitor behavior on a website. Examining the monthly distribution reveals missing months and significant traffic peaks in May, November, March, and December, potentially linked to events like Black Friday.  So as expected, returning visitors dominate the traffic, followed by new visitors and other categories. Despite a majority of returning visitors, November and December see more new visitors, likely associated with specific events.  With all of this,  only 15% of visits result in purchases. Further exploration suggests that new visitors tend to explore administrative pages more, while regular visitors prefer product pages

