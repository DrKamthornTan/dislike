import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import numpy as np

# Read the CSV file
data = pd.read_csv('data0.csv')

# Convert the event_date column to datetime
data['event_date'] = pd.to_datetime(data['event_date'], format="%Y%m%d").dt.strftime('%Y-%m-%d')

# Filter data for is_active_user = 1 and = 0
active_user_data = data[data['is_active_user'] == 1]
inactive_user_data = data[data['is_active_user'] == 0]

# Create Dash app
app = dash.Dash(__name__)

# Set up the layout of the app
app.layout = html.Div([
    html.H1("Likelihood Distance Scatterplot", style={'textAlign': 'center'}),
    dcc.Graph(
        id='scatter-plot',
    )
])

# Callback to update the scatter plot
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('scatter-plot', 'relayoutData')]
)
def update_scatter_plot(relayoutData):
    fig = px.scatter(active_user_data, x='event_date', y='event_previous_timestamp',
                     color_discrete_sequence=['blue'], hover_data=['user_id'],
                     labels={'event_date': 'Event Date', 'event_previous_timestamp': 'Previous Timestamp'},
                     title='ข้อมูล พค.-ธค. 2023 - is_active_user=1 จุดสีฟ้า')
    fig.add_trace(px.scatter(inactive_user_data, x='event_date', y='event_previous_timestamp',
                             color_discrete_sequence=['red'], hover_data=['user_id']).data[0])

    fig.update_layout(
        xaxis=dict(title='Event Date'),
        yaxis=dict(title='Previous Timestamp'),
        title_x=0.5
    )
    

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
