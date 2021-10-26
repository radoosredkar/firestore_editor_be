import flask
from app import app
from flask_graphql import GraphQLView
from application import schemas
from config import settings
import application.db_firestore as db

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schemas.schema, graphiql=True),
)


@app.route("/")
def root():
    return f"App is online ... (environment={settings.environment})"


@app.route("/test")
def test():
    colls = db.get_collections()
    coll = db.get_collection("dev_col2")
    rs = ""
    for c in colls:
        rs = rs + str((c.get()[0]))
    return rs


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8081)
