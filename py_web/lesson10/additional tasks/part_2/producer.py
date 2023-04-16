import pika
from random import randint
from faker import Faker

from models.models import Contacts


fake = Faker()

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='spam_servise', exchange_type='direct')
    channel.queue_declare(queue='marketing_campain', durable=True)
    channel.queue_bind(exchange='spam_servise', queue='marketing_campain')

    for count in range(1, 30):
        contact = Contacts(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            cell_phone=fake.phone_number(),
            age=randint(18, 75)
        ).save()

        channel.basic_publish(
            exchange='spam_servise',
            routing_key='marketing_campain',
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    
    connection.close()

if __name__ == '__main__':
    main()