#!/usr/bin/env python
# -*- coding: UTF8 -*-

# Author: Guillaume Bouvier -- guillaume.bouvier@pasteur.fr
# https://research.pasteur.fr/en/member/guillaume-bouvier/
# 2020-01-13 09:32:10 (UTC+0100)

import sys
import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def plot_histogram(fields, plotid):
    """
    Plot the histogram for the data given by fields
    """
    plot = dcc.Graph(
        id=plotid,
        figure={
            'data': [
                {'x': df[field], 'type': 'histogram',
                 'name':field} for field in fields],
            'layout': {
                'title': 'Histogram',
                'showlegend': True
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
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    plots = []

    if args.hist is not None:
        hist_fields = nested_args(args.hist)
        for i, fields in enumerate(hist_fields):
            print(i, fields)
            plots.append(plot_histogram(fields, 'hist_%d' % i))

    app.layout = html.Div(plots)
    app.run_server(debug=True)
