# PMTCT

Devs
1. [Bronch Mukami](https://github.com/MadeaRiggs)
2. [Michael Wekesa](https://github.com/wekesa360)
3. [Brayan Kai](https://github.com/mwanyumba7)
4. [Ivan Bowen](https://github.com/874bowen)
5. [Francis Njoroge](https://github.com/francis450)

<details> 
    <summary><h2>Business Understanding</h2></summary>
    <h3>I. Background of the study </h3>

-There is a significant challenge in the reporting of PMTCT tests as some facilities do not report these tests which affects the accuracy of estimates of HIV prevalence. This is critical for planning interventions to reduce HIV transmission.

-There are facilities whose DHIS records does not match the DATIM records in both HTS and PMTCT data.

<h3>II. Objectives </h3>

The main objective of this report is to analyze the presented datasets based on the reporting of the PMTCT tests using summary statistics, visualizations, statistical models, and textual explanations. It specifically seeks to:


1. Identify the different data behaviors in our datasets.
2. Understand the relationship between the PMTCT tests reporting and HTS test Reporting, then proceed to advise on the estimates where data gaps are found.
3. Provide a basis and guide the automation of the data cleaning process.
4. Dive deep into the step by step approach taken in the development of  a classification model to assist in the identification of PMTCT sites that do not report tests.

</details>

<details>
  <summary><h2>Data Acqusition</h3></summary>
  <h3>I. Data Sources </h3>
 
-The data for this project was obtained from various health facilities in the country. The data was collected through the Health Information Management System (HIMS) and the District Health Information System (DHIS). These systems are widely used in the healthcare industry to collect, store, and manage patient data.
    
-The dataset used in the analysis consists of a Four xlsx files, where each row represents a test report from a specific facility. 

-Two of the xlsx files contain three sheets from Migori ,Kakamega and Bungoma counties, categorized in their specific counties:

1. PMTC-KSM
    This sheet contains records of all reported HIV/AIDS tests done on pregnant women across different periods of the year 2019 and 2020 in Migori County, Kakamega County and Migori County. 
    
2. HTS_TST
    This file contains  records of all reported HIV/AIDS tests across different periods of time by facilities in Migori County, Kakamega County and Bungoma.
    
-The other two xlsx files differ in that they have test indicators of different counties in one sheet:

1. HTS_comparison21
    
2. PMTCT_comparison21

 <h3>II. Data Acquisition Process</h3>


-Data Gathering: Gathering data from the source systems was the first phase in the data acquisition process. The information was accessed by an allowed user in the Health System who is allowed access to the systems and shared to us in form of an excel format.

-Data Extraction: After the data had been shared with us we gathered it by downloading it to our machines. To make using the data during the data analysis process easier, the data was exported to pandas dataframe .

-Data Cleaning: To make sure the data was of the highest quality and prepared for analysis, the data underwent cleaning before being loaded into the working environment using pandas. Checking the data for duplicates, missing numbers, and inconsistencies was part of the cleaning procedure.

-Data Loading: Following data cleansing, pandas was used to load the data into the working environment. Data frames, a type of pandas data structure that facilitates effective data manipulation and analysis, were used to load the data.

-Data Preparation: The data was further prepared for analysis after it had been imported into the data frames. This required changing column names, eliminating extra columns, and converting the data's data types.

-Data Analysis: When the data had been loaded and formatted, data analysis was the following stage in order to find trends, patterns, and insights. Data visualization, machine learning, and statistical methodologies were all used to accomplish this.

</details>

<details>

<summary><h2>Exploratory Data Analysis</h2></summary>
    
   <h3>I. Introduction</h3>

- Explanation of EDA and its purpose in this project
- The main variable of interest in the data


 <h3>II. EDA Techniques Used</h3>

- Description of the exploratory visualizations used to analyze which facilities do not report their PMTCT tests
- Explanation of data cleaning and preprocessing
- Identification of patterns and relationships
 
 <h3>III. Results of EDA </h3>

- Calculation of errors between DHIS and DATIM data
- Visualizations such as lineplots to examine the number of DHIS and DATIM records of the HTS and PMTCT data reported from different facilities
- Feature selection used to train the model

<h3>IV. Conclusion</h3>

- Outcome of EDA and its usefulness in understanding the data
- Importance of EDA in the development of the classification model

</details>

<details>
    
<summary><h2> Data Cleaning </h2></summary>

   <h3>I. Data Cleaning Process</h3>

1. Identifying and removing null values

2. Extracting data merged in one column

3. Dataset visualizations to identify the relationships between the columns. 

outcomes of the data cleaning process included:
- Acquiring a dataset whose values are distinct per column
- Converting excel files into CSV for easier data manipulation
- Improved data quality by removing errors, inconsistencies, and irrelevant data

<h3>II. Conclusion</h3>
Summarize the importance of data cleaning in ensuring high quality data for analysis and modeling purposes.

</details>

<details>

<summary><h2> Feature Engineering </h2></summary>

<h3>I. Feature Engineering Process </h3>

- Data cleaning and transformation
- Extracting the age and gender data from the Indicator column
- Grouping data according to the facility ID and Period
- Calculating errors and percentage errors between DHIS and DATIM records per facility in HTS data
- Generating the target variable based on the percetage error between DHIS and DATIM records per facility in HTS data

 <h3>II. Features Used</h3>

The dependent variables are:

- 'period'
- 'total_dhis2_value_hts'
- 'total_datim_value_hts'
- 'percentage_difference_hts'
- 'total_dhis2_value_pmtct'
- 'total_datim_value_pmtct’

The target variable is ‘accept’ 

  <h3>III. Conclusion</h3>

- Summary of feature engineering process and features used
- Importance of feature engineering in training classification models

</details>


<details>
  <summary><h2>Model Development</h2></summary>
  
  <h3>I. Model Development</h3>
The project uses a supervised learning approach for model development by providing the machine with labeled data(input data and required output). The computer then learns a model from this data, which can be used to map new input data to the desired output. The model can also classify data into different categories and make predictions on unseen data.

  <h3>II. Justification for Model Used</h3>

The supervised learning ensures accuracy and reliability since the computer is given both the input data and the corresponding desired output. For the model creation, the output is a binary classification model predicting either “yes” or “no”  using the target variable “accept”. The selected machine learning algorithm was the Decision Tree classifier because we are trying to classify between two outputs. We used the sklearn library.

</details>

<details>
  <summary><h2>Model Evaluation</h2></summary>
-The metric used was F1 score which combines precision and recall into a single score to assess the overall performance of the model. It takes into account both precision and recall to give an overall measure of how well the model is performing. Higher F1-score indicates better overall performance of the model.


<h3>I. Results from Different Metric</h3>
    
The model’s training accuracy was 95% which when compared to the y_test dataset, most were a match. The F1 score which was 0.98. This means that the model was good.
    
<h3>II. Justification for Metric Used</h3>
    
   The F1 score combines precision and recall into a single score to assess the overall performance of the model. Higher F1-score indicates better overall performance of the model. It is also used to check if our model is overfitting

</details>
    
<details>
  <summary><h2>Model Deployment</h2></summary>

   <h3>Justification for Deployment method used</h3>
    The following are a number of reasons why we decided to use Microsoft Azure for deployment of our model:
 
  1. Scalable - scale up or scale down of the model proved to be really simple with Azure
  2. Azure provides very useful tools and platforms which are very useful for machine learning workflows
  3. Security - Azure provides a rnage sepreme tools for securing machine learning models which is very valuable for our case.

    The following is the process we used to deploy our machine learning:
     - Prepared the model - this involved saving the model into a pickel file  so that it can be loaded and executed by a web service.
     - Created an azure virtual machine learning workspace - this was to be used to store the model and all related files.
     - Created a scoring script - this was needed to run and load our model, process input data to generate predictions.
     - Built a docker image that included our model, scoring script and any other necessary dependencies.
     - Deployed the model - we deployed the docker image to the deployment target.
     - Tested the deployment to ensure it was working correctly.


</details>
  
<details>
  <summary><h2>Challenges</h2></summary>
Some of the challenges we faced are:
    
1. Unbalanced distribution of PMTCT sites: It's likely that there are far less PMTCT sites than there are sites that report testing. This might lead to a class imbalance issue, in which case our machine learning model might be biased towards the majority class and perform poorly while looking for sites that don't disclose tests.
2. Generalizability: A machine learning model may or may not generalize well to fresh, untried data, even if it performs well on our training data. To make sure that our model is not overfitting to our training data, we must carefully assess its performance on a holdout set of data.

</details>




