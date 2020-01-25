from turtleapi import db
from turtleapi.models.turtlemodels import Turtle, Tag, TurtleSchema

def find_turtle_from_tags(tags):
    for tag in tags:
        turtle = Turtle.query.filter_by(turtle_id=tag['turtle']).first()
        if turtle is not None:
            turtle_schema = TurtleSchema()
            return turtle_schema.dump(turtle)
    return None