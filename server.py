from app import app

from app.controllers import pets, users
from app.api_controllers import pets_api

if __name__=="__main__":
    app.run(debug=True)

# think you're so smart?
    