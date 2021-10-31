import application.db_firestore as db
import graphene
from graphene import ObjectType, Mutation, String, Int, Field, List, Enum
from app import app


class FsColl(ObjectType):
    id = String()
    title = String()
    value = String()
    description = String()

    #    def __init__(self, coll_dict, ident):
    #        self.id = ident
    #        for keys, values in coll_dict.items():
    #            # app.logger.info(keys + " " + str(values))
    #            setattr(self, keys, values)
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            app.logger.info(f"{k}->{v}")
            setattr(self, k, v)

    def resolve_id(self, info):
        return f"{self.id}"

    def resolve_title(self, info):
        return f"{self.title}"

    def resolve_value(self, info):
        return f"{self.value}"

    def resolve_description(self, info):
        return f"{self.description}"


class Query(ObjectType):
    fs_collection = graphene.Field(FsColl)
    fs_collections = List(FsColl)
    fs_collection_fields = List(FsColl)

    def resolve_fs_collection_fields(self, info):
        coll = FsColl(
            coll_dict={"title": "title1", "description": "description1"}, ident=1
        )
        coll1 = FsColl(
            coll_dict={"title": "title2", "description": "description2"}, ident=2
        )
        fs_coll_ref = db.get_collection("dev_col1")
        fields = []
        for field in fs_coll_ref:
            fields_dict = field.to_dict()
            for k, v in fields_dict.items():
                fields.append(FsColl(id=1, title=k, description=fields_dict))
        return fields

    def resolve_fs_collection(self, info, ident):
        fs_col = FsColl(
            {"id": 2, "title": "title123", "description": "description123"}, "1"
        )
        return fs_col
        # doc_ref = db_firestore.get_document_ref(settings.collections.Collections, ident)
        # return Collection(doc_ref.get().to_dict(), ident)

    def resolve_fs_collections(self, info):
        # Collections_ref = db.collection(Collections_collection_name)
        # docs = Collections_ref.stream()
        collections = []
        # for doc in docs:
        #    Collection_dict = doc.to_dict()
        #    # app.logger.info(Collection_dict)
        #    Collection = Collection(Collection_dict, doc.id)
        #    if Collection.archived == archived:
        #        Collections.append(Collection)
        for i in range(10):
            fs_col = Collection(
                {"id": i, "title": f"title{i}", "description": f"description{i}"}, "1"
            )
            collections.append(fs_col)
        return collections


schema = graphene.Schema(query=Query)
