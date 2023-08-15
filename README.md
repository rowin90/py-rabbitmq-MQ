# 简单模式
```python
### 生产者
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

### 消费者

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

# 参数
### 应答
1. 默认的应答，是取出即销毁，无需确认
2. 如果要确保 ack 手动应答
    1. auto_ack=False
    2. ch.basic_ack(delivery_tag=method.delivery_tag)
```python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
#  创建队列
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动确认

# 确定定义监听
channel.basic_consume(queue='hello',
                      auto_ack=False, # 手动确认
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听
channel.start_consuming()

```
### 持久化参数
1. 创建队列的时候，就要声明是持久化的
2. 消费者和生产者都要设置，并且保持一致
3. 如果之前已经定义过queue队列，不能通过继续加参数 durable=True 来改变其属性，务必重新建一个新队列
```python

#声明queue
channel.queue_declare(queue='hello2', durable=True)  # 若声明过，则换一个名字
 
channel.basic_publish(exchange='',
                      routing_key='hello2',
                      body='Hello World!',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                          )
                      )
```
### 分发参数
1. 如果有多个消费者，默认分发规则是轮询
2. 如果看哪个空闲给哪个，消费者加入分发参数即可
```python

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

channel.basic_qos(prefetch_count=1)  # 分发规则

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听
channel.start_consuming()

```

# 交换机模式
- 先创建一个交换机 exchange
- 生产者推入消息到 交换机
- 消费者，建立队列，绑定对应的交换机
- 交换机推消息到，绑定该交换机上的 队列中

1. fanout 发布订阅模式。一个交换机，被多个消费队列绑定，可以一次消息推送到多份
2. direct 关键字。直接命中关键字的，routing_key，才会被推送
3. topic 通配符。命中通配符即可，匹配一些列的
    1. “通配符交换机”（Topic Exchange）将路由键和某模式进行匹配。此时队列需要绑定在一个模式上。符号“#”匹配一个或多个词，符号“*”仅匹配一个词。因此“audit.#”能够匹配到“audit.irs.corporate”，但是“audit.*”只会匹配到“audit.irs”。（这里与我们一般的正则表达式的“*”和“#”刚好相反，这里我们需要注意一下。）
