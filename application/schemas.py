import application.db_firestore as db
import graphene
from graphene import ObjectType, Mutation, String, Int, Field, List, Enum
from app import app
import google.cloud.firestore_v1.base_document as doc


class CollectionsTypeSchema(graphene.Enum):
    DOCUMENT = "DOCUMENT"
    FIELD = "FIELD"
    COLLECTION = "COLLECTION"


class CRUDEnum(graphene.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


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


class UpdateCollection(Mutation):
    class Arguments:
        collection_name = String()
        document_id = String()
        field_name = String()
        field_value = String()
        crud_action = CRUDEnum()

    gcpField = graphene.Field(GcpField)

    def mutate(
        self,
        info,
        collection_name,
        document_id,
        field_name,
        field_value,
        crud_action: CRUDEnum,
    ):
        app.logger.info("Updating collection %s, %s", collection_name, crud_action)
        if crud_action == CRUDEnum.CREATE or crud_action == CRUDEnum.UPDATE:
            update_dict = {field_name: field_value}
            app.logger.info(
                "Sending update dict %s to document %s", update_dict, document_id
            )

            doc_ref = db.get_document_ref(collection_name, document_id)
            doc = doc_ref.get()
            if doc.exists:
                db.update_document(doc_ref, update_dict)
                gcpField = GcpField(
                    field_name, CollectionsTypeSchema.FIELD.value, document_id
                )
            else:
                gcpField = None
        elif crud_action == CRUDEnum.DELETE:
            app.logger.info(
                "Deleting %s field from document %s", field_name, document_id
            )

            doc_ref = db.get_document_ref(collection_name, document_id)
            doc = doc_ref.get()
            if doc.exists:
                db.delete_field(doc_ref, field_name)
                gcpField = GcpField(
                    field_name, CollectionsTypeSchema.FIELD.value, document_id
                )
        else:
            raise ValueError("Invalid CRUD Action")
        return UpdateCollection(gcpField)


def create_schema():
    fields = List(GcpField)
    updateCollection = UpdateCollection.Field()

    def make_resolver(rec_name, rec_cls):
        def resolver(self, info):
            return show_collection("dev_col1", 1)

        resolver.__name__ = f"resolve_{rec_name}"
        return resolver

    fields_dict = {}
    fields_dict["fields"] = fields
    fields_dict["resolve_fields"] = make_resolver("fields", fields)

    Query = type("Query", (graphene.ObjectType,), fields_dict,)

    fields_dict = {}
    fields_dict["updateCollection"] = UpdateCollection.Field()
    Mutation = type("Mutation", (graphene.ObjectType,), fields_dict,)
    return graphene.Schema(query=Query, mutation=Mutation)


schema = create_schema()
