from turtleapi import db
from turtleapi.models.turtlemodels import Turtle, Tag, TurtleSchema, TagSchema

# Match one turtle
def find_turtle_from_tags(tags):
    # taglist = []
    
    # for t in tags:
    #     taglist.append(t['tag_number'])

    # turtle = Turtle.query.filter(Tag.tag_number.in_(taglist)).first()
    # if turtle is not None:
    #     turtle_schema = TurtleSchema()
    #     return turtle_schema.dump(turtle)
    # return None

    for t in tags:
        res = Tag.query.filter_by(tag_number=t['tag_number']).first()
        if res is not None:
            turtle = Turtle.query.filter_by(turtle_id=res.turtle_id).first()
            return turtle
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
def insert_new_tags(tags):
    tag_schema = TagSchema()
    
    print("HEYO")
    print(tags)
    for t in tags:
        print(t)
        tag_result = Tag.query.filter(Tag.tag_number==t['tag_number']).first()
        print(tag_result)
        if tag_result is None:
            print(True)
            tag = tag_schema.load(t, unknown='EXCLUDE')
            db.session.add(tag)

    db.session.commit()