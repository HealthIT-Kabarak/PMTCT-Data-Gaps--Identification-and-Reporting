import pandas as pd
from sklearn import preprocessing
import pickle
import os


def read_file(file_path):
    file_ext = os.path.splitext(file_path)[-1].lower()
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext in [".xls",".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported")  

def file_merger(file_path):
    """Method to merge multiple files"""
    data_df = pd.DataFrame()
    for file_path in file_path:
        # read the file and append it to the DataFrame
        df = read_file(file_path)
        data_df.append(df, ignore_index=True)
    return data_df

def clean_csv(data):
    df = data
    numerical_defaults = {'int64': 0, 'float64': 0.0}
    # replace missing values with defaults
    for col in df.columns:
        if df[col].dtype in numerical_defaults.keys():
            # replace null values with the default value for the datatatype
            df[col].fillna(numerical_defaults[df[col].dtype], inplace=True)

    # drop all null values
    try:
        df = df.dropna(how='any')
    except:
        raise Exception

    # with the column, extract gender, age bracket
    if 'Indicator Name' in df.columns:
        df[['gender']] = df['Indicator Name'].str.extract(r'(\(F\)|\(M\))')
        # extract age
        df[['age']] = df['Indicator Name'].str.extract(r'(?P<age><1|1-9|10-14|15-19|20-24|25\+)')
        # drop indicator column
        df = df.drop(columns=['Indicator Name'])
    else:
        print('No such Column named Indicator Name')
        return df
    return df

def hts_cleaner(df):
    # group values
    suffix = 'hts'
    df = df.groupby(['facilityuid', 'period']).agg({'dhis2_value': 'sum', 'datim_value': 'sum'})
    df = df.reset_index() # reset index
    # rename columns
    df = df.rename(columns={'dhis2_value': f'total_dhis2_value_{suffix}', 'datim_value': f'total_datim_value_{suffix}'})
    #calculate  diff
    df[f'difference_{suffix}'] = df[f'total_dhis2_value_{suffix}'] - df[f'total_datim_value_{suffix}']
    df[f'percentage_difference_{suffix}'] = abs(df[f'difference_{suffix}'] / df[f'total_datim_value_{suffix}'] * 100)
    
    hts_df = df
    return hts_df

def pmtct_cleaner(df):
    # group values
    suffix = 'pmtct'
    df = df.groupby(['facilityuid', 'period']).agg({'dhis2_value': 'sum', 'datim_value': 'sum'})
    df = df.reset_index() # reset index
    # rename columns
    df = df.rename(columns={'dhis2_value': f'total_dhis2_value_{suffix}', 'datim_value': f'total_datim_value_{suffix}'})
    #calculate  diff
    df[f'difference_{suffix}'] = df[f'total_dhis2_value_{suffix}'] - df[f'total_datim_value_{suffix}']
    df[f'percentage_difference_{suffix}'] = abs(df[f'difference_{suffix}'] / df[f'total_datim_value_{suffix}'] * 100)
    
    pmtct_df = df
    return pmtct_df

def merge_hts_pmtct(pmtct_df, hts_df):
    # merge two dataframes
    merged_df = pd.merge(hts_df, pmtct_df, on=["facilityuid","period"])
    #calculate first cutoff
    cutoff = merged_df["percentage_difference_hts"].median()
    # define a lambda function with if-else conditions: yes if below cutoff, no if above
    merged_df['accept'] = merged_df['percentage_difference_hts'].apply(lambda x: 'yes' if x < cutoff else 'no')
    # set a 'no' based dataframe
    rejected = merged_df[merged_df['accept'] == 'no']
    return [rejected, merged_df]

def rejected_dataset(df_list):
    rejected = df_list[0]
    merged_df = df_list[1]
    # set new difference
    if (rejected['difference_hts'] < 0).any():
        rejected['new_difference'] = rejected['total_dhis2_value_pmtct'] + rejected['difference_hts']
    else:
        rejected['new_difference'] = rejected['total_datim_value_pmtct'] + rejected['difference_hts']

    rejected['new_percentage_difference']= abs(rejected['new_difference']/ rejected['total_datim_value_hts']* 100)
    # calc cut off
    cutoff = rejected["new_percentage_difference"].mean()
    # define a lambda function with if-else conditions
    rejected['new_accept'] = rejected['new_percentage_difference'].apply(lambda x: 'yes' if x < cutoff else 'no')
    rejected['accept'] = rejected['new_accept']
    # merged_df without the rejected
    merged_df = merged_df[merged_df['accept'] != 'no'].copy()
    # delete added columns in rejected
    rejected.drop(['new_difference','new_percentage_difference', 'new_accept'], axis=1, inplace=True)
    #merge two dataframes
    final_df = pd.concat([merged_df, rejected], axis=0)

    return final_df


def run_model(final_df):
    with open('./model.pkl', 'rb') as f:
        model = pickle.load(f)

        # Get the input data from the request
        input_data = final_df
        #converting categorical data to numerical data
        label_encoder = preprocessing.LabelEncoder()

        # Three columns have categorical text info, and we convert them to numbers
        final_df['accept'] = label_encoder.fit_transform(final_df['accept'])
        final_df['period'] = label_encoder.fit_transform(final_df['period'])
        final_df.reset_index(drop=True, inplace=True)

        # #converting facilityuid to index values
        # final_df.rename(columns={'index': 'facilityuid'}, inplace=True)
        # final_df


        # Make a prediction using the model
        prediction = model.predict([input_data])[0]

        # Format the prediction as a JSON response
        response = {'prediction': prediction}

        return  response







def export_file(data_frame):
    output_filename = f"cleaned_data.csv"
    data_frame.to_csv(output_filename, index=False)
    return output_filename