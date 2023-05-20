import streamlit as st
import pandas as pd
import geopandas as gd
from libraries import (
    check_positions,
    create_dict,
    create_chart_from_dict,
    create_donut,
    create_map_data,
    create_map,
)
from plotly.subplots import make_subplots

vietnam = gd.read_file("vietnamHigh.json")

vietnam["name"] = vietnam["name"].replace(
    {
        "Bà Rịa–Vũng Tàu": "Bà Rịa - Vũng Tàu",
        "Hòa Bình": "Hoà Bình",
        "Khánh Hòa": "Khánh Hoà",
        "Hồ Chí Minh": "TP. Hồ Chí Minh",
        "Thanh Hóa": "Thanh Hoá",
        "Thừa Thiên–Huế": "Thừa Thiên - Huế",
    }
)

vietnam.head()


def main():
    st.set_page_config(page_title="Data Insights", page_icon="🖖", layout="wide")
    st.markdown(
        "<style> @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap'); .css-18e3th9, .stApp, .css-fg4pbf, .streamlit-wide, .eczokvf0 { padding-top: 1em; padding-left: 2em; padding-right: 2em; font-family: Inter } h1, .st-ae {font-family: Inter}</style> ",
        unsafe_allow_html=True,
    )

    # st.markdown('<style> </style>')
    st.title("Data-related Positions Insights")
    technology_list = [
        "python",
        "sql",
        " r ",
        "sas",
        "javascript",
        "matlab",
        "html",
        "php",
        " c ",
        "scala",
        "perl",
        "shell",
        "java",
        "c#",
    ]
    operation_list = [
        "tableau",
        "looker",
        "power bi",
        "aws",
        "azure",
        "git",
        "jira",
        "jenkins",
        "sap",
        "mlflow",
        "kubernetes",
        "kubeflow",
        "airflow",
        "excel",
        "kafka",
        "hadoop",
        "amazon",
    ]
    package_list = [
        "matplotlib",
        "spark",
        "plotly",
        "pandas",
        "tensorflow",
        "numpy",
        "pytorch",
        "keras",
        "ggplot",
        "opencv",
        "nltk",
        "statsmodels",
        "tidyverse",
    ]
    edu_level = ["phd", "master", "bachelor", "msc"]

    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        query = st.selectbox(
            "Select Role:",
            [
                "Data Analyst",
                "Data Scientist",
                "Data Engineer",
                "Machine Learning Engineer",
            ],
        )
    data = pd.read_csv("new_df.csv")

    def plot_charts(df, query):
        title_df = df[df.title.str.find(query) != -1]
        title_df = title_df.reset_index(drop=True)
        title = title_df.copy()
        title = check_positions(title, technology_list, operation_list, package_list)
        tech, operation, package = create_dict(title)
        tech_fig = create_chart_from_dict(tech, title)
        op_fig = create_chart_from_dict(operation, title)
        pack_fig = create_chart_from_dict(package, title)
        donut = create_donut(title, edu_level)
        map_fig = create_map(create_map_data(df))
        with col2:
            st.write(donut)
            st.write(op_fig)
        with col3:
            st.write(pack_fig)
            st.write(tech_fig)
        with col4:
            st.write(map_fig)

    if query == "Data Analyst":
        plot_charts(data, "Data Analyst")
    elif query == "Data Scientist":
        plot_charts(data, "Data Scientist")
    elif query == "Data Engineer":
        plot_charts(data, "Data Engineer")
    else:
        plot_charts(data, "Machine Learning Engineer")


if __name__ == "__main__":
    main()
