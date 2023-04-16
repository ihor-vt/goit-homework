from PA_MongoDB.src.addressbook import main as run_app
from PA_MongoDB.src.create_fake_data import create_contact

'''
For a successful launch, you need to run Docker MongoDB
docker run -d -p 27017:27017 --name mongo_app mongo
'''

if __name__ == '__main__':
    create_contact(5)  # When you need to fill the database with fake contacts
    run_app()
