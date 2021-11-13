import application.db_firestore as db
import graphene
from graphene import ObjectType, Mutation, String, Int, Field, List, Enum
from app import app
import google.cloud.firestore_v1.base_document as doc


class CollectionsTypeSchema(graphene.Enum):
    DOCUMENT = "DOCUMENT"
    FIELD = "FIELD"
    COLLECTION = "COLLECTION"


class GcpField(ObjectType):
    parents = String()
    name = String()
    type = CollectionsTypeSchema()

    def __init__(self, name: str, _type: graphene.Enum, parents: str):
        self.name = name
        self.type = _type
        self.parents = parents

    def resolve_name(self, info):
        return self.name

    def resolve_type(self, info):
        return self.type

    def resolve_parents(self, info):
        return self.parents


def show_document_fields(doc):
    app.logger.info("Call show_document_fields doc.id:%s", doc.id)
    fields = []
    fields_dict = doc.to_dict()
    for collection_ref in doc.reference.collections():
        app.logger.info(
            "loop collections  in doc.id=%s collection_ref=%s",
            doc.id,
            collection_ref.id,
        )
        fields.append(
            GcpField(collection_ref.id, CollectionsTypeSchema.COLLECTION.value, doc.id)
        )
        documents: doc.DocumentSnapshot = collection_ref.get()
        for subdoc in documents:
            fields += show_document_fields(subdoc)
    # Get fields
    for k, v in fields_dict.items():
        app.logger.info("loop field_dict  k=%s v=%s", k, v)
        fields.append(GcpField(k, CollectionsTypeSchema.FIELD.value, doc.id))
    return fields


def show_collection(name: str, depth: int):
    docs = db.get_collection(name)
    fields = []
    app.logger.info("Call show_collection name:%s depth:%s", name, depth)
    for doc in docs:
        app.logger.info("loop docs doc.id=%s", doc.id)
        fields.append(GcpField(doc.id, CollectionsTypeSchema.DOCUMENT.value, name))
        fields += show_document_fields(doc)
    return fields


def create_schema():
    fields = List(GcpField)

    def make_resolver(rec_name, rec_cls):
        def resolver(self, info):
            return show_collection("dev_col1", 1)

        resolver.__name__ = f"resolve_{rec_name}"
        return resolver

    fields_dict = {}
    fields_dict["fields"] = fields
    fields_dict["resolve_fields"] = make_resolver("fields", fields)
    # fields = show_collection("dev_col1", 1)
    #    for f in fields:
    #        fields_dict[str(f)] = graphene.String()
    #        fields_dict[f"resolve_{str(f)}"] = make_resolver(str(f), String)
    Query = type("Query", (graphene.ObjectType,), fields_dict,)
    return graphene.Schema(query=Query)


schema = create_schema()
