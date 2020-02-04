from turtleapi import db
from turtleapi.models.turtlemodels import Turtle, Tag, TurtleSchema, TagSchema

# Match one turtle
def find_turtle_from_tags(tags):
    taglist = []
    
    for t in tags:
        taglist.append(t['tag_number'])

    turtle = Turtle.query.filter(Tag.tag_number.in_(taglist)).first()
    if turtle is not None:
        turtle_schema = TurtleSchema()
        return turtle_schema.dump(turtle)
    return None

# Match all turtles
def find_turtles_from_tags(tags):
    #turtle_ids = Tag.query.filter(Tag.tag_number.in_(tags)).all() #.distinct()
    #turtle_ids = Tag.query.filter(Tag.tag_number.in_(tags)).distinct()
    turtle_ids = Tag.query.distinct(Tag.turtle_id).filter(Tag.tag_number.in_(tags)).all()
    #turtle_ids = Tag.query.with_entities(Tag.turtle_id).distinct(Tag.turtle_id).filter(Tag.tag_number.in_(tags)).all() # doesn't work?

    if turtle_ids is not None:
        tag_schema = TagSchema()
        turtle_ids_dump = tag_schema.dump(turtle_ids, many=True)

        turtle_ids_list = [d['turtle'] for d in turtle_ids_dump]
        return turtle_ids_list
    return None
