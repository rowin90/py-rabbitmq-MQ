import pika

# 1. 链接 rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. 创建交换机
channel.exchange_declare(exchange='logs3',
                         exchange_type='topic')

# 3. 向指定交换机插入数据
message = "info: Hello World!"
channel.basic_publish(exchange='logs3',
                      routing_key='usa.weather',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
