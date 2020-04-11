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

many_to_one_models = [Tag]


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
    many_to_one_dict = {}
    rels = inspect(LagoonEncounter).relationships
    clss = [rel.mapper.class_ for rel in rels]

    turtle_id = 24


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

    many_to_one_col_list = []

    #print(modelList)

    # Iterate over all unique combinations of models
    for pair in itertools.combinations(modelList, 2):
        coll = get_key_connecting_models(pair[0], pair[1])

        # If the models have a relationship, match them with a query so they get joined
        if coll is not None:
            #print(pair[0])
            #print(pair[1])
            if pair[0] in many_to_one_models:
                print("Test1")
                many_to_one_dict[pair[0]] = (pair[1], coll)
            if pair[1] in many_to_one_models:
                print("Test2")
                many_to_one_dict[pair[1]] = (pair[0], coll)
            else:
                print("one-to-one")
                query_filters.append(getattr(pair[0], coll) == getattr(pair[1], coll))

            #if pair[0]._sa_class_manager[getattr(pair[0], coll)]:
            # mmm = getattr(LagoonEncounter, 'encounter_id')
            # if LagoonEncounter._sa_class_manager[mmm].property.uselist:
            #     print("True")

    #return {}

    #print(get_referencing_foreign_keys(Turtle))

    # table_connections = [LagoonEncounter.turtle_id == Turtle.turtle_id]
    # query_filters.append(table_connections)
    tables_to_revisit_later = {}
    filters_to_revisit_later = {}
    fields_to_revisit_later = {}

    ### Iterate over JSON and query for data
    for d in data:
        # Ignore invalid input (tables)
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        elif model_mapping[d] in many_to_one_dict:
            print("skipping to query later")
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
        else:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]
            #buildup_temp_columns = []   # List of DB columns, string format. Needed to handle an empty query result edge case

            for f in fields:
                # Check if field exists in database
                if f in table_columns:
                    query_columns.append(getattr(model_mapping[d], f))
                    #buildup_temp_columns.append(f)
                    query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
                else:
                    print("Extra key (field), ignoring")
                #buildup_valid_columns[d] = buildup_temp_columns

    table_result = db.session.query(*query_columns).filter(*query_filters).all()
    #print(type(table_result))
    #print(type(table_result[0]))
    buildup[d] = table_result

    more_dict = {}
    header_dict = {}
    max_num_dict = {}

    print("TEST")

    for t in tables_to_revisit_later:
        max_num_dict[t] = 0
        #test_str = t.__tablename__ + str(result[0].keys()) # Inefficient, generated x times
        test_str = t.__name__  + ' ['
        first = True
        for f in fields_to_revisit_later[t]:
            if first:
                test_str += f
                first = False
            else:
                test_str += ', ' + f
        test_str += ']'
        header_dict[t] = str(test_str)

    for r in table_result:
        test_model = Tag
        #print(r.encounter_id)
        more_table_result_list = []

        for t in tables_to_revisit_later:
            #print(tables_to_revisit_later.keys())
            #print(tables_to_revisit_later.values())
            # print(many_to_one_dict[t][1])
            # zzzzz = many_to_one_dict[t][1]
            #print(r.turtle_id)
            #print(getattr(r, many_to_one_dict[t][1]))

            result = db.session.query(*tables_to_revisit_later[t]).filter(getattr(t, many_to_one_dict[t][1]) == getattr(r, many_to_one_dict[t][1]))
            num = result.count()
            if num > max_num_dict[t]:
                max_num_dict[t] = num

            result = result.all()
            #print(result)
            more_table_result_list.append(result)

            #result = db.session.query(tables_to_revisit_later[t])
            #print(result)
        result = db.session.query(test_model.tag_number, test_model.turtle_id).filter(test_model.turtle_id == r.turtle_id).all()
        #print(type(result))
        #print(type(result[0]))
        more_dict[r] = more_table_result_list



    # for r in more_dict:
    #     print(more_dict[r])
    
    
    # ### Many-to-one querying
    # for d in data:
    #     if d in model_mapping and model_mapping[d] in many_to_one_dict:
    #         query_columns.clear()
    #         query_filters.clear()
    #         model = model_mapping[d]
    #         table_columns = model.__table__.c
    #         fields = data[d]
    #         buildup_temp_columns2 = []   # List of DB columns, string format. Needed to handle an empty query result edge case
    #         query_filters.append(getattr(model, many_to_one_dict[model][1]) == getattr(many_to_one_dict[model][0], many_to_one_dict[model][1]))

    #         for f in fields:
    #             # Check if field exists in database
    #             if f in table_columns:
    #                 query_columns.append(getattr(model_mapping[d], f))
    #                 buildup_temp_columns2.append(f)
    #                 query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
    #             else:
    #                 print("Extra key (field), ignoring")
    #             #buildup_valid_columns[d] = buildup_temp_columns2
    #         table_result = db.session.query(*query_columns).filter(*query_filters).all()
    #         print(len(table_result))

    ### Create CSV
    # Write the header row
    header_row = []
    try:
        for r in table_result[0].keys():
            header_row.append(r)
    except:
        print("error, empty results")
    # try:
    #     for t in tables_to_revisit_later:
    #         for n in max_num_dict[t]:
    #             header_row.append(header_dict[t])
    # except:
    #     print("error, major fuckup")
    for t in tables_to_revisit_later:
        for i in range(max_num_dict[t]):
            header_row.append(header_dict[t])




    # try:
    #     for h in header_dict:
    #         header_row.append(header_dict[h])
    # except:
    #     print("woops")
    
    # for table in buildup_valid_columns:
    #     for column in buildup_valid_columns[table]:
    #         header_row.append(table + '.' + column)
    
    writer.writerow(header_row)
    
    # Write the body
    for b in buildup:
        for val in buildup[b]:
            new_list = list(val)
            #new_list.extend(more_dict[val])
            for item in more_dict[val]:
                new_list.extend(item)
            # for more in more_dict[val]:
            #     new_list.append(more)
            writer.writerow(new_list)
            # writer.writerow(list(val) + list(more_dict[val][0]))

    # preceding_commas = []
    # for b in buildup:
    #     for val in buildup[b]:
    #         writer.writerow(preceding_commas + list(val))
    #     for num_keys in buildup_valid_columns[b]:
    #         preceding_commas.append('')

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    return {}