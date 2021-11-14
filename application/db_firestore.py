from app import app
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

if os.environ.get("DEVELOPMENT"):
    cred = credentials.Certificate(
        "firebasegui-firebase-adminsdk-lpxg1-236a6b0926.json"
    )
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    cred = credentials.Certificate(
        "firebasegui-firebase-adminsdk-lpxg1-236a6b0926.json"
    )
    firebase_admin.initialize_app(cred)
    db = firestore.client()

def get_collections():
    app.logger.info(db.__dict__)
    return db.collections()


def get_collection(collection_name):
    app.logger.info(collection_name)
    return db.collection(collection_name).stream()


def get_document_ref(collection_name, doc_id):
    # app.logger.info("%s %s", collection_name, doc_id)
    doc_ref = db.collection(collection_name).document(f"{doc_id}")
    return doc_ref


def insert_document(doc_ref, json_data):
    app.logger.info(f"Inserting document to {doc_ref}")
    app.logger.info(f"Document {json_data}")
    doc_ref.set(json_data)


def update_document(doc_ref, field_dict: dict):
    # app.logger.debug(f"Updating document {doc_ref}")
    if doc_ref.get().exists:
        app.logger.debug(f"Applying updates {field_dict}")
        doc_ref.update(field_dict)
    else:
        raise FileNotFoundError(f"Document not found")


def delete_document(doc_ref):
    # app.logger.debug(f"Updating document {doc_ref}")
    if doc_ref.get().exists:
        app.logger.debug("Deleting document")
        doc_ref.delete()
    else:
        raise FileNotFoundError("Document not found")


def get_latest_refresh(collection_name):
    app.logger.info(collection_name)
    now = datetime.datetime.now()
    document_id = now.strftime("%Y%m%d")
    latest_date = None

    result_stream = (
        db.collection(collection_name).document(f"refresh_{document_id}")
        # .order_by("datetime", direction="DESCENDING")
        # .limit(1)
        .get()
    )

    if result_stream.exists:
        whole_day_data = result_stream.to_dict()
        # Get latest hour
        if whole_day_data:
            fields = list(whole_day_data)
            fields.sort(key=float)
            app.logger.info(fields)
            latest_date = whole_day_data[fields[-1]]

    return latest_date
