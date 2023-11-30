from django.http import HttpResponse
from django.template import loader

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp

dtype_mapping = {
    'OperatingSystems': str,
    'Browser': str,
    'Region': str,
    'TrafficType': str,
    'SpecialDay': str,
    'Revenue': str,
    'Weekend': str,
    '5eme lot': str,
    'Code type local': str
}

# Create your views here.
df = pd.read_csv("online_shoppers_intention.csv",dtype=dtype_mapping)


def index(request):
    template = loader.get_template("dataproject/index.html")
    sentence = 'Hello, world. You\'re at the dataproject index.'
    context = {
        'sentence': sentence,
    }
    return HttpResponse(template.render(context,request))

def graphics(request):
    template = loader.get_template("dataproject/graphics.html")

    #Month distribution
    month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    num_to_month = {v: k for k, v in month_to_num.items()}
    # Apply the mapping and sort
    month_counts = df['Month'].value_counts()
    month_counts.index = pd.Index([month_to_num[month] for month in month_counts.index])
    month_counts = month_counts.sort_index()
    month_counts.index = pd.Index([num_to_month[month] for month in month_counts.index])
    month_counts = pd.DataFrame(month_counts)
    month_counts.reset_index(inplace=True)

    month_counts.columns = ['Month', 'Count']
    bar_color = 'lightgreen'
    fig0 = px.bar(month_counts, x='Month', y='Count', title='Monthly Visitor counts')
    fig0.update_layout(
        yaxis_title='Number of Visitors',
        plot_bgcolor='white', 
    )
    fig0.update_traces(marker_color=bar_color)
    month_visitors_plot = to_plot(fig0)
    
    #Categories of Visitors
    VisitorType_counts = df['VisitorType'].value_counts()
    colors = ['limegreen','green', 'darkgreen']
    fig1 = go.Figure(data=[go.Pie(labels=VisitorType_counts.index, values=VisitorType_counts, pull=[0, 0, 0.2, 0],
                                marker=dict(colors=colors),title='Visitors type distribution')])
    categ_visitors_plot = to_plot(fig1)

    #Weekend visits
    df['Revenue'] = df['Revenue'].replace({'TRUE': 1, 'FALSE': 0})
    df['Weekend'] = df['Weekend'].replace({'TRUE': 1, 'FALSE': 0})
    df['Revenue'] = df['Revenue'].astype(str)
    df['Weekend'] = df['Weekend'].astype(str)

    Weekend_counts = df['Weekend'].value_counts()
    colors = ['skyblue','honeydew']
    fig2 = go.Figure(data=[go.Pie(labels=Weekend_counts.index.map({'1': 'Yes', '0': 'No'}), 
                             values=Weekend_counts, marker=dict(colors=colors),
                             title='Weekend distribution')])
    weekends_cnt_plot = to_plot(fig2) 
    
    #Revenue distribution
    Revenue_counts = df['Revenue'].value_counts()
    colors = ['lightsteelblue','lavender']
    fig3 = go.Figure(data=[go.Pie(labels=Revenue_counts.index.map({'1': 'Yes', '0': 'No'}), 
                                values=Revenue_counts, marker=dict(colors=colors),
                                title='Revenue distribution')])
    revenue_dist_plot = to_plot(fig3)

    #Revenue during special days
    color_map = {'Yes': 'lightcoral', 'No': 'lightpink'}
    fig4 = px.histogram(df, 
                    x="SpecialDay", 
                    color=df['Revenue'].map({'1': 'Yes', '0': 'No'}), 
                    barmode='group',
                    title='Visits that led to a transaction or not during Special Days',
                    color_discrete_map=color_map
                    )
    revenue_special_days_plot = to_plot(fig4)

    # Revenue during wwekends
    color_map = {'Yes': 'lightsalmon', 'No': 'salmon'}

    fig5 = px.histogram(df, x=df['Weekend'].map({'1': 'Yes', '0': 'No'}), color=df['Revenue'].map({'1': 'Yes', '0': 'No'}), barmode='group',
                   title='',
                  color_discrete_map=color_map)

    fig5.update_layout(yaxis_title='Number of Visitors',
                    xaxis_title='Weekend',
                    legend_title_text='Revenue',
                    plot_bgcolor='white')
    revenue_weekends_plot = to_plot(fig5)

    #Visitors category by month
    color_map = {'New Visitor': 'red', 'Returning Visitor': 'salmon', 'Other': 'orange'}
    fig6 = px.histogram(df, x="Month", color='VisitorType', barmode='group',
                    title='Visitor Type Distribution by Month',
                    color_discrete_map=color_map)
    fig6.update_layout(yaxis_title='Number of Visitors',
                    legend_title_text='Visitors categories',
                    plot_bgcolor='white')
    visitors_month_plot = to_plot(fig6)

    # Revenue by visitor type
    grouped_df = df.groupby(['VisitorType', 'Revenue']).size().unstack()
    fig7 = px.pie(names=grouped_df.index,
                values=grouped_df["1"],
                hole=0.3,
                title="Pie of transactions by visitor type"
                )
    fig7.update_layout(legend_title_text='Visior category',
                    plot_bgcolor='white')
    revenue_visitor_type_plot = to_plot(fig7)

    #Number of views by visits page type
    pages_df = df[["Administrative", "Informational", "ProductRelated"]]
    pages_df = pages_df.applymap(lambda x: 1 if x >= 1 else 0)

    pages_df2 = pd.melt(pages_df, value_vars=pages_df.columns, var_name='Type of pages', value_name='Number of views')
    pages_df2 = pages_df2[pages_df2['Number of views'] == 1]

    fig8 = px.histogram(pages_df2, x='Type of pages', color='Type of pages',
                    labels={'Number of views': 'Number of views'},
                    title='Total number of views by page type')
       
    fig8.update_layout(plot_bgcolor='white')
    views_pages_type_plot = to_plot(fig8)

    #Visitors type by page type
    pages_df = df[['VisitorType', 'Administrative', 'Informational', 'ProductRelated']]
    grouped_data = pages_df.groupby('VisitorType').median().reset_index()
    grouped_data2 = pd.melt(grouped_data, id_vars='VisitorType', var_name='PageCategory', value_name='Number_of_Visits')
    fig9 = px.bar(grouped_data2, x='VisitorType', y='Number_of_Visits', color='PageCategory',
                title='Median of Visits for Different Page Categories by visitors type')
    fig9.update_layout(plot_bgcolor='white')
    visitors_type_page_type_plot = to_plot(fig9)

    #Administrative Pages visits by Visitor Type
    fig10 = px.box(df, x="VisitorType", y="Administrative",
             labels={"VisitorType": "Visitor Type", "Administrative": "Number of Administrative Pages"},
             title="Distribution of Administrative Pages by Visitor Type",
             color="VisitorType",
             color_discrete_map={"New Visitor": "skyblue", "Returning Visitor": "lightgreen", "Other": "lightcoral"})
    fig10.update_layout(legend_title_text='Visiors categories', plot_bgcolor='white')
    admin_pages_visitors_type_plot = to_plot(fig10)

    #Correlation matrix
    correlations = df.corr(numeric_only=True)
    fig13 = sp.make_subplots(rows=1, cols=1, subplot_titles=["Correlation Matrix"])

    heatmap = go.Heatmap(z=correlations.values,
                        x=correlations.columns,
                        y=correlations.index,
                        colorscale="Viridis")

    fig13.add_trace(heatmap, row=1, col=1)

    fig13.update_layout(title_text="Correlation Matrix",
                    xaxis=dict(ticks=""),
                    yaxis=dict(ticks="", tickvals=list(range(len(correlations.index))), ticktext=correlations.index),
                    coloraxis_colorbar=dict(title="Correlation"))
    correlation_matrix_plot = to_plot(fig13)

    #Bounce Rate by Visitor Type
    bounce_rate_data = df.groupby('VisitorType')['BounceRates'].mean().reset_index()
    fig14 = px.bar(bounce_rate_data, x='VisitorType', y='BounceRates', color='VisitorType',
                title='Bounce Rate by Visitor Type',
                labels={'BounceRates': 'Average Bounce Rate'})

    fig14.update_layout(xaxis_title='Visitor Type', 
                    yaxis_title='Average Bounce Rate',
                    plot_bgcolor='white')
    bounce_rate_visitor_type_plot = to_plot(fig14)

    context = {
        'categ_visitors_plot': categ_visitors_plot,
        'weekends_cnt_plot': weekends_cnt_plot,
        'revenue_dist_plot': revenue_dist_plot,
        'revenue_special_days_plot': revenue_special_days_plot,
        'revenue_weekends_plot': revenue_weekends_plot,
        'visitors_month_plot': visitors_month_plot,
        'revenue_visitor_type_plot': revenue_visitor_type_plot,
        'views_pages_type_plot': views_pages_type_plot,
        'visitors_type_page_type_plot': visitors_type_page_type_plot,
        'admin_pages_visitors_type_plot': admin_pages_visitors_type_plot,
        'correlation_matrix_plot': correlation_matrix_plot,
        'bounce_rate_visitor_type_plot': bounce_rate_visitor_type_plot,
        'month_visitors_plot': month_visitors_plot,
    }
    return HttpResponse(template.render(context,request))

def to_plot(fig):
    return fig.to_html(full_html=False)
