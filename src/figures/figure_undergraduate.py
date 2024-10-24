from pathlib import Path
import pandas as pd
import plotly.express as px

# Extract the data
data_path = Path(__file__).parent.parent.parent.joinpath("data", "df_prepared.csv")

data = pd.read_csv(data_path)


def bar_ethnicity(time_period):
    """
    Generates an interactive bar chart for the percentage of undergraduates awarded QTS by their ethnicity for a given time period.

    Parameters:
    - time_period: int, the academic year for filtering the data, formatted as YYYYYY.
    """
    # Filter for the specific time period and for undergraduates who were awarded QTS
    filtered_data = data[(data['time_period'] == time_period) &
                         (data['course_level_recoded'] == 'Undergraduate') &
                         (data['qts_status'] == 'Awarded QTS')]

    ethnicity_columns = [
        'pct_total_ethnic_asian',
        'pct_total_ethnic_black',
        'pct_total_ethnic_mixed_ethnicity',
        'pct_total_ethnic_other',
        'pct_total_ethnic_white',
        'pct_total_ethnic_unknown'
    ]
    ethnicity_data = filtered_data[ethnicity_columns].mean().reset_index()
    ethnicity_data.columns = ['Ethnicity', 'Percentage']

    # Create a color mapping for each ethnicity
    color_discrete_map = {
        'pct_total_ethnic_asian': 'blue',
        'pct_total_ethnic_black': 'green',
        'pct_total_ethnic_mixed_ethnicity': 'red',
        'pct_total_ethnic_other': 'cyan',
        'pct_total_ethnic_white': 'magenta',
        'pct_total_ethnic_unknown': 'yellow'
    }

    # Clean up the 'Ethnicity' column to have nicer labels
    ethnicity_data['Ethnicity'] = ethnicity_data['Ethnicity'].str.replace('pct_total_', '')

    # Plotting with Plotly Express
    fig = px.bar(ethnicity_data, x='Ethnicity', y='Percentage',
                 title=f'Percentage of Postgraduates Awarded QTS by Ethnicity ({time_period})',
                 labels={'Ethnicity': 'Ethnicity', 'Percentage': 'Percentage (%)'},
                 color='Ethnicity',  # Assign colors based on the 'Ethnicity' column
                 color_discrete_map=color_discrete_map)

    # Update the layout to rotate the x-axis labels to prevent overlap
    fig.update_layout(
        xaxis_tickangle=-30  # Rotate labels by 45 degrees
    )

    return fig


def line_chart(feature):
    """
    Generates a line chart displaying the total number of undergraduates (n_total) 
    over all time periods, filtered based on the selected feature.

    Parameters:
    - feature: str, one of 'Awarded QTS', 'Not awarded QTS', or 'Teaching in a state-funded school'

    Returns:
    - fig: A Plotly Express figure object representing the line chart.
    """
    # Filter data based on the feature selected
    if feature in ['Awarded QTS', 'Not awarded QTS']:
        filtered_data = data[(data['qts_status'] == feature) & (data['course_level_recoded'] == 'Undergraduate')]
    else:
        filtered_data = data[(data['employment_status'] == feature) & (data['course_level_recoded'] == 'Undergraduate')]

    # Group by time period and sum the total numbers
    grouped_data = filtered_data.groupby('time_period', as_index=False)['n_total'].sum()

    # Convert the 'time_period' column to string to ensure no decimals are shown on the x-axis
    grouped_data['time_period'] = grouped_data['time_period'].astype(str)

    # Generate the line chart
    fig = px.line(grouped_data, x='time_period', y='n_total',
                  title=f'Total Number of Undergraduates Over Time ({feature})',
                  labels={'time_period': 'Academic Year', 'n_total': 'Total Number of Undergraduates'},
                  markers=True)

    # Update the layout to customize the x-axis tick labels
    fig.update_layout(
        xaxis = {
            'tickmode': 'array',
            'tickvals': grouped_data['time_period'],
            'ticktext': grouped_data['time_period']
        }
    )

    return fig
