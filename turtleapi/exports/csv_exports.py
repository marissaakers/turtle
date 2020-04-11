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
from collections import OrderedDict
from sqlalchemy.inspection import inspect
#from sqlalchemy_utils import get_referencing_foreign_keys
import itertools

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

related_model_mapping = {
    LagoonEncounter: []



}


def field_lister():
    data = {}

    for model in model_mapping:
        model_data = {}
        columns = model_mapping[model].__table__.c
        
        for c in columns:
            model_data[c.key] = c.type.python_type.__name__

        data[model] = model_data

    return data

def parse_query_filter(fieldname, filter, column):
    field_type = column.type.python_type
    # print(field_type)

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

def csv_export(data):


    modelList = []
    rels = inspect(LagoonEncounter).relationships
    clss = [rel.mapper.class_ for rel in rels]
    #print(clss)


    #print(modelList)
    # print(Sample)
    #print(rels)

    turtle_id = 24



    # for rel in inspect(LagoonEncounter).relationships:
    #     print(rel)


    # Small brain iterator
    # keepLooping = False
    # for model in clss:
    #     #print(model)
    #     if model not in modelList:
    #         modelList.append(model)
    #         keepLooping = True
    #     if model is Turtle:
    #         print("Turtle!")




    #return 'test'

    string_io = StringIO()
    writer = csv.writer(string_io)

    buildup = {}
    buildup_valid_columns = {}
    query_columns = []          # List of DB columns to query
    query_filters = []          # List of filters to apply to query
    
    for d in data:
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        else:
            modelList.append(model_mapping[d])

    #print(modelList)

    # Iterate over all unique combinations of models
    for pair in itertools.combinations(modelList, 2):
        coll = get_key_connecting_models(pair[0], pair[1])

        # If the models have a relationship, match them with a query so they get joined
        if coll is not None:
            query_filters.append(getattr(pair[0], coll) == getattr(pair[1], coll))

    #return {}

    #print(get_referencing_foreign_keys(Turtle))

    # table_connections = [LagoonEncounter.turtle_id == Turtle.turtle_id]
    # query_filters.append(table_connections)

    ### Iterate over JSON and query for data
    for d in data:
        # Ignore invalid input (tables)
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        else:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]
            buildup_temp_columns = []   # List of DB columns, string format. Needed to handle an empty query result edge case

            for f in fields:
                # Check if field exists in database
                if f in table_columns:
                    query_columns.append(getattr(model_mapping[d], f))
                    buildup_temp_columns.append(f)
                    query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
                else:
                    print("Extra key (field), ignoring")
                buildup_valid_columns[d] = buildup_temp_columns

    table_result = db.session.query(*query_columns).filter(*query_filters).all()
    buildup[d] = table_result

    ### Create CSV
    # Write the header row
    header_row = []
    for table in buildup_valid_columns:
        for column in buildup_valid_columns[table]:
            header_row.append(table + '.' + column)
    
    writer.writerow(header_row)
    
    # Write the body
    preceding_commas = []
    for b in buildup:
        for val in buildup[b]:
            writer.writerow(preceding_commas + list(val))
        for num_keys in buildup_valid_columns[b]:
            preceding_commas.append('')

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    return {}