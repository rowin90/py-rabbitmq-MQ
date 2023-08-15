
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
#  创建交换机
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 创建队列
result = channel.queue_declare("",exclusive=True)
queue_name = result.method.queue

# 绑定交换机
channel.queue_bind(exchange='logs',
                   queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 确定定义监听
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听
channel.start_consuming()
