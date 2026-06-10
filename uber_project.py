import pandas as pd
import plotly.express as px

path = '/Users/luanabreno/Desktop/UBER - PROJECT/datasets/'

uber_15 = pd.read_csv(path + 'uber-raw-data-janjune-15_sample.csv')

print(uber_15.info())
print(uber_15.head().to_string())

#Duplicated values
#print(uber_15.duplicated().sum())
uber_15.drop_duplicates(inplace=True)
#print(uber_15.isnull().sum())
uber_15['Pickup_date'] = pd.to_datetime(uber_15['Pickup_date'])
print(uber_15.dtypes)

uber_15['month'] = uber_15['Pickup_date'].dt.month_name()
uber_15['weekday'] = uber_15['Pickup_date'].dt.day_name()
uber_15['day'] = uber_15['Pickup_date'].dt.day
uber_15['hour'] = uber_15['Pickup_date'].dt.hour
uber_15['minute'] = uber_15['Pickup_date'].dt.minute

print(uber_15['month'].value_counts())
"""
month
June        19620
May         18660
April       15982
March       15969
February    15896
January     13819
"""

pivot = pd.crosstab(uber_15['month'], uber_15['weekday'])
month_order = ['January', 'February', 'March', 'April', 'May', 'June']
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_sorted = pivot.reindex(index=month_order, columns=weekday_order)
print(pivot_sorted)

fig = px.bar(pivot_sorted,
       x=pivot_sorted.index,
       y=pivot_sorted.columns,
       barmode='group',
       title='Uber Pickups by Month & Weekday')
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Number of Pickups',
    legend_title='Weekday'
)
#fig.show()

rush_hours = uber_15.groupby(['weekday', 'hour'], as_index=False).size()
rush_hours['weekday'] = pd.Categorical(rush_hours['weekday'], categories = weekday_order, ordered=True)
print(rush_hours.sort_values(by=['weekday', 'hour']))

fig2 = px.line(
    rush_hours,
    x='hour',
    y='size',
    color='weekday',
    markers=True,
    title = 'Hourly Uber Rush by days'
)
fig2.update_layout(
    xaxis_title='Hour',
    yaxis_title='Number of Pickups',
    legend_title='Weekday',
    template='plotly_white'
)
#fig2.show()

#Pareto Analysis
base_df = uber_15['Dispatching_base_num'].value_counts(normalize=True).reset_index()
base_df.columns = ['Base', 'Percent']
base_df['Run.Percent'] = base_df['Percent'].cumsum()
print(base_df)

import plotly.graph_objs as go

pareto = go.Figure([
    go.Bar(x = base_df['Base'],
                y = base_df['Percent'],
                name = 'Trips'),
    go.Scatter(x = base_df['Base'],
               y= base_df['Run.Percent'],
               yaxis='y2',
               mode='lines+markers',
               name= 'Cumulative %')
])
pareto = pareto.update_layout(yaxis2 = dict(overlaying = 'y',
                                   side = 'right',
                                   tickformat = '.0%',
                                   range = [0,1] ))
pareto = pareto.add_hline(y = 0.8, yref = 'y2', line_dash = 'dash')

#pareto.show()

airport_ids = [1, 132, 138]
airport = uber_15[uber_15['locationID'].isin(airport_ids)].copy()
airport['name'] = airport['locationID'].map({
    1: 'EWR',
    132: 'JFK',
    138: 'LGA'
})
airport_hours = airport.groupby(['name', 'hour']).size().reset_index(name='trips')
print(airport_hours)

fig3 = px.area(
    airport_hours,
    x = 'hour',
    y = 'trips',
    color = 'name',
    title = 'Airport Demand Pressure'
)
fig3.update_layout(
    xaxis_title='Hour',
    yaxis_title='Number of Pickups',
)

#fig3.show()



