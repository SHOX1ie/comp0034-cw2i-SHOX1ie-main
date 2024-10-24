from pathlib import Path
import pandas as pd
import plotly.express as px

# Extract the data
data_path = Path(__file__).parent.parent.parent.joinpath("data", "df_prepared.csv")

data = pd.read_csv(data_path)


def pie_chart_total(time_period):
    """
    Generates an interactive pie chart showing the number of undergraduates and postgraduates awarded QTS.

    Parameters:
    - time_period: str, the academic year for filtering the data, formatted as YYYYYY.
    """
    # Filter data for the specific time period, for those who were awarded QTS
    # and exclude the 'Total' category to get only undergraduates and postgraduates
    filtered_data = data[(data['time_period'] == time_period) &
                         (data['qts_status'] == 'Awarded QTS') &
                         (~data['course_level_recoded'].isin(['Total']))]

    # Group by course level and sum up the totals
    distribution = filtered_data.groupby(['course_level_recoded'])['n_total'].sum().reset_index()
    distribution.columns = ['Course Level', 'Total']

    custom_colors = ['#EB89B5', '#330C73', '#FFD700', '#C1E1C1', '#6A0DAD']
    # Plotting with Plotly Express
    fig = px.pie(distribution, names='Course Level', values='Total',
                 title=f'Distribution of Awarded QTS Among Course Levels ({time_period})',
                 labels={'Course Level': 'Course Level', 'Total': 'Number Awarded QTS'},
                 color_discrete_sequence=custom_colors)

    # Here's the updated layout configuration for a transparent background
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # Additional style settings as needed
    )

    return fig


def pie_chart_age(time_period, course_level):
    """
    Generates an interactive pie chart for the distribution of percentage total age under 25 and 25 and over
    with awarded QTS, with a checklist of undergraduates and postgraduates and a dropdown for time period.

    Parameters:
    - time_period: str, the academic year for filtering the data, formatted as YYYYYY.
    - course_level: list, the course levels to include in the chart.
    """
    # Filter data for the specific time period, awarded QTS, and the selected course levels
    filtered_data = data[(data['time_period'] == time_period) &
                         (data['qts_status'] == 'Awarded QTS') &
                         (data['course_level_recoded'].isin(course_level))]

    # Assuming the data has columns for age distribution percentages named 'pct_total_age_u25' and 'pct_total_age_25andover'
    age_columns = ['pct_total_age_u25', 'pct_total_age_25andover']
    # Calculate the mean of the percentages as we are showing distribution
    age_distribution = filtered_data[age_columns].mean().reset_index()
    age_distribution.columns = ['Age Group', 'Percentage']

    # Map age group columns to a more readable form if necessary
    age_distribution['Age Group'] = age_distribution['Age Group'].map({
        'pct_total_age_u25': 'Percentage age under 25',
        'pct_total_age_25andover': 'Percentage age 25 and Over'
    })

    custom_colors = ['#EB89B5', '#330C73', '#FFD700', '#C1E1C1', '#6A0DAD']

    # Plotting with Plotly Express
    fig = px.pie(age_distribution, names='Age Group', values='Percentage',
                 title=f'Percentage Distribution of Age Groups Awarded QTS ({time_period})',
                 labels={'Percentage': '% of Total Awarded QTS'},
                 color_discrete_sequence=custom_colors)

    # Here's the updated layout configuration for a transparent background
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # Additional style settings as needed
    )

    return fig
