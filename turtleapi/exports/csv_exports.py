from flask import request, make_response
import csv
from io import StringIO
from turtleapi.models.turtlemodels import (LagoonEncounter, TridentEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, LagoonMetadata, Net,
                                           IncidentalCapture, BeachEncounter, OffshoreEncounter,
                                           OffshoreMetadata, TridentMetadata, SampleTracking, Clutch)
from turtleapi import db
from sqlalchemy.orm import load_only
from sqlalchemy import select
import datetime
from sqlalchemy.inspection import inspect
import itertools

# Easy way to convert incoming JSON string to database model / table
model_mapping = {
    "LagoonEncounter": LagoonEncounter,
    "TridentEncounter": TridentEncounter,
    "BeachEncounter": BeachEncounter,
    "OffshoreEncounter": OffshoreEncounter,
    "LagoonMetadata": LagoonMetadata,
    "TridentMetadata": TridentMetadata,
    "OffshoreMetadata": OffshoreMetadata,
    "Clutch": Clutch,
    "Turtle": Turtle,
    "Net": Net,
    "IncidentalCapture": IncidentalCapture,
    "Tag": Tag,
    "Morphometrics": Morphometrics,
    "Sample": Sample,
    "SampleTracking": SampleTracking
}

# No SQLAlchemy built-in to see if relationship is one-to-one or one-to-many
# List tables with one-to-many relationships here
many_to_one_models = [Tag]

# Return list of tables and fields for the frontend to display
def field_lister():
    data = {}

    for model in model_mapping:
        model_data = {}
        columns = model_mapping[model].__table__.c
        
        for c in columns:
            model_data[c.key] = c.type.python_type.__name__

        data[model] = model_data

    return data

# Generate a filter we can query on, depending on column type
def parse_query_filter(fieldname, filter, column):
    field_type = column.type.python_type

    queries = []

    # Filter is blank; no filter / return all values for this column
    if filter is "":
        return queries
    
    # Case: string
    if field_type is str:
        queries.append(column.contains(filter))

    # Case: int, float, date, time, etc.
    else:
        try:
            if "_" in filter:
                range = filter.split("_")
                queries.append(column >= range[0])
                queries.append(column <= range[1])
            else:
                queries.append(column == filter)
        except:
            print("ERROR HANDLING INPUT " + fieldname + " WITH GENERIC FILTER")
    
    return queries

# Return name of column if two models have a relationship. Else, return None
def get_key_connecting_models(model1, model2):
    rels = inspect(model1).relationships
    for rel in rels:
        clss = rel.mapper.class_
        if clss is model2:
            try:
                name = inspect(model1).primary_key[0].name
                getattr(model1, name)
                getattr(model2, name)
                return name
            except:
                return inspect(model2).primary_key[0].name
    
    return None

# Query and return CSV file
def csv_export(data):
    modelList = []
    many_to_one_dict = {}
    string_io = StringIO()
    writer = csv.writer(string_io)
    query_columns = []          # List of DB columns to query
    query_filters = []          # List of filters to apply to query
    
    ### Groundwork for one-to-many relationship handling
    # Make a list of requested models
    for d in data:
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        else:
            modelList.append(model_mapping[d])

    # Iterate over all unique combinations of models
    for pair in itertools.combinations(modelList, 2):
        coll = get_key_connecting_models(pair[0], pair[1])

        # If the models have a one-to-many relationship, note this for later
        if coll is not None:
            if pair[0] in many_to_one_models:
                many_to_one_dict[pair[0]] = (pair[1], coll)
            if pair[1] in many_to_one_models:
                many_to_one_dict[pair[1]] = (pair[0], coll)
            else:
                # Normal one-to-one case; just add a filter to JOIN the tables
                query_filters.append(getattr(pair[0], coll) == getattr(pair[1], coll))

    tables_to_revisit_later = {}
    filters_to_revisit_later = {}
    fields_to_revisit_later = {}

    ### Iterate over JSON and query for data
    for d in data:
        # Ignore invalid input (tables)
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        # Gather data for handling one-to-many later
        elif model_mapping[d] in many_to_one_dict:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]
            field_list = []
            column_list = []
            filter_list = []

            for f in fields:
                # Check if field exists in database
                if f in table_columns:
                    field_list.append(f)
                    column_list.append(getattr(model_mapping[d], f))
                    filter_list.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
            tables_to_revisit_later[model_mapping[d]] = column_list
            filters_to_revisit_later[model_mapping[d]] = filter_list
            fields_to_revisit_later[model_mapping[d]] = field_list
        # Handle regular tables
        else:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]

            for f in fields:
                # Check if field exists in database
                if f in table_columns:
                    query_columns.append(getattr(model_mapping[d], f))
                    query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
                else:
                    print("Extra key (field), ignoring")

    # Query for normal tables
    table_result = db.session.query(*query_columns).filter(*query_filters).all()

    ### Handle one-to-many relationships
    more_dict = {}
    header_dict = {}
    max_num_dict = {}

    # Generate string for header row of CSV
    for t in tables_to_revisit_later:
        max_num_dict[t] = 0
        test_str = t.__name__  + ' ['
        first = True

        for f in fields_to_revisit_later[t]:
            if first:
                test_str += f
                first = False
            else:
                test_str += ', ' + f
        
        test_str += ']'
        header_dict[t] = test_str

    # For each result, query any table(s) needed and store the result
    for r in table_result:
        test_model = Tag
        more_table_result_list = []

        # Iterate over tables
        for t in tables_to_revisit_later:
            result = db.session.query(*tables_to_revisit_later[t]).filter(getattr(t, many_to_one_dict[t][1]) == getattr(r, many_to_one_dict[t][1]))
            num = result.count()

            # Need to track maximum number of results so the header is generated correctly
            if num > max_num_dict[t]:
                max_num_dict[t] = num

            result = result.all()
            more_table_result_list.append(result)

        more_dict[r] = more_table_result_list

    ### Create CSV
    # Write most of the header row
    header_row = []
    try:
        for r in table_result[0].keys():
            header_row.append(r)
    except:
        print("error, empty results")
        return {'error': 'Result was empty'}

    # Write dynamic, one-to-many portion of the header row
    try:
        for t in tables_to_revisit_later:
            for i in range(max_num_dict[t]):
                header_row.append(header_dict[t])
    except:
        print("error adding dynamic header")
        return {'error': 'Problem generating one-to-many output'}

    writer.writerow(header_row)
    
    # Write the body
    for r in table_result:
        new_list = list(r)
        for item in more_dict[r]:
            new_list.extend(item)
        writer.writerow(new_list)

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    return {}