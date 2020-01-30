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
    #turtles = Turtle.query.filter(Turtle.turtle_id.in_(tags)).all()
    tags = Tag.query.filter(Tag.tag_number.in_(tags)).all() #.distinct()
    
    print("TAGS IS")
    print(tags)

    if tags is not None:
        tag_schema = TagSchema()
        tagdump = tag_schema.dump(tags, many=True)
        print(tagdump)

        print(list(tagdump['turtle_id'].values()))

        # if turtles is not None:
        #     turtle_schema = TurtleSchema()
        #     return turtle_schema.dump(turtles)
    return None
