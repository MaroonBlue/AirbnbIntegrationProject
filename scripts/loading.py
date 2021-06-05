# %%
"""
### Loading data from csv to database
"""

# %%
import numpy as np
import pandas as pd
import pyodbc
import os


# %%
data = pd.read_csv (f'../data/airbnb_csv/Barcelona, Catalonia, Spain.csv')
city_df = pd.DataFrame(data)
df=pd.DataFrame(columns=city_df.columns)

# %%
for file in os.listdir('../data/airbnb_csv'):
    string=file.split(".")[0]
    string_split=string.split(", ")  

    data = pd.read_csv(f'../data/airbnb_csv/{file}')
    city_df = pd.DataFrame(data)
    city_df['city']=string_split[0]
    city_df['region']=string_split[1]
    city_df['country']=string_split[2]
    df=pd.concat([df, city_df], axis=0)


# %%
df_copy=df.copy()


"""
### INSERT DATA
"""


# %%
df = df.loc[:,['id','scrape_id','last_scraped','name',
'host_id','host_name','host_since','host_response_time','host_response_rate','host_acceptance_rate','host_is_superhost',
'host_listings_count','host_has_profile_pic','host_identity_verified','latitude','longitude','property_type','room_type','accommodates',
'bathrooms_text','bedrooms','beds','amenities','price','minimum_nights','maximum_nights',
'availability_365','number_of_reviews','first_review','last_review',
        'review_scores_rating', 'review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location',
       'review_scores_value',
'instant_bookable','reviews_per_month', 'city', 'region', 'country']]


# %%
cols_missing=['review_scores_rating', 'review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location',
       'review_scores_value','bedrooms', 'beds','bathrooms_text', 'host_listings_count', 'name', 'first_review', 'last_review']
df = df.dropna(subset=cols_missing).reset_index(drop=True)

# %%
# usuniecie $ i konwersja price na typ numeryczny
df['price'] = df['price'].apply(lambda x: x[1:].replace(',','')).astype(float)

# %%
# usuniecie ; z nazwy
df['name'] = df['name'].apply(lambda x: x.replace(';',':'))

# %%
# bathrooms
df['bathrooms_type'] = 'private'
df['bathrooms'] = 0.0
for i, val in df.iterrows():
    if ('shared' in df.iat[i,19]) or ('Shared' in df.iat[i,19]):
        df.iat[i,42] = 'shared'
    if ('half-bath' in df.iat[i,19]) or ('Half-bath' in df.iat[i,19]):
        df.iat[i,43] = 0.5
    first_word = df.iat[i,19].split(' ', 1)[0]
    if len(first_word) <= 4:
        df.iat[i,43] = float(first_word)
df['bathrooms_text'] = df['bathrooms_type']

# %%
df = df.drop('bathrooms_type', axis=1).rename(columns={'bathrooms_text':'bathrooms_type'})

# %%
# beds
df['bedrooms'] = df.bedrooms.astype(int)
df['beds'] = df.beds.astype(int)


"""
## Conversion
"""

# %%
date_cols=['last_scraped', 'first_review','last_review', 'host_since']
for col in date_cols:
    df[col]=pd.to_datetime(df[col])

# %%
int_cols=['id', 'host_id', 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
          'review_scores_communication', 'review_scores_location', 'review_scores_value', 'host_listings_count',
         'minimum_nights', 'maximum_nights', 'accommodates', 'availability_365', 'number_of_reviews', ]

# %%
for col in int_cols:
    df[col]=df[col].astype(int)


# %%
df.to_csv('../data/airbnb_data.csv', sep=';', index=False)


