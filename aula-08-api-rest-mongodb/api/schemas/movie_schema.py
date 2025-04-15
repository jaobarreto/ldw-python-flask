from marshmallow import Schema, fields
from api import ma

class MovieSchema(ma.Schema):
    _id = fields.Str()  
    title = fields.Str(required=True)  
    description = fields.Str(required=True)
    year = fields.Int(required=True)

    class Meta:
        fields = ("_id", "title", "description", "year") 