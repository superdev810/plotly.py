# -*- coding: utf-8 -*-

"""
tools
=====

Functions that USERS will possibly want access to.

"""
from __future__ import absolute_import

import json
import warnings

import six
import os

from plotly import exceptions, optional_imports
from plotly.files import PLOTLY_DIR

DEFAULT_PLOTLY_COLORS = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                         'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                         'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                         'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                         'rgb(188, 189, 34)', 'rgb(23, 190, 207)']


REQUIRED_GANTT_KEYS = ['Task', 'Start', 'Finish']
PLOTLY_SCALES = {'Greys': ['rgb(0,0,0)', 'rgb(255,255,255)'],
                 'YlGnBu': ['rgb(8,29,88)', 'rgb(255,255,217)'],
                 'Greens': ['rgb(0,68,27)', 'rgb(247,252,245)'],
                 'YlOrRd': ['rgb(128,0,38)', 'rgb(255,255,204)'],
                 'Bluered': ['rgb(0,0,255)', 'rgb(255,0,0)'],
                 'RdBu': ['rgb(5,10,172)', 'rgb(178,10,28)'],
                 'Reds': ['rgb(220,220,220)', 'rgb(178,10,28)'],
                 'Blues': ['rgb(5,10,172)', 'rgb(220,220,220)'],
                 'Picnic': ['rgb(0,0,255)', 'rgb(255,0,0)'],
                 'Rainbow': ['rgb(150,0,90)', 'rgb(255,0,0)'],
                 'Portland': ['rgb(12,51,131)', 'rgb(217,30,30)'],
                 'Jet': ['rgb(0,0,131)', 'rgb(128,0,0)'],
                 'Hot': ['rgb(0,0,0)', 'rgb(255,255,255)'],
                 'Blackbody': ['rgb(0,0,0)', 'rgb(160,200,255)'],
                 'Earth': ['rgb(0,0,130)', 'rgb(255,255,255)'],
                 'Electric': ['rgb(0,0,0)', 'rgb(255,250,220)'],
                 'Viridis': ['rgb(68,1,84)', 'rgb(253,231,37)']}

# color constants for violin plot
DEFAULT_FILLCOLOR = '#1f77b4'
DEFAULT_HISTNORM = 'probability density'
ALTERNATIVE_HISTNORM = 'probability'


# Warning format
def warning_on_one_line(message, category, filename, lineno,
                        file=None, line=None):
    return '%s:%s: %s:\n\n%s\n\n' % (filename, lineno, category.__name__,
                                     message)
warnings.formatwarning = warning_on_one_line

ipython_core_display = optional_imports.get_module('IPython.core.display')
sage_salvus = optional_imports.get_module('sage_salvus')


### mpl-related tools ###
def mpl_to_plotly(fig, resize=False, strip_style=False, verbose=False):
    """Convert a matplotlib figure to plotly dictionary and send.

    All available information about matplotlib visualizations are stored
    within a matplotlib.figure.Figure object. You can create a plot in python
    using matplotlib, store the figure object, and then pass this object to
    the fig_to_plotly function. In the background, mplexporter is used to
    crawl through the mpl figure object for appropriate information. This
    information is then systematically sent to the PlotlyRenderer which
    creates the JSON structure used to make plotly visualizations. Finally,
    these dictionaries are sent to plotly and your browser should open up a
    new tab for viewing! Optionally, if you're working in IPython, you can
    set notebook=True and the PlotlyRenderer will call plotly.iplot instead
    of plotly.plot to have the graph appear directly in the IPython notebook.

    Note, this function gives the user access to a simple, one-line way to
    render an mpl figure in plotly. If you need to trouble shoot, you can do
    this step manually by NOT running this fuction and entereing the following:

    ===========================================================================
    from plotly.matplotlylib import mplexporter, PlotlyRenderer

    # create an mpl figure and store it under a varialble 'fig'

    renderer = PlotlyRenderer()
    exporter = mplexporter.Exporter(renderer)
    exporter.run(fig)
    ===========================================================================

    You can then inspect the JSON structures by accessing these:

    renderer.layout -- a plotly layout dictionary
    renderer.data -- a list of plotly data dictionaries
    """
    matplotlylib = optional_imports.get_module('plotly.matplotlylib')
    if matplotlylib:
        renderer = matplotlylib.PlotlyRenderer()
        matplotlylib.Exporter(renderer).run(fig)
        if resize:
            renderer.resize()
        if strip_style:
            renderer.strip_style()
        if verbose:
            print(renderer.msg)
        return renderer.plotly_fig
    else:
        warnings.warn(
            "To use Plotly's matplotlylib functionality, you'll need to have "
            "matplotlib successfully installed with all of its dependencies. "
            "You're getting this error because matplotlib or one of its "
            "dependencies doesn't seem to be installed correctly.")


