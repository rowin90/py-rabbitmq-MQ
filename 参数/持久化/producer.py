import pika

# 1. 链接 rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. 创建队列
channel.queue_declare(queue='hello2', durable=True) # 若声明过，则换一个名字

# 3. 向指定队列插入数据
channel.basic_publish(exchange='',  # 简单模式
                      routing_key='hello',  # 指定队列
                      body='hello 1111')
print('dsadad')
