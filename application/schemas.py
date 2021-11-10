import application.db_firestore as db
import graphene
from graphene import ObjectType, Mutation, String, Int, Field, List, Enum
from app import app


class CollectionsTypeSchema(graphene.Enum):
    FIELD = "FIELD"
    COLLECTION = "COLLECTION"


class GcpField(ObjectType):
    name = String()
    type = CollectionsTypeSchema()

    def __init__(self, name, _type):
        self.name = name
        self.type = _type

    def resolve_name(self, info):
        return "a"

    def resolve_type(self, info):
        return "b"


def show_collection(name: str, depth: int):
    docs = db.get_collection(name)
    fields = []
    for doc in docs:
        fields_dict = doc.to_dict()
        # Get collections
        for collection_ref in doc.reference.collections():
            fields.append(
                GcpField(collection_ref.id, CollectionsTypeSchema.COLLECTION.value)
            )
            # pass
        # Get fields
        for k, v in fields_dict.items():
            fields.append(GcpField(k, CollectionsTypeSchema.FIELD.value))
    return fields


def create_schema():
    fields = Field(GcpField)

    def resolve_fields(self, info):
        flds = show_collection("dev_col2", 1)
        return flds[0]

    def make_resolver(rec_name, rec_cls):
        def resolver(self, info):
            return f"Record is {rec_name}"

        resolver.__name__ = f"resolve_{rec_name}"
        return resolver

    fields_dict = {}
    fields_dict["fields"] = graphene.String()
    fields_dict["resolve_fields"] = resolve_fields
    fields = show_collection("dev_col1", 1)
    #    for f in fields:
    #        fields_dict[str(f)] = graphene.String()
    #        fields_dict[f"resolve_{str(f)}"] = make_resolver(str(f), String)
    Query = type("Query", (graphene.ObjectType,), fields_dict,)
    return graphene.Schema(query=Query)


schema = create_schema()
