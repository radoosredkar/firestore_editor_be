import flask
from app import app
from flask_graphql import GraphQLView
from application import schemas
from config import settings
import application.db_firestore as db
import application.schemas

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schemas.schema, graphiql=True),
)


@app.route("/")
def root():
    return f"App is online ... (environment={settings.environment})"
    flask.g.root_collection = "dev_col1"


@app.route("/reload")
def reload():
    schemas.create_schema("dev_col2")
    return "Schema reloaded OK"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8081)
