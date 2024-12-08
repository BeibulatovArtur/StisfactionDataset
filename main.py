import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv('customer_feedback_satisfaction.csv')
st.write('Data')
st.write(data)
st.write('Base stastistics')
st.write(data.describe())
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns[:10]
categorical_columns = data.select_dtypes(include=['object']).columns[:10]
cleaned_data = data.dropna()
cleaned_data.info()

plt.figure(figsize=(8,5))
plot1= sns.histplot(cleaned_data[numerical_columns[-1]],bins=25)
st.text('Satisfaction score distribution')
st.pyplot(plot1.get_figure())
plt.title(f'Satisfaction score distribution')

plt.figure(figsize=(8,5))
plot3 = sns.barplot(cleaned_data,x='Country',y='SatisfactionScore',hue='Gender')
st.pyplot(plot3.get_figure())

fig1 = plt.figure(figsize=(8, 5))
plt.title('Loyalty levels destribution')
loyalty_levels = []
for loyalty in cleaned_data['LoyaltyLevel'].unique():
    loyalty_levels.append(cleaned_data[cleaned_data['LoyaltyLevel'] == f'{loyalty}'].shape[0])
plt.pie(loyalty_levels,labels=cleaned_data['LoyaltyLevel'].unique(),autopct='%1.1f%%')
plt.show()
st.pyplot(fig1)
fig2 = plt.figure(figsize=(8, 5))

feedback_score = []
plt.title('Feedback score destribution')
for feedback in cleaned_data['FeedbackScore'].unique():
    feedback_score.append(cleaned_data[cleaned_data['FeedbackScore'] == f'{feedback}'].shape[0])
plt.pie(loyalty_levels,labels=cleaned_data['FeedbackScore'].unique(),colors=['tomato', 'cornflowerblue', 'gold'],autopct='%1.1f%%')
plt.show()
st.pyplot(fig2)

st.text('Satisfaction destribution with age')
sorted_by_age = cleaned_data.sort_values(by='Age')
fig4= plt.figure(figsize=(12,7))
sns.barplot(x=sorted_by_age['Age'],y=sorted_by_age['SatisfactionScore'],)
st.pyplot(fig4)

st.write('Transformed data with new columns')
countries_list = cleaned_data['Country'].unique()
def data_transformation(cleaned_data):
    transformed_data = cleaned_data
    transformed_data['Gender']= transformed_data['Gender'].map(lambda x: True if x=='Male' else False)
    for country in cleaned_data['Country'].unique():
        transformed_data.insert(5,f'Country_{country}',transformed_data['Country'].map(lambda x: True if x==f'{country}' else False))
    transformed_data = transformed_data.drop('Country',axis=1)
    for feedback in cleaned_data['FeedbackScore'].unique():
        transformed_data.insert(9,f'FeedbackScore_{feedback}',transformed_data['FeedbackScore'].map(lambda x: True if x==f'{feedback}' else False))
    transformed_data = transformed_data.drop('FeedbackScore',axis=1)
    for loyalty in cleaned_data['LoyaltyLevel'].unique():
        transformed_data.insert(12,f'LoyaltyLevel_{loyalty}',transformed_data['LoyaltyLevel'].map(lambda x: True if x==f'{loyalty}' else False))
    transformed_data = transformed_data.drop('LoyaltyLevel',axis=1)
    transformed_data['CombinedQuality'] = (transformed_data['ProductQuality']+transformed_data['ServiceQuality'])/2
    transformed_data['SatisfactionPerUnitsOfQuality'] = transformed_data['SatisfactionScore']/transformed_data['CombinedQuality']
    return transformed_data
transformed_data = data_transformation(cleaned_data)
transformed_data
fig5 = plt.figure(figsize=(15,10))
corr = transformed_data.corr()
st.text('Correlation Matrix')
sns.heatmap(corr,annot=True,fmt='.2f')
st.pyplot(fig5)

st.text('Comparing 3d plots for differnt countries with x-Satisfaction Score, y-Age and z - Income')
fig6 = plt.figure(figsize=(60,40))
i = 0
for country in countries_list:
    i+=1
    ax = fig6.add_subplot(2,3,i,projection='3d')
    plt.title(country)
    country_data = transformed_data[transformed_data[f'Country_{country}']==True]
    country_data.drop(columns=country_data.columns[4:10],inplace=True)
    ax.scatter(country_data['SatisfactionPerUnitsOfQuality'],country_data['Age'],country_data['Income'])
    #corrx = country_data.corr()
    #sns.heatmap(corrx,annot=True,fmt='.2f')
    ax.set_xlabel('SatisfactionPerUnitsOfQuality')
    ax.set_ylabel('Age')
    ax.set_zlabel('Income')
st.pyplot(fig6)

with st.form('Add information') as form:
    i = st.slider('Income',min_value=transformed_data['Income'].min(),max_value=transformed_data['Income'].max())
    a = st.slider('Age',min_value=transformed_data['Age'].min(),max_value=transformed_data['Age'].max())
    l = st.selectbox('Loyalty level',cleaned_data['LoyaltyLevel'].unique())
    f = st.selectbox('Feedback Score',cleaned_data['FeedbackScore'].unique())
    c = st.selectbox('Country',cleaned_data['Country'].unique())
    g = st.selectbox('Gender',('Male','Female'))
    s = st.slider('Satisfaction Score',min_value=0.0,max_value=transformed_data['SatisfactionScore'].max())
    q1 = st.slider('Product Quality',min_value=0,max_value=10)
    q2 = st.slider('Service Quality',min_value=0,max_value=10)
    sb = st.form_submit_button(label='Add')
#if sb:
    
