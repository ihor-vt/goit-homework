import pika
import time

from models.models import Contacts


def send_sms(email, first_name, last_name, company_numper='+380111111111'):
    pass


def callback(ch, method, properties, body):
    _id = body.decode()
    contact, = Contacts.objects(id=_id, completed_sms=False)
    print()
    if contact:
        phone = contact.cell_phone
        first_name = contact.first_name
        last_name = contact.last_name
        send_sms(phone, first_name, last_name, company_numper='+380111111111')
        Contacts.objects(id=_id).update_one(set__completed_sms=True)
        time.sleep(1)
        print(f" [x] Done SMS: {first_name} {last_name}: {phone}")
    ch.basic_ack(delivery_tag=method.delivery_tag)



def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='marketing_campain', durable=True)
    channel.basic_qos(prefetch_size=0)
    channel.basic_consume(queue='marketing_campain', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    main()