import json
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HTMLTemplateFormatter, Select

# Load data from the JSON file
with open("items.json") as f:
    items = json.load(f)

# Prepare the data for Bokeh
data = {
    "title": [item["title"] for item in items],
    "url": [item["url"] for item in items],
    "cost": [item["cost"] for item in items],
    "image": [item["image"] for item in items],
    "game_system": [item["game_system"] for item in items],
    "tactical_level": [item["tactical_level"] for item in items],
    "seats_left": [str(item["seats_left"]) if item["seats_left"] is not None else 'N/A' for item in items],
}

source = ColumnDataSource(data)

# Define the columns for the DataTable
columns = [
    TableColumn(field="title", title="Title"),
    TableColumn(field="game_system", title="Game System"),
    TableColumn(field="url", title="URL", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>">Link</a>')),
    TableColumn(field="cost", title="Cost"),
    TableColumn(field="tactical_level", title="Tactical Level"),
    TableColumn(field="seats_left", title="Seats Left"),
    TableColumn(field="image", title="Image", width=150,
                formatter=HTMLTemplateFormatter(template='''
                    <a href="<%= value %>" target="_blank">
                        <img src="<%= value %>" height="300px"/>
                    </a>
                '''))
]

# Create the DataTable
data_table = DataTable(source=source, columns=columns, sizing_mode="stretch_both")

# Create Select widgets for filtering seats_left and tactical_level
filter_seats_left = Select(title="Filter by Seats Left:", value="All", options=["All", "0", "1", "2", "3", "4"])
tactical_levels = sorted(set(data["tactical_level"]))
filter_tactical_level = Select(title="Filter by Tactical Level:", value="All", options=["All"] + tactical_levels)


# Define the callback function for updating the table
def update_table(attr, old, new):
    selected_seats = filter_seats_left.value
    selected_tactical_level = filter_tactical_level.value

    filtered_data = {key: [] for key in data}
    for i in range(len(data['title'])):
        if (selected_seats == "All" or data['seats_left'][i] == selected_seats) and \
                (selected_tactical_level == "All" or data['tactical_level'][i] == selected_tactical_level):
            for key in data:
                filtered_data[key].append(data[key][i])

    source.data = filtered_data


# Add the callback to both Select widgets
filter_seats_left.on_change("value", update_table)
filter_tactical_level.on_change("value", update_table)

# Layout the widgets and the DataTable
layout = column(filter_seats_left, filter_tactical_level, data_table, sizing_mode="stretch_both")

# Add the layout to the current document
curdoc().add_root(layout)