### graph_objs related tools ###

def get_subplots(rows=1, columns=1, print_grid=False, **kwargs):
    """Return a dictionary instance with the subplots set in 'layout'.

    Example 1:
    # stack two subplots vertically
    fig = tools.get_subplots(rows=2)
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x1', yaxis='y1')]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    Example 2:
    # print out string showing the subplot grid you've put in the layout
    fig = tools.get_subplots(rows=3, columns=2, print_grid=True)

    Keywords arguments with constant defaults:

    rows (kwarg, int greater than 0, default=1):
        Number of rows, evenly spaced vertically on the figure.

    columns (kwarg, int greater than 0, default=1):
        Number of columns, evenly spaced horizontally on the figure.

    horizontal_spacing (kwarg, float in [0,1], default=0.1):
        Space between subplot columns. Applied to all columns.

    vertical_spacing (kwarg, float in [0,1], default=0.05):
        Space between subplot rows. Applied to all rows.

    print_grid (kwarg, True | False, default=False):
        If True, prints a tab-delimited string representation
        of your plot grid.

    Keyword arguments with variable defaults:

    horizontal_spacing (kwarg, float in [0,1], default=0.2 / columns):
        Space between subplot columns.

    vertical_spacing (kwarg, float in [0,1], default=0.3 / rows):
        Space between subplot rows.

    """
    # TODO: protected until #282
    from plotly.graph_objs import graph_objs

    warnings.warn(
        "tools.get_subplots is depreciated. "
        "Please use tools.make_subplots instead."
    )

    # Throw exception for non-integer rows and columns
    if not isinstance(rows, int) or rows <= 0:
        raise Exception("Keyword argument 'rows' "
                        "must be an int greater than 0")
    if not isinstance(columns, int) or columns <= 0:
        raise Exception("Keyword argument 'columns' "
                        "must be an int greater than 0")

    # Throw exception if non-valid kwarg is sent
    VALID_KWARGS = ['horizontal_spacing', 'vertical_spacing']
    for key in kwargs.keys():
        if key not in VALID_KWARGS:
            raise Exception("Invalid keyword argument: '{0}'".format(key))

    # Set 'horizontal_spacing' / 'vertical_spacing' w.r.t. rows / columns
    try:
        horizontal_spacing = float(kwargs['horizontal_spacing'])
    except KeyError:
        horizontal_spacing = 0.2 / columns
    try:
        vertical_spacing = float(kwargs['vertical_spacing'])
    except KeyError:
        vertical_spacing = 0.3 / rows

    fig = dict(layout=graph_objs.Layout())  # will return this at the end
    plot_width = (1 - horizontal_spacing * (columns - 1)) / columns
    plot_height = (1 - vertical_spacing * (rows - 1)) / rows
    plot_num = 0
    for rrr in range(rows):
        for ccc in range(columns):
            xaxis_name = 'xaxis{0}'.format(plot_num + 1)
            x_anchor = 'y{0}'.format(plot_num + 1)
            x_start = (plot_width + horizontal_spacing) * ccc
            x_end = x_start + plot_width

            yaxis_name = 'yaxis{0}'.format(plot_num + 1)
            y_anchor = 'x{0}'.format(plot_num + 1)
            y_start = (plot_height + vertical_spacing) * rrr
            y_end = y_start + plot_height

            xaxis = dict(domain=[x_start, x_end], anchor=x_anchor)
            fig['layout'][xaxis_name] = xaxis
            yaxis = dict(domain=[y_start, y_end], anchor=y_anchor)
            fig['layout'][yaxis_name] = yaxis
            plot_num += 1

    if print_grid:
        print("This is the format of your plot grid!")
        grid_string = ""
        plot = 1
        for rrr in range(rows):
            grid_line = ""
            for ccc in range(columns):
                grid_line += "[{0}]\t".format(plot)
                plot += 1
            grid_string = grid_line + '\n' + grid_string
        print(grid_string)

    return graph_objs.Figure(fig)  # forces us to validate what we just did...


def get_graph_obj(obj, obj_type=None):
    """Returns a new graph object.

    OLD FUNCTION: this will *silently* strip out invalid pieces of the object.
    NEW FUNCTION: no striping of invalid pieces anymore - only raises error
        on unrecognized graph_objs
    """
    # TODO: Deprecate or move. #283
    from plotly.graph_objs import graph_objs
    try:
        cls = getattr(graph_objs, obj_type)
    except (AttributeError, KeyError):
        raise exceptions.PlotlyError(
            "'{}' is not a recognized graph_obj.".format(obj_type)
        )
    return cls(obj)


def validate(obj, obj_type):
    """Validate a dictionary, list, or graph object as 'obj_type'.

    This will not alter the 'obj' referenced in the call signature. It will
    raise an error if the 'obj' reference could not be instantiated as a
    valid 'obj_type' graph object.

    """
    # TODO: Deprecate or move. #283
    from plotly import graph_reference
    from plotly.graph_objs import graph_objs

    if obj_type not in graph_reference.CLASSES:
        obj_type = graph_reference.string_to_class_name(obj_type)

    try:
        cls = getattr(graph_objs, obj_type)
    #except AttributeError:
    except ValueError:
        raise exceptions.PlotlyError(
            "'{0}' is not a recognizable graph_obj.".
            format(obj_type))
    cls(obj)  # this will raise on invalid keys/items


def _replace_newline(obj):
    """Replaces '\n' with '<br>' for all strings in a collection."""
    if isinstance(obj, dict):
        d = dict()
        for key, val in list(obj.items()):
            d[key] = _replace_newline(val)
        return d
    elif isinstance(obj, list):
        l = list()
        for index, entry in enumerate(obj):
            l += [_replace_newline(entry)]
        return l
    elif isinstance(obj, six.string_types):
        s = obj.replace('\n', '<br>')
        if s != obj:
            warnings.warn("Looks like you used a newline character: '\\n'.\n\n"
                          "Plotly uses a subset of HTML escape characters\n"
                          "to do things like newline (<br>), bold (<b></b>),\n"
                          "italics (<i></i>), etc. Your newline characters \n"
                          "have been converted to '<br>' so they will show \n"
                          "up right on your Plotly figure!")
        return s
    else:
        return obj  # we return the actual reference... but DON'T mutate.


def return_figure_from_figure_or_data(figure_or_data, validate_figure):
    from plotly.graph_objs import Figure
    from plotly.basedatatypes import BaseFigure

    validated = False
    if isinstance(figure_or_data, dict):
        figure = figure_or_data
    elif isinstance(figure_or_data, list):
        figure = {'data': figure_or_data}
    elif isinstance(figure_or_data, BaseFigure):
        figure = figure_or_data.to_dict()
        validated = True
    else:
        raise exceptions.PlotlyError("The `figure_or_data` positional "
                                     "argument must be "
                                     "`dict`-like, `list`-like, or an instance of plotly.graph_objs.Figure")

    if validate_figure and not validated:

        try:
            figure = Figure(**figure).to_dict()
        except exceptions.PlotlyError as err:
            raise exceptions.PlotlyError("Invalid 'figure_or_data' argument. "
                                         "Plotly will not be able to properly "
                                         "parse the resulting JSON. If you "
                                         "want to send this 'figure_or_data' "
                                         "to Plotly anyway (not recommended), "
                                         "you can set 'validate=False' as a "
                                         "plot option.\nHere's why you're "
                                         "seeing this error:\n\n{0}"
                                         "".format(err))
        if not figure['data']:
            raise exceptions.PlotlyEmptyDataError(
                "Empty data list found. Make sure that you populated the "
                "list of data objects you're sending and try again.\n"
                "Questions? Visit support.plot.ly"
            )

    return figure

# Default colours for finance charts
_DEFAULT_INCREASING_COLOR = '#3D9970'  # http://clrs.cc
_DEFAULT_DECREASING_COLOR = '#FF4136'

DIAG_CHOICES = ['scatter', 'histogram', 'box']
VALID_COLORMAP_TYPES = ['cat', 'seq']

# For backward compatibility expose make_subplots
# as plotly.tools.make_subplots
from plotly.subplots import make_subplots

# Deprecations
class FigureFactory(object):

    @staticmethod
    def _deprecated(old_method, new_method=None):
        if new_method is None:
            # The method name stayed the same.
            new_method = old_method
        warnings.warn(
            'plotly.tools.FigureFactory.{} is deprecated. '
            'Use plotly.figure_factory.{}'.format(old_method, new_method)
        )

    @staticmethod
    def create_2D_density(*args, **kwargs):
        FigureFactory._deprecated('create_2D_density', 'create_2d_density')
        from plotly.figure_factory import create_2d_density
        return create_2d_density(*args, **kwargs)

    @staticmethod
    def create_annotated_heatmap(*args, **kwargs):
        FigureFactory._deprecated('create_annotated_heatmap')
        from plotly.figure_factory import create_annotated_heatmap
        return create_annotated_heatmap(*args, **kwargs)

    @staticmethod
    def create_candlestick(*args, **kwargs):
        FigureFactory._deprecated('create_candlestick')
        from plotly.figure_factory import create_candlestick
        return create_candlestick(*args, **kwargs)

    @staticmethod
    def create_dendrogram(*args, **kwargs):
        FigureFactory._deprecated('create_dendrogram')
        from plotly.figure_factory import create_dendrogram
        return create_dendrogram(*args, **kwargs)

    @staticmethod
    def create_distplot(*args, **kwargs):
        FigureFactory._deprecated('create_distplot')
        from plotly.figure_factory import create_distplot
        return create_distplot(*args, **kwargs)

    @staticmethod
    def create_facet_grid(*args, **kwargs):
        FigureFactory._deprecated('create_facet_grid')
        from plotly.figure_factory import create_facet_grid
        return create_facet_grid(*args, **kwargs)

    @staticmethod
    def create_gantt(*args, **kwargs):
        FigureFactory._deprecated('create_gantt')
        from plotly.figure_factory import create_gantt
        return create_gantt(*args, **kwargs)

    @staticmethod
    def create_ohlc(*args, **kwargs):
        FigureFactory._deprecated('create_ohlc')
        from plotly.figure_factory import create_ohlc
        return create_ohlc(*args, **kwargs)

    @staticmethod
    def create_quiver(*args, **kwargs):
        FigureFactory._deprecated('create_quiver')
        from plotly.figure_factory import create_quiver
        return create_quiver(*args, **kwargs)

    @staticmethod
    def create_scatterplotmatrix(*args, **kwargs):
        FigureFactory._deprecated('create_scatterplotmatrix')
        from plotly.figure_factory import create_scatterplotmatrix
        return create_scatterplotmatrix(*args, **kwargs)

    @staticmethod
    def create_streamline(*args, **kwargs):
        FigureFactory._deprecated('create_streamline')
        from plotly.figure_factory import create_streamline
        return create_streamline(*args, **kwargs)

    @staticmethod
    def create_table(*args, **kwargs):
        FigureFactory._deprecated('create_table')
        from plotly.figure_factory import create_table
        return create_table(*args, **kwargs)

    @staticmethod
    def create_trisurf(*args, **kwargs):
        FigureFactory._deprecated('create_trisurf')
        from plotly.figure_factory import create_trisurf
        return create_trisurf(*args, **kwargs)

    @staticmethod
    def create_violin(*args, **kwargs):
        FigureFactory._deprecated('create_violin')
        from plotly.figure_factory import create_violin
        return create_violin(*args, **kwargs)


def get_config_plotly_server_url():
    """
    Function to get the .config file's 'plotly_domain' without importing
    the chart_studio package.  This property is needed to compute the default
    value of the plotly.js config plotlyServerURL, so it is independent of
    the chart_studio integration and still needs to live in

    Returns
    -------
    str
    """
    config_file = os.path.join(PLOTLY_DIR, ".config")
    default_server_url = 'https://plot.ly'
    if not os.path.exists(config_file):
        return default_server_url
    with open(config_file, 'rt') as f:
        try:
            config_dict = json.load(f)
            if not isinstance(config_dict, dict):
                data = {}
        except:
            # TODO: issue a warning and bubble it up
            data = {}

    return config_dict.get('plotly_domain', default_server_url)


# get_config_defaults
from _plotly_future_ import _future_flags

if 'remove_deprecations' not in _future_flags:
    from _plotly_future_ import _chart_studio_deprecation

    from chart_studio.tools import (get_config_defaults)
    get_config_defaults = _chart_studio_deprecation(
        get_config_defaults)

    # ensure_local_plotly_files
    from chart_studio.tools import ensure_local_plotly_files
    ensure_local_plotly_files = _chart_studio_deprecation(
        ensure_local_plotly_files)

    # set_credentials_file
    from chart_studio.tools import set_credentials_file
    set_credentials_file = _chart_studio_deprecation(
        set_credentials_file)

    # get_credentials_file
    from chart_studio.tools import get_credentials_file
    get_credentials_file = _chart_studio_deprecation(
        get_credentials_file)

    # reset_credentials_file
    from chart_studio.tools import reset_credentials_file
    reset_credentials_file = _chart_studio_deprecation(
        reset_credentials_file)

    # set_config_file
    from chart_studio.tools import set_config_file
    set_config_file = _chart_studio_deprecation(
        set_config_file)

    # get_config_file
    from chart_studio.tools import get_config_file
    get_config_file = _chart_studio_deprecation(
        get_config_file)

    # reset_config_file
    from chart_studio.tools import reset_config_file
    reset_config_file = _chart_studio_deprecation(
        reset_config_file)

    # get_embed
    from chart_studio.tools import get_embed
    get_embed = _chart_studio_deprecation(
        get_embed)

    # embed
    from chart_studio.tools import embed
    embed = _chart_studio_deprecation(
        embed)
