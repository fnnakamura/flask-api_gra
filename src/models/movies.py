from marshmallow import EXCLUDE, Schema, fields


class MovieSchema(Schema):
    id = fields.Integer(allow_none=True)
    year = fields.Integer(required=True,
                          error_messages={"required": "A movie needs a year"})
    title = fields.Str(required=True,
                       error_messages={"required": "A movie needs a title"})
    studios = fields.Str(required=True,
                         error_messages={"required": "A movie needs a studio"})
    producers = fields.Str(required=True,
                           error_messages={"required": "A movie needs a producer"})
    winner = fields.Boolean(allow_none=True)

    class Meta:
        unknown = EXCLUDE
