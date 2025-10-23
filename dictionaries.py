
import os
from dotenv import load_dotenv
import pandas as pd


dict_mobile = {
  "pct_Males_ACS_17_21" : 'Percentage of men in the population',
  "pct_Hispanic_ACS_17_21" : 'Percentage of hispanics in the population',
  "pct_NH_White_alone_ACS_17_21" : 'Percentage of non-hispanic White people in the population',
  "pct_NH_Blk_alone_ACS_17_21" : 'Percentage of non-hispanic Black or African American people in the population',
  "pct_NH_AIAN_alone_ACS_17_21" : 'Percentage of non-hispanic American Indian and Alaska Native people in the population',
  "pct_NH_Asian_alone_ACS_17_21" : 'Percentage of non-hispanic Asian people in the population',
  "pct_NH_NHOPI_alone_ACS_17_21" : 'Percentage of non-hispanic Native Hawaiian and Other Pacific Islander people in the population',
  "pct_NH_Multi_Races_ACS_17_21" : 'Percentage of non-hispanic Mixed Race people in the population',
  "pct_Othr_Lang_ACS_17_21" : 'Percentage of people speaking a language other than English in the population',
  "Median_Age_ACS_17_21" : 'Median age of the population',
   "pct_Pop_18_24_ACS_17_21" : 'Percentage of people aged 18 to 24 in the population',
   "pct_Pop_25_44_ACS_17_21" : 'Percentage of people aged 25 to 44 in the population',
   "pct_Pop_45_64_ACS_17_21" : 'Percentage of people aged 45 to 64 in the population',
  "pct_Not_HS_Grad_ACS_17_21" : 'Percentage of the population without a high school diploma',
  "pct_College_ACS_17_21" : 'Percentage of the population without a college degree',
   "pct_Prs_Blw_Pov_Lev_ACS_17_21" : 'Percentage of the population below the poverty level',
 "pct_PUB_ASST_INC_ACS_17_21" : 'Percentage of the population receiving public assistance income',
 "Med_HHD_Inc_BG_ACS_17_21" : 'Median household income',
 "Aggregate_HH_INC_ACS_17_21" : 'Aggregate household income',
 "pct_Rel_Family_HHD_ACS_17_21" : 'Percentage of households with living relatives',
 "pct_MrdCple_HHD_ACS_17_21" : 'Percentage of married-couple households',
  "pct_HHD_PPL_Und_18_ACS_17_21" : 'Percentage of households with people under 18 years old',
  "avg_Tot_Prns_in_HHD_ACS_17_21" : 'Average household size',
   "pct_Tot_Occp_Units_ACS_17_21" : 'Percentage of total occupied housing units',
 "pct_Occp_U_NO_PH_SRVC_ACS_17_21" : 'Percentage of housing units without telephone service in the ACS',
 "pct_URBAN_POP_CEN_2020" : 'Percentage of the population living in urban areas',
   "pop_density" : 'Population density (people per square mile)',
 "phone_response_rate_cen_2020" : 'Percentage of households that responded to the census via phone'
  }


dict_food = {'order_id':'Unique ID of the order',
             'customer_id': 'ID of the customer who ordered the food',
             'restaurant_name':'Name of the restaurant',
             'cuisine_type':'Cuisine ordered by the customer',
             'cost_of_the_order':'Cost of the order',
             'day_of_the_week':'Indicates whether the order is placed on a weekday or weekend (The weekday is from Monday to Friday and the weekend is Saturday and Sunday)',
             'rating':'Rating given by the customer out of 5',
            'food_preparation_time':': Time (in minutes) taken by the restaurant to prepare the food. This is calculated by taking the difference between the timestamps of the order confirmation and the pick-up confirmation.',
            'delivery_time':'Time (in minutes) taken by the delivery person to deliver the food package. This is calculated by taking the difference between the timestamps of the pick-up confirmation and drop-off information'
            }

dict_conv = {'ID': 'ID of the lead',
             'age': 'Age of the lead',
             'current_occupation': 'Current occupation of the lead. Values include Professional,Unemployed, and Student',
             'first_interaction': 'How did the lead first interacted with Coeus. Values include Website, and Mobile App',
             'profile_completed': 'What percentage of profile has been filled by the lead on the website or mobile app. Values include Low: 0-50%, Medium: 50-75%, and High: 75-100%',
             'website_visits': 'How many times has a lead visited the website',
             'time_spent_on_website': 'Total time spent on the website',
             'page_views_per_visit': 'Average number of pages on the website viewed during the visits',
             'last_activity': 'Last interaction between the lead and Coeus',
             'Email Activity': 'Seeking for details about program through email, Representative shared information with lead like brochure of program , etc.',
             'Phone Activity': 'Had a Phone Conversation with representative, Had conversation over SMS with representative, etc.',
             'Website Activity': 'Interacted on live chat with representative, Updated profile on website, etc.',
             'print_media_type1': 'Flag indicating whether the lead had seen the ad of Coeus in the Newspaper',
             'print_media_type2': 'Flag indicating whether the lead had seen the ad of Coeus in the Magazine',
             'digital_media': 'Flag indicating whether the lead had seen the ad of Coeus on the digital platforms',
             'educational_channels': 'Flag indicating whether the lead had heard about Coeus in the education channels like online forums, discussion threads, educational websites, etc.',
             'referral': 'Flag indicating whether the lead had heard about Coeus through reference',
             'status': 'Flag indicating whether the lead was converted to a paid customer or not'}


def load_column_dict(file_name: str) -> str:
    
    res_str= ''
    if file_name=='Food Delivery':
        res_str = str(dict_food)
    elif file_name=='Customer Conversion':
        res_str = str(dict_conv)
    elif file_name=='Mobile Coverage':
        res_str = str(dict_mobile)
    
    return res_str