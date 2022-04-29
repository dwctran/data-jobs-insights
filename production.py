import streamlit as st
import pandas as pd
from libraries import check_positions, create_dict, create_chart_from_dict, create_donut, create_map_data, create_map
from plotly.subplots import make_subplots

def main():
    st.set_page_config(page_title='Data Insights', page_icon='🖖', layout="wide")
    st.markdown('<style> .css-18e3th9, .stApp, .css-fg4pbf, .streamlit-wide, .eczokvf0 { padding-top: 1em; padding-left: 2em; padding-right: 2em; font-family: Inter } h1, .st-ae {font-family: Inter}</style> ', unsafe_allow_html=True)
                                                
    # st.markdown('<style> </style>')
    st.title('Data-related Positions Insights')
    new_df = pd.read_csv('new_df.csv')
    technology_list = ['python', 'sql', ' r ', 'sas', 'javascript', 'matlab', 'html', 'php', ' c ', 
                   'scala', 'perl', 'shell', 'java', 'c#']
    operation_list = ['tableau', 'looker', 'power bi', 'aws', 'azure', 'git', 'jira', 'jenkins', 
                  'sap', 'mlflow', 'kubernetes', 'kubeflow', 'airflow', 'excel', 'kafka', 
                  'hadoop', 'amazon']
    package_list = ['matplotlib', 'spark', 'plotly', 'pandas', 'tensorflow', 'numpy', 'pytorch', 
                'keras', 'ggplot', 'opencv', 'nltk', 'statsmodels', 'tidyverse']
    edu_level = ['phd', 'master', 'bachelor', 'msc']
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        query = st.selectbox('Select Role:', ['Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer'])
    def plot_charts(new_df, query):
        title_df = new_df[new_df.title.str.find(query) != -1]
        title_df = title_df.reset_index(drop = True)
        title = title_df.copy()
        title = check_positions(title, technology_list, operation_list, package_list)
        tech, operation, package = create_dict(title)
        tech_fig = create_chart_from_dict(tech, title)
        op_fig = create_chart_from_dict(operation, title)
        pack_fig = create_chart_from_dict(package, title)
        donut = create_donut(title, edu_level)
        map_fig = create_map(create_map_data(new_df))
        with col2: 
            st.write(donut)
            st.write(op_fig)
        with col3:
            st.write(pack_fig)
            st.write(tech_fig)
        with col4:
            st.write(map_fig)
    if query == 'Data Analyst':
        plot_charts(new_df, 'Data Analyst')
    elif query == 'Data Scientist':
        plot_charts(new_df, 'Data Scientist')
    elif query == 'Data Engineer':
        plot_charts(new_df, 'Data Engineer')
    else:
        plot_charts(new_df, 'Machine Learning Engineer')
   

if __name__ == '__main__':
    main()


