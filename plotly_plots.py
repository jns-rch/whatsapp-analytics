""" Plotter
Plot functions with Plotly for standardized plots
"""

import plotly.express as px
from plotly.subplots import make_subplots

class Plotter():
    def __init__(self, title_x=0.5, title_font_size=24, font_size=14, template='plotly_white', 
                    autosize=True, margin={"l":0, "r":0, "t":120, "b":0}, 
                    color_discrete_sequence=px.colors.qualitative.T10):
        self.title_x = title_x
        self.title_font_size = title_font_size
        self.font_size = font_size
        self.template = template
        self.autosize = autosize
        self.color_discrete_sequence = color_discrete_sequence
        self.margin = margin

    def standardize_plot(self, fig):
        fig.update_layout(title_font_size=self.title_font_size,
            title_x=self.title_x,
            font_size=self.font_size,
            template=self.template,
            autosize=self.autosize,
            margin=self.margin,
            legend={"orientation":"h", "y":-0.3}
            )
        return fig
          
    def barplot(self, data, x, y, color=None, barmode=None, title_text=None, 
                    legend_title_text=None, xaxis_title=None, yaxis_title=None, 
                    xtickvals=None, ytickvals=None, xtickangle=None, ytickangle=None): 
        fig = px.bar(data_frame=data, x=x, y=y, color=color, barmode=barmode, 
                    color_discrete_sequence=self.color_discrete_sequence)
        fig = fig.update_xaxes(tickvals=xtickvals, tickangle=xtickangle)
        fig = fig.update_yaxes(tickvals=ytickvals, tickangle=ytickangle)
        fig = fig.update_layout(title_text=title_text, legend_title_text=legend_title_text, 
                    xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig = self.standardize_plot(fig)

        return fig
    
    def pieplot(self, data, values, names, color=None, title_text=None, 
                    legend_title_text=None): 
        fig = px.pie(data_frame=data, values=values, names=names, color=color, 
                    color_discrete_sequence=self.color_discrete_sequence)
        fig = fig.update_layout(title_text=title_text, legend_title_text=legend_title_text)
        fig = self.standardize_plot(fig)

        return fig

    def histogram(self, data, x, color=None, title_text=None, legend_title_text=None, 
                    xaxis_title=None, yaxis_title=None, xtickvals=None, ytickvals=None, 
                    xtickangle=None, ytickangle=None):
        fig = px.histogram(data_frame=data, x=x, color=color, 
                    color_discrete_sequence = self.color_discrete_sequence)
        fig = fig.update_xaxes(tickvals=xtickvals, tickangle=xtickangle)
        fig = fig.update_yaxes(tickvals=ytickvals, tickangle=ytickangle)
        fig = fig.update_layout(title_text=title_text, legend_title_text=legend_title_text, 
                    xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig = self.standardize_plot(fig)

        return fig

    def boxplot(self, data, x=None, y=None, color=None, title_text=None, legend_title_text=None, 
                    xaxis_title=None, yaxis_title=None, xtickvals=None, ytickvals=None, 
                    xtickangle=None, ytickangle=None):
        fig = px.box(data, x, y, color=color, 
                    color_discrete_sequence = self.color_discrete_sequence)
        fig = fig.update_xaxes(tickvals=xtickvals, tickangle=xtickangle)
        fig = fig.update_yaxes(tickvals=ytickvals, tickangle=ytickangle)
        fig = fig.update_layout(title_text=title_text, legend_title_text=legend_title_text, 
                    xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig = self.standardize_plot(fig)

        return fig

    def lineplot(self, data, x, y, color=None, title_text=None, legend_title_text=None, 
                    xaxis_title=None, yaxis_title=None, xtickvals=None, ytickvals=None, 
                    xtickangle=None, ytickangle=None): 
        fig = px.line(data_frame=data, x=x, y=y, color=color, 
                    color_discrete_sequence=self.color_discrete_sequence)
        fig = fig.update_xaxes(tickvals=xtickvals, tickangle=xtickangle)
        fig = fig.update_yaxes(tickvals=ytickvals, tickangle=ytickangle)
        fig = fig.update_layout(title_text=title_text, legend_title_text=legend_title_text, 
                    xaxis_title=xaxis_title, yaxis_title=yaxis_title)
        fig = self.standardize_plot(fig)

        return fig