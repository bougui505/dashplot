#!/usr/bin/env python3
# -*- coding: UTF8 -*-

# Author: Guillaume Bouvier -- guillaume.bouvier@pasteur.fr
# https://research.pasteur.fr/en/member/guillaume-bouvier/
# 2020-01-13 09:32:10 (UTC+0100)

import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def plot_histogram(df, fields, plotid):
    """
    Plot the histogram for the data given by fields
    """
    data = []
    for field in fields:
        data.append({'x': df[field], 'type': 'histogram',
                     'name': field})
    plot = dcc.Graph(
        id=plotid,
        figure={
            'data': data,
            'layout': {
                'showlegend': True,
                'yaxis': {'title': 'Count'}
            },
        }
    )
    return plot


def plot_scatter(df, x_fields, y_fields, plotid, labels=None):
    """
    Scatter plot
    - df: dataframe
    - x_fields: name of the field to use for the x values
    - y_fields: name of the field to use for the y values
    - labels: labels to display when hovering the points
    """
    data = []
    if labels is None:
        labels = [None, ]*len(y_fields)
    for (x_field, y_field, label) in zip(x_fields, y_fields, labels):
        data.append({'x': df[x_field],
                     'y': df[y_field],
                     'name': y_field,
                     'mode': 'markers',
                     'text': df[label]})
    plot = dcc.Graph(
        id=plotid,
        figure={
            'data': data,
            'layout': {
                'showlegend': True,
                'xaxis': {'title': x_field},
                'yaxis': {'title': 'y'}
            },
        }
    )
    return plot


def nested_args(args):
    """
    Split a list of list
    """
    if type(args[0]) is list:
        return args
    else:
        return [args, ]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plot data using Dash (https://dash.plot.ly)')
    parser.add_argument('--csv', help='csv with data', type=str)
    parser.add_argument('--hist', nargs='+', type=str,
                        help='plot histogram for the given fields',
                        action='append', metavar='Fields1')
    parser.add_argument('--scatter', help='Toggle scatter plot',
                        default=False, action='store_true')
    parser.add_argument('-x', help='Field for x-values', action='append',
                        type=str, nargs='+')
    parser.add_argument('-y', help='Field for y-values', action='append',
                        type=str, nargs='+')
    parser.add_argument('--labels', help='Name of the field with the labels to display when hovering data points',
                        type=str, nargs='+', action='append')
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    plots = []

    if args.hist is not None:
        hist_fields = nested_args(args.hist)
        print("Histograms for:")
        for i, fields in enumerate(hist_fields):
            print(i, fields)
            plots.append(plot_histogram(df, fields, 'hist_%d' % i))

    if args.scatter:
        x_fields = nested_args(args.x)
        y_fields = nested_args(args.y)
        if args.labels is None:
            labels = [[None, ]*len(e) for e in y_fields]
        else:
            labels = nested_args(args.labels)
        print("Scatter plots for:")
        for i in range(len(x_fields)):
            x_field = x_fields[i]
            y_field = y_fields[i]
            label = labels[i]
            print(i, x_field, y_field)
            plots.append(plot_scatter(df, x_field, y_field, 'scatter_%d' % i,
                         labels=label))

    app.layout = html.Div(plots)
    app.run_server(debug=True)
