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

# For editing, insert any new tags
# WIP & untested 
def insert_new_tags(turtle_id, tags):
    turtle_result = Tag.query.filter(Tag.turtle_id == turtle_id)
    
    if turtle_result is not None:
        tag_schema = TagSchema()
        turtle_result_dump = tag_schema.dump(turtle_result, many=True)
        turtle_tag_list = [d['tag_number'] for d in turtle_result_dump]
        for t in tags:
            if t not in turtle_tag_list:
                new_tag = Tag(
                turtle=turtle_id,
                tag_number=t,
                location="DEBUG",
                active=tag['active'],
                tag_type=tag['tag_type'] #grrr
            )
        