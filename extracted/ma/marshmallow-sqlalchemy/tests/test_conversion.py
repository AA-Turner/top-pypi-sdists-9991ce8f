import datetime as dt
import decimal
import uuid
from typing import cast

import pytest
import sqlalchemy as sa
from marshmallow import Schema, fields, validate
from sqlalchemy import Integer, String
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy.orm import Mapped, Session, column_property

from marshmallow_sqlalchemy import (
    ModelConversionError,
    ModelConverter,
    column2field,
    field_for,
    fields_for_model,
    property2field,
)
from marshmallow_sqlalchemy.fields import Related, RelatedList

from .conftest import CourseLevel, mapped_column


def contains_validator(field, v_type):
    for v in field.validators:
        if isinstance(v, v_type):
            return v
    return False


class TestModelFieldConversion:
    def test_fields_for_model_types(self, models):
        fields_ = fields_for_model(models.Student, include_fk=True)
        assert type(fields_["id"]) is fields.Int
        assert type(fields_["full_name"]) is fields.Str
        assert type(fields_["dob"]) is fields.Date
        assert type(fields_["current_school_id"]) is fields.Int
        assert type(fields_["date_created"]) is fields.DateTime

    def test_fields_for_model_handles_exclude(self, models):
        fields_ = fields_for_model(models.Student, exclude=("dob",))
        assert type(fields_["id"]) is fields.Int
        assert type(fields_["full_name"]) is fields.Str
        assert fields_["dob"] is None

    def test_fields_for_model_handles_custom_types(self, models):
        fields_ = fields_for_model(models.Course, include_fk=True)
        assert type(fields_["grade"]) is fields.Int
        assert type(fields_["transcription"]) is fields.Str

    def test_fields_for_model_saves_doc(self, models):
        fields_ = fields_for_model(models.Student, include_fk=True)
        assert (
            fields_["date_created"].metadata["description"]
            == "date the student was created"
        )

    def test_length_validator_set(self, models):
        fields_ = fields_for_model(models.Student)
        validator = contains_validator(fields_["full_name"], validate.Length)
        assert validator
        assert validator.max == 255

    def test_none_length_validator_not_set(self, models):
        fields_ = fields_for_model(models.Course)
        assert not contains_validator(fields_["transcription"], validate.Length)

    def test_sets_allow_none_for_nullable_fields(self, models):
        fields_ = fields_for_model(models.Student)
        assert fields_["dob"].allow_none is True

    def test_enum_with_choices_converted_to_field_with_validator(self, models):
        fields_ = fields_for_model(models.Course)
        validator = contains_validator(fields_["level"], validate.OneOf)
        assert validator
        assert list(validator.choices) == ["Primary", "Secondary"]

    def test_enum_with_class_converted_to_enum_field(self, models):
        fields_ = fields_for_model(models.Course)
        field = fields_["level_with_enum_class"]
        assert type(field) is fields.Enum
        assert contains_validator(field, validate.OneOf) is False
        assert field.enum is CourseLevel

    def test_many_to_many_relationship(self, models):
        student_fields = fields_for_model(models.Student, include_relationships=True)
        courses_field = student_fields["courses"]
        assert type(courses_field) is RelatedList
        assert courses_field.required is False

        course_fields = fields_for_model(models.Course, include_relationships=True)
        students_field = course_fields["students"]
        assert type(students_field) is RelatedList
        assert students_field.required is False

    def test_many_to_one_relationship(self, models):
        student_fields = fields_for_model(models.Student, include_relationships=True)
        current_school_field = student_fields["current_school"]
        assert type(current_school_field) is Related
        assert current_school_field.allow_none is False
        assert current_school_field.required is True

        school_fields = fields_for_model(models.School, include_relationships=True)
        assert type(school_fields["students"]) is RelatedList

        teacher_fields = fields_for_model(models.Teacher, include_relationships=True)
        current_school_field = teacher_fields["current_school"]
        assert type(current_school_field) is Related
        assert current_school_field.required is False

    def test_many_to_many_uselist_false_relationship(self, models):
        teacher_fields = fields_for_model(models.Teacher, include_relationships=True)
        substitute_field = teacher_fields["substitute"]
        assert type(substitute_field) is Related
        assert substitute_field.required is False

    def test_include_fk(self, models):
        student_fields = fields_for_model(models.Student, include_fk=False)
        assert "current_school_id" not in student_fields

        student_fields2 = fields_for_model(models.Student, include_fk=True)
        assert "current_school_id" in student_fields2

    def test_overridden_with_fk(self, models):
        graded_paper_fields = fields_for_model(models.GradedPaper, include_fk=False)
        assert "id" in graded_paper_fields

    def test_rename_key(self, models):
        class RenameConverter(ModelConverter):
            def _get_field_name(self, prop):
                if prop.key == "name":
                    return "title"
                return prop.key

        converter = RenameConverter()
        fields = converter.fields_for_model(models.Paper)
        assert "title" in fields
        assert "name" not in fields

    def test_subquery_proxies(self, session: Session, Base: type, models):
        # Model from a subquery, columns are proxied.
        # https://github.com/marshmallow-code/marshmallow-sqlalchemy/issues/383
        first_graders = session.query(models.Student).filter(
            models.Student.courses.any(models.Course.grade == 1)
        )

        class FirstGradeStudent(Base):
            __table__ = first_graders.subquery("first_graders")

        fields_ = fields_for_model(FirstGradeStudent)
        assert fields_["dob"].allow_none is True


def make_property(*column_args, **column_kwargs):
    return column_property(sa.Column(*column_args, **column_kwargs))


class TestPropertyFieldConversion:
    @pytest.fixture
    def converter(self):
        return ModelConverter()

    def test_convert_custom_type_mapping_on_schema(self):
        class MyDateTimeField(fields.DateTime):
            pass

        class MySchema(Schema):
            TYPE_MAPPING = Schema.TYPE_MAPPING.copy()
            TYPE_MAPPING.update({dt.datetime: MyDateTimeField})

        converter = ModelConverter(schema_cls=MySchema)
        prop = make_property(sa.DateTime())
        field = converter.property2field(prop)
        assert type(field) is MyDateTimeField

    @pytest.mark.parametrize(
        ("sa_type", "field_type"),
        (
            (sa.String, fields.Str),
            (sa.Unicode, fields.Str),
            (sa.LargeBinary, fields.Str),
            (sa.Text, fields.Str),
            (sa.Date, fields.Date),
            (sa.DateTime, fields.DateTime),
            (sa.Boolean, fields.Bool),
            (sa.Float, fields.Float),
            (sa.SmallInteger, fields.Int),
            (sa.Interval, fields.TimeDelta),
            (postgresql.UUID, fields.UUID),
            (postgresql.MACADDR, fields.Str),
            (postgresql.INET, fields.Str),
            (postgresql.BIT, fields.Integer),
            (postgresql.OID, fields.Integer),
            (postgresql.CIDR, fields.String),
            (postgresql.DATE, fields.Date),
            (postgresql.TIME, fields.Time),
            (mysql.INTEGER, fields.Integer),
            (mysql.DATETIME, fields.DateTime),
        ),
    )
    def test_convert_types(self, converter, sa_type, field_type):
        prop = make_property(sa_type())
        field = converter.property2field(prop)
        assert type(field) is field_type

    def test_convert_Numeric(self, converter):
        prop = make_property(sa.Numeric(scale=2))
        field = converter.property2field(prop)
        assert type(field) is fields.Decimal
        assert field.places == decimal.Decimal((0, (1,), -2))

    def test_convert_ARRAY_String(self, converter):
        prop = make_property(postgresql.ARRAY(sa.String()))
        field = converter.property2field(prop)
        assert type(field) is fields.List
        inner_field = getattr(field, "inner", getattr(field, "container", None))
        assert type(inner_field) is fields.Str

    def test_convert_ARRAY_Integer(self, converter):
        prop = make_property(postgresql.ARRAY(sa.Integer))
        field = converter.property2field(prop)
        assert type(field) is fields.List
        inner_field = getattr(field, "inner", getattr(field, "container", None))
        assert type(inner_field) is fields.Int

    @pytest.mark.parametrize(
        "array_property",
        (
            pytest.param(make_property(sa.ARRAY(sa.Enum(CourseLevel))), id="sa.ARRAY"),
            pytest.param(
                make_property(postgresql.ARRAY(sa.Enum(CourseLevel))),
                id="postgresql.ARRAY",
            ),
        ),
    )
    def test_convert_ARRAY_Enum(self, converter, array_property):
        field = converter.property2field(array_property)
        assert type(field) is fields.List
        inner_field = field.inner
        assert type(inner_field) is fields.Enum

    @pytest.mark.parametrize(
        "array_property",
        (
            pytest.param(
                make_property(sa.ARRAY(sa.Float, dimensions=2)), id="sa.ARRAY"
            ),
            pytest.param(
                make_property(postgresql.ARRAY(sa.Float, dimensions=2)),
                id="postgresql.ARRAY",
            ),
        ),
    )
    def test_convert_multidimensional_ARRAY(self, converter, array_property):
        field = converter.property2field(array_property)
        assert type(field) is fields.List
        assert type(field.inner) is fields.List
        assert type(field.inner.inner) is fields.Float

    def test_convert_one_dimensional_ARRAY(self, converter):
        prop = make_property(postgresql.ARRAY(sa.Float, dimensions=1))
        field = converter.property2field(prop)
        assert type(field) is fields.List
        assert type(field.inner) is fields.Float

    def test_convert_TSVECTOR(self, converter):
        prop = make_property(postgresql.TSVECTOR)
        with pytest.raises(ModelConversionError):
            converter.property2field(prop)

    def test_convert_default(self, converter):
        prop = make_property(sa.String, default="ack")
        field = converter.property2field(prop)
        assert field.required is False

    def test_convert_server_default(self, converter):
        prop = make_property(sa.String, server_default=sa.text("sysdate"))
        field = converter.property2field(prop)
        assert field.required is False

    def test_convert_autoincrement(self, models, converter):
        prop = models.Course.__mapper__.attrs.get("id")
        field = converter.property2field(prop)
        assert field.required is False

    def test_handle_expression_based_column_property(self, models, converter):
        """
        Tests ability to handle a column_property with a mapped expression value.
        Such properties should be marked as dump_only, and the type should be properly
        inferred.
        """
        prop = models.Student.__mapper__.attrs.get("course_count")
        field = converter.property2field(prop)
        assert type(field) is fields.Integer
        assert field.dump_only is True

    def test_handle_simple_column_property(self, models, converter):
        """
        Tests handling of column properties that do not derive directly from Column
        """
        prop = models.Seminar.__mapper__.attrs.get("label")
        field = converter.property2field(prop)
        assert type(field) is fields.String
        assert field.dump_only is True


class TestPropToFieldClass:
    def test_property2field(self):
        prop = make_property(sa.Integer())
        field = property2field(prop, instance=True)

        assert type(field) is fields.Int

        field_cls = property2field(prop, instance=False)
        assert field_cls is fields.Int

    def test_can_pass_extra_kwargs(self):
        prop = make_property(sa.String())
        field = property2field(
            prop, instance=True, metadata=dict(description="just a string")
        )
        assert field.metadata["description"] == "just a string"


class TestColumnToFieldClass:
    def test_column2field(self):
        column = sa.Column(sa.String(255))
        field = column2field(column, instance=True)

        assert type(field) is fields.String

        field_cls = column2field(column, instance=False)
        assert field_cls is fields.String

    def test_can_pass_extra_kwargs(self):
        column = sa.Column(sa.String(255))
        field = column2field(
            column, instance=True, metadata=dict(description="just a string")
        )
        assert field.metadata["description"] == "just a string"

    def test_uuid_column2field(self):
        class UUIDType(sa.types.TypeDecorator):
            python_type = uuid.UUID
            impl = sa.BINARY(16)

        column = sa.Column(UUIDType)
        assert issubclass(column.type.python_type, uuid.UUID)  # Test against test check
        assert hasattr(column.type, "length")  # Test against test check
        assert column.type.length == 16  # Test against test
        field = column2field(column, instance=True)

        uuid_val = uuid.uuid4()
        assert field.deserialize(str(uuid_val)) == uuid_val


class TestFieldFor:
    def test_field_for(self, models):
        field = field_for(models.Student, "full_name")
        assert type(field) is fields.Str

        field = field_for(models.Student, "current_school")
        assert type(field) is Related

        field = field_for(models.Student, "full_name", field_class=fields.Date)
        assert type(field) is fields.Date

    def test_related_initialization_warning(self, models, session):
        with pytest.warns(
            DeprecationWarning,
            match="column` parameter is deprecated and will be removed in future releases. Use `columns` instead.",
        ):
            Related(column="TestCol")

    def test_related_initialization_with_columns(self, models, session):
        ret = Related(columns=["TestCol"])
        assert len(ret.columns) == 1
        assert ret.columns[0] == "TestCol"
        ret = Related(columns="TestCol")
        assert isinstance(ret.columns, list)
        assert len(ret.columns) == 1
        assert ret.columns[0] == "TestCol"

    def test_field_for_can_override_validators(self, models, session):
        field = field_for(
            models.Student, "full_name", validate=[validate.Length(max=20)]
        )
        assert len(field.validators) == 1
        validator = cast("validate.Length", field.validators[0])
        assert validator.max == 20

        field = field_for(models.Student, "full_name", validate=[])
        assert field.validators == []

    def tests_postgresql_array_with_args(self, Base: type):
        # regression test for #392
        class ModelWithArray(Base):
            __tablename__ = "model_with_array"
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            bar: Mapped[list[str]] = mapped_column(postgresql.ARRAY(String))

        field = field_for(ModelWithArray, "bar", dump_only=True)
        assert type(field) is fields.List
        assert field.dump_only is True
