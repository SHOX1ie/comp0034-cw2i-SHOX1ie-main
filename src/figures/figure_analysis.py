from pathlib import Path
import pandas as pd
import plotly.express as px

# Extract the data
data_path = Path(__file__).parent.parent.parent.joinpath("data", "df_prepared.csv")

data = pd.read_csv(data_path)


def line_chart_analysis(data, selected_feature, time_period_range, qts_status="Awarded QTS"):
    """
    Generates a line chart to compare selected metrics of undergraduates and postgraduates who were awarded QTS.

    Parameters:
    - data: DataFrame, the dataset containing the information.
    - selected_feature: str, one of the metrics to be compared.
    - time_period_range: list, a list of strings representing the range of academic years to include in the chart.
    - qts_status: str, the QTS status to filter on, defaulted to "Awarded QTS".

    Returns:
    - fig: A Plotly Express figure object representing the line chart.
    """
    # Convert 'time_period' to string
    data['time_period'] = data['time_period'].astype(str)
    # Filter data based on QTS status and the specified time period range
    filtered_data = data[
        (data['qts_status'] == qts_status) &
        (data['time_period'].isin(time_period_range))
    ]

    # Exclude "total" category from course_level_recoded
    filtered_data = filtered_data[~filtered_data['course_level_recoded'].str.lower().str.contains('total')]

    # Sort the data by time_period to ensure the order is correct on the x-axis
    filtered_data = filtered_data.sort_values('time_period')

    # Define color mapping for 'Postgraduate' and 'Undergraduate'
    color_discrete_map = {'Postgraduate': 'blue', 'Undergraduate': 'magenta'}

    # Create the line chart
    fig = px.line(
        filtered_data,
        x='time_period',
        y=selected_feature,
        color='course_level_recoded',
        title=f'Comparison of {selected_feature} by Course Level Over Time',
        labels={'time_period': 'Academic Year', selected_feature: f'Percentage of {selected_feature}'},
        markers=True,
        color_discrete_map=color_discrete_map,
        category_orders={"time_period": time_period_range}  # Ensure the x-axis respects the order of academic years
    )

    return fig
