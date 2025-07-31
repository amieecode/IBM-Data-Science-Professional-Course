# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'site1', 'values': 'site1'},
                                             ],
                                             value='ALL',
                                             placeholder="Place holder here",
                                             searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                @app.callback(Output(component_id='success-pie-chart', components_property='figure'),
                                              Input(component_id='site-dropdown', components_property='value'))
                                def get_pie_chart(entered_site):
                                    filtered_df = spacex_df
                                    if entered_site == 'ALL':
                                        fig = px.pie(data, values='class',
                                        names='pie chart names',
                                        title='title')
                                        return fig
                                    else:
                                                                        # Filter dataframe for the selected launch site
                                        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

                                        # Count success and failure for the selected site
                                        success_fail_counts = filtered_df['class'].value_counts().reset_index()
                                        success_fail_counts.columns = ['class', 'count']
                                        success_fail_counts['class'] = success_fail_counts['class'].replace({1: 'Success', 0: 'Failure'})

                                        # Pie chart showing success vs failure for the selected site
                                        fig = px.pie(
                                            success_fail_counts, 
                                            names='class', 
                                            values='count',
                                            title=f'Success vs Failure Launches for site {entered_site}'
                                        )
                                        return fig

                                        html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_value, max_value])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
                                @app.callback(
                                    Output(component_id='success-payload-scatter-chart', component_property='figure'),
                                    [
                                        Input(component_id='site-dropdown', component_property='value'),
                                        Input(component_id='payload-slider', component_property='value')
                                    ]
                                )
                                def get_scatter_plot(entered_site, payload_range):
                                    low, high = payload_range

                                    # Filter by payload range first
                                    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                                                            (spacex_df['Payload Mass (kg)'] <= high)]

                                    if entered_site == 'ALL':
                                        # Scatter for all sites
                                        fig = px.scatter(
                                            filtered_df,
                                            x='Payload Mass (kg)',
                                            y='class',
                                            color='Booster Version Category',
                                            title='Correlation between Payload and Success for All Sites'
                                        )
                                    else:
                                        # Filter by site
                                        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
                                        fig = px.scatter(
                                            filtered_df,
                                            x='Payload Mass (kg)',
                                            y='class',
                                            color='Booster Version Category',
                                            title=f'Payload vs Outcome for site {entered_site}'
                                        )
                                    return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
