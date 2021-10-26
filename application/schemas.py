import application.db_firestore
import graphene
from graphene import ObjectType, Mutation, String, Int, Field, List, Enum


class Collection(ObjectType):
    id = String()
    title = String()
    description = String()

    def __init__(self, Collections_dict, ident):
        self.id = ident
        for keys, values in Collections_dict.items():
            # app.logger.info(keys + " " + str(values))
            setattr(self, keys, values)

    def resolve_id(self, info):
        return f"{self.id}"

    def resolve_title(self, info):
        return f"{self.title}"

    def resolve_description(self, info):
        return f"{self.description}"


class Query(ObjectType):
    fs_collection = graphene.Field(Collection, ident=String())
    fs_collections = List(Collection)

    def resolve_fs_collection(self, info, ident):
        fs_col = Collection(
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
