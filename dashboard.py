# imprt necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style = 'whitegrid')

# create necessary function

def day_count(DataFrame):
    # create a function to count the number of days
    return len(DataFrame['date'].unique())

def station_count(DataFrame):
    # create a function to count the number of stations
    return len(DataFrame['station'].unique())

def all_avg_score(DataFrame):
    # create a function to average the air quality score
    return round(DataFrame['air_quality_score'].mean(), 3)

def df_avg_by_station(DataFrame):
    # create dataframe group by station with mean aggregation
    temp = DataFrame.groupby(by='station', as_index=False).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "air_quality_score": "mean",
    }).sort_values('air_quality_score', ascending = False)

    return temp.iloc[:6]

def df_rev_avg_by_station(DataFrame):
    # create reverse dataframe group by station with mean aggregation
    temp = DataFrame.groupby(by='station', as_index=False).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "air_quality_score": "mean",
    }).sort_values('air_quality_score', ascending = True)

    return temp.iloc[:6]

def df_avg_by_station_year(DataFrame):
    # create mod_df group by station, year with mean aggregation
    temp = DataFrame.groupby(by=['station', 'year'], as_index=False).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "air_quality_score": "mean",
    }).sort_values(['year', 'air_quality_score'], ascending = [True, False])

    return temp

def df_avg_by_station_year_month(DataFrame):
    # create mod_df group by station, year with mean aggregation
    temp = DataFrame.groupby(by=['station', 'year', 'month'], as_index=False).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "air_quality_score": "mean",
    }).sort_values(['year', 'month', 'air_quality_score'], ascending = [True, True, False])

    # save the month-year as a single feature
    temp2 = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
    for i in range(len(temp)):
        mon = temp['month'].iloc[i]
        for j in range(1, len(months)+1):
            if mon == j:
                mon_as = months[j-1]
                break
        temp2.append(mon_as + ' ' + str(temp['year'].iloc[i]))
    temp['date_my'] = temp2

    return temp

def main():
    # header
    st.header('Analysing Air Quality by Irfan :cloud:')

    # initialize some variables
    df = pd.read_csv("main_data.csv")
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    min_date = df["date"].min()
    max_date = df["date"].max()
    station = df['station'].unique()

    with st.sidebar:
        # centered logo
        c1, c2, c3 = st.columns(3)
        with c2:
            # st.image(logo)
            st.image("https://media.discordapp.net/attachments/906940359077134377/1188165607582077058/image.png")

        # range of date
        try:
            start_date, end_date = st.date_input(
                label='Range of Date',
                min_value=min_date,
                max_value=max_date,
                value=[min_date, max_date],
                format="YYYY-MM-DD"
            )
        except:
            pass

        # stations selected
        options = st.multiselect(
            label='Selected Stations',
            options=station,
            default=station
        )

    # to handle the error
    try:
        # apply filter settings
        mod_df = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date)) & (df['station'].isin(options))]

        # create separate columns layout
        co1, co2, co3 = st.columns([2, 2, 2])
        with co1:
            st.metric("Number of Days", value=day_count(mod_df))
        with co2:
            st.metric("Number of Stations", value=station_count(mod_df))
        with co3:
            st.metric("Average Air Quality Score", value=all_avg_score(mod_df))
        
        # create the first and the second data visualization
        colors1 = ['#40923A', '#B3D495', '#B3D495', '#B3D495', '#B3D495', '#B3D495']
        colors2 = ['#CA3335', '#EFA6A5', '#EFA6A5', '#EFA6A5', '#EFA6A5', '#EFA6A5']
        col1, col2 = st.columns([2, 2])

        with col1:
            st.subheader('Best Avg Air Quality Score')
            fig, ax = plt.subplots(figsize=(3, 3))
            sns.barplot(x = 'air_quality_score',
                        y = 'station',
                        data = df_avg_by_station(mod_df),
                        orient = 'h',
                        palette = colors1)
            
            plt.xlabel('AQS (pts)\nhigher is better')
            st.pyplot(fig)

        with col2:
            st.subheader('Worst Avg Air Quality Score')
            fig, ax = plt.subplots(figsize=(3, 3))
            sns.barplot(x = 'air_quality_score',
                        y = 'station',
                        data = df_rev_avg_by_station(mod_df),
                        orient = 'h',
                        palette = colors2)
            
            plt.xlabel('AQS (pts)\nlower is inferior')
            st.pyplot(fig)
        
        # create the third data visualization
        temp = df_avg_by_station_year(mod_df)
        min_year = temp['year'].min()
        max_year = temp['year'].max()

        if min_year != max_year:
            st.divider()
            st.subheader(f'Average Air Quality Score, by Stations and Years ({min_year} - {max_year})')
            fig, ax = plt.subplots(figsize=(9, 5))
            sns.lineplot(data = temp,
                        x = 'year',
                        y = 'air_quality_score',
                        hue = 'station',
                        palette = 'Paired')
            
            plt.ylabel('AQS (pts)\nhigher is better')
            plt.xticks(mod_df['year'].unique())
            plt.legend(ncol = 3)
            st.pyplot(fig)

        # create the last data visualization
        temp = df_avg_by_station_year_month(mod_df)
        min_d = str(start_date).split('-')
        max_d = str(end_date).split('-')
        try:
            # eliminate zero as the first digit on month
            if min_d[1][0] == 0:
                min_d[1] = min_d[1][1]
            if max_d[1][0] == 0:
                max_d[1] = max_d[1][1]
        except:
            pass

        min_date = temp['date_my'].loc[(temp['year'] == int(min_d[0])) & (temp['month'] == int(min_d[1]))].unique()[0]
        max_date = temp['date_my'].loc[(temp['year'] == int(max_d[0])) & (temp['month'] == int(max_d[1]))].unique()[0]

        st.divider()
        st.subheader(f'Average Air Quality Score, by Stations, Years and Months ({min_date} - {max_date})')
        fig, ax = plt.subplots(figsize=(11, 6))
        sns.lineplot(data = temp,
                     x = 'date_my',
                     y = 'air_quality_score',
                     hue = 'station',
                     palette = 'Paired')

        plt.ylabel('AQS (pts)\nhigher is better')
        plt.xlabel('month year')
        plt.xticks(temp['date_my'].unique()[::3], rotation=45)
        plt.legend(ncol = 3)
        st.pyplot(fig)

        st.caption('*Copyright (c) Muhammad Irfan Arisani 2023*')
    
    except:
        pass

if __name__ == '__main__':
    main()