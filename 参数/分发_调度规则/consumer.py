
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
#  创建队列
channel.queue_declare(queue='hello2', durable=True) # 若声明过，则换一个名字

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 确定定义监听
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

channel.basic_qos(prefetch_count=1)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听
channel.start_consuming()
