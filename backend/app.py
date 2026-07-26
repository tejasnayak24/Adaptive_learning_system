from flask import Flask

from database.database import engine
from database.models import Base


from authentication.register import register_bp
from authentication.login import login_bp



app = Flask(__name__)


Base.metadata.create_all(bind=engine)



app.register_blueprint(register_bp)

app.register_blueprint(login_bp)



@app.route("/")
def home():

    return {

        "message":
        "Adaptive Learning Backend Running"

    }



if __name__ == "__main__":

    app.run(debug=True)