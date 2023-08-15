
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
#  创建队列
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 确定定义监听
channel.basic_consume(queue='hello',
                      auto_ack=False,
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听
channel.start_consuming()
