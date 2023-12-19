import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('dataset_part_2.csv')

app = dash.Dash(__name__)


def display():
    # transform some relevant data for plotting
    data['Class_str'] = data['Class'].apply(lambda x: "Success" if x == 1 else "Failure")
    Success_rate_orbit = data.groupby('Orbit')[['Class']].mean().reset_index()
    data['Year'] = data['Date'].str[:4].astype(int)
    Success_rate_Y = data.groupby('Year')[['Class']].sum().reset_index()
    
    plot_obj = [
        px.scatter(data, 
            x='FlightNumber',
            y='LaunchSite',
            symbol='Class_str',
            color='Class_str',
            color_continuous_scale='RdBu',
            title="LaunchSite and FlightNumber"
        ).update_traces(marker_size=10),

        px.scatter(data, 
            x='PayloadMass',
            y='LaunchSite',
            symbol='Class_str',
            color='Class_str',
            color_continuous_scale='RdBu',
            title="Between Payload Mass and Launch Site"
        ).update_traces(marker_size=10),
        
        px.bar(Success_rate_orbit, 
            x='Orbit',
            y='Class',
            # symbol='Class_str',
            color_continuous_scale='RdBu',
            title="Success Rate of Each Orbit Type."
        ).update_layout(yaxis_title="Success Rate"),
        
        px.scatter(data, 
            x='FlightNumber',
            y='Orbit',
            # symbol='Class_str'
            color='Class_str',
            color_continuous_scale='RdBu',
            title="Flight Number by Orbit Type."
        ).update_traces(marker_size=10),
        
        px.scatter(data, 
            x='PayloadMass',
            y='Orbit',
            # symbol='Class_str'
            color='Class_str',
            color_continuous_scale='RdBu',
            title="Payload Mass Each Orbit Type."
        ).update_traces(marker_size=10),
        
        px.line(Success_rate_Y, 
            x='Year',
            y='Class',
            title="Number of Successful Missions Over Year."
        ).update_layout(yaxis_title="Number of successful"),
    ]
    
    charts = [dcc.Graph(figure=plot_obj) for plot_obj in plot_obj]

    return (
        html.Div(
            className='chart-item',
            children=[html.Div(children=chart, style={'width':'auto'}) for chart in charts],
            style={  
                'display': 'flex',
                'justify-content': 'flex-center',
                'allign-content': 'stretch',
                'flex-wrap': 'wrap',
                'margin-top': 'calc(-1 * var(--bs-gutter-y))',
                'margin-right': 'calc(-.5 * var(--bs-gutter-x))',
                'margin-left': 'calc(-.5 * var(--bs-gutter-x))',
            }
        )
    )


app.layout = html.Div([
    html.H1(
        "SpaceY Mission Dashboard.",
        style={
            'textAlign': 'center',
            'color': '#503D36', 
            'font-size': 28
        }),

    html.Div(
        id='output-container1',
        children=display(),
        className='chart-grid', 
        style={
            'overflow-x': 'hidden',
            'width': '100%',
            'padding-right': 'calc(var(--bs-gutter-x) * .5)',
            'padding-left': 'calc(var(--bs-gutter-x) * .5)',
            'margin-right': 'auto',
            'margin-left': 'auto',
        }
    )
])


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)