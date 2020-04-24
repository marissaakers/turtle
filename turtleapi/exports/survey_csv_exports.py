from flask import request, make_response
from turtleapi.models.turtlemodels import (Emergence, Depredation, Disorientation, Scarp,
    FalseCrawl, DcCrawl, BigSurvey, NSRefuge)
from turtleapi.exports.csv_exports import csv_export, field_lister

# Easy way to convert incoming JSON string to database model / table
model_mapping_survey = {
    "Emergence": Emergence,
    "Depredation": Depredation,
    "Disorientation": Disorientation,
    "Scarp": Scarp,
    "FalseCrawl": FalseCrawl,
    "DcCrawl": DcCrawl,
    "BigSurvey": BigSurvey,
    "NSRefuge": NSRefuge
}

# No SQLAlchemy built-in to see if relationship is one-to-one or one-to-many
# List tables with one-to-many relationships here
many_to_one_models_survey = [Emergence]

# Return list of tables and fields for the frontend to display
def survey_field_lister():
    return field_lister(model_mapping_survey, many_to_one_models_survey)

# Query and return CSV file
def survey_csv_export(data):
    return csv_export(data, model_mapping_survey, many_to_one_models_survey)