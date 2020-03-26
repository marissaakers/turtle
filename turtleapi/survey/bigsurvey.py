from turtleapi import db
from turtleapi.models.turtlemodels import BigSurvey, Emergence

def insert_big_survey(data):
    big_survey = BigSurvey()
    emergences = []

    for item in data.items():
        if item[0] == 'emergences':
            for em in item[1]:
                emergences.append(Emergence(**em))
        else:
            setattr(big_survey, item[0], item[1])

    big_survey.emergences = emergences
    db.session.add(big_survey)
    db.session.commit()
    return {'message':'no errors'}