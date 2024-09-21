from marshmallow import Schema, EXCLUDE,  post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.libs import assertions
from core.models.teachers import Teacher


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    user_id = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        assertions.assert_true(len(data_dict.keys()) > 0, 'No data was provided')
        return Teacher(**data_dict)