from aio_pika import connect_robust, RobustConnection, ExchangeType, Channel, Exchange, Queue, IncomingMessage, Message
from asyncio import create_task, sleep
from loguru import logger

from app.config import RabbitConfig
from app.entities import BaseModel, RabbitQueue, RabbitExchange, RabbitMessageType
from app.transport.rabbit.receive_notifications import receive_notifications
from app.transport.rabbit.receive_data import receive_data


class RabbitClient:
    def __init__(self, config: RabbitConfig) -> None:
        logger.info('Rabbit initialization...')

        self.config: RabbitConfig = config if type(config) is RabbitConfig else RabbitConfig(config)
        self.connection: RobustConnection = None
        self.channel: Channel = None
        self.notification_exchange: Exchange = None
        self.data_request_exchange: Exchange = None
        self.data_exchange: Exchange = None
        self.notification_queue: Queue = None
        self.data_queue: Queue = None

        create_task(self._start())
    
    async def _start(self):
        logger.info('Rabbit starting...')

        try:
            self.connection = await connect_robust(
                host=self.config.HOST,
                port=self.config.PORT,
                login=self.config.USER,
                password=self.config.PASSWORD,
                ssl=self.config.SECURE,
            )

            async with self.connection:
                self.channel = await self.connection.channel()
                
                async with self.channel:
                    self.notification_exchange = await self.channel.declare_exchange(RabbitExchange.notification.value, ExchangeType.DIRECT, durable=True)
                    self.data_request_exchange = await self.channel.declare_exchange(RabbitExchange.data_request.value, ExchangeType.DIRECT, durable=True)
                    self.data_exchange = await self.channel.declare_exchange(RabbitExchange.data.value, ExchangeType.FANOUT, durable=True)

                    self.notification_queue = await self.channel.declare_queue(RabbitQueue.notification.value)
                    self.data_queue = await self.channel.declare_queue(RabbitQueue.data.value)
                    
                    await self.notification_queue.bind(self.notification_exchange, routing_key=RabbitQueue.notification.value)
                    await self.data_queue.bind(self.data_exchange, routing_key=RabbitQueue.data_request.value)

                    await self.notification_queue.consume(self._receive_delivery_func(receive_notifications))
                    await self.data_queue.consume(self._receive_delivery_func(receive_data))

                    logger.info('Rabbit started')

                    await self.send_message(None, RabbitExchange.data_request, RabbitQueue.data_request, RabbitMessageType.data)

                    while True:
                        await sleep(10)

        except KeyboardInterrupt:
            ...
        except Exception as e:
            logger.exception(e)
            raise

        logger.info('Rabbit stopped')
    
    async def send_message(self, messge: BaseModel | None, exchange: RabbitExchange, routing_key: RabbitQueue, type: RabbitMessageType):
        body = messge.model_dump_json().encode() if messge else b''

        match exchange:
            case RabbitExchange.data_request:
                logger.info('Sending a request for data')
                m = await self.data_request_exchange.publish(Message(
                    body=body,
                    type=type.value,
                    reply_to=RabbitQueue.data.value,
                ), routing_key=routing_key)

                logger.info('Request for data sent')
            
            case _:
                ...
    
    @staticmethod
    def _receive_delivery_func(handler):
        from app.container import get_container
        container = get_container()

        async def receive_delivery(message: IncomingMessage) -> None:
            async with message.process():
                try:
                    logger.info(f'New delivery. Type: {message.type}. Body: {message.body}')
                    await handler(container, message)
                except Exception as e:
                    logger.exception(e)
                    await message.nack(requeue=False)

        return receive_delivery
