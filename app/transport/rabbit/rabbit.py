from aio_pika import connect_robust, RobustConnection, ExchangeType, Channel, Exchange, Queue, IncomingMessage
from asyncio import create_task, sleep
from loguru import logger

from app.config import RabbitConfig
from app.transport.rabbit.receive_notifications import receive_notifications


class RabbitClient:
    notification_exchange_name = 'notification_exchange'
    notification_queue_name = 'notification_queue'


    def __init__(self, config: RabbitConfig) -> None:
        logger.info('Rabbit initialization...')

        self.config: RabbitConfig = config if type(config) is RabbitConfig else RabbitConfig(config)
        self.connection: RobustConnection = None
        self.channel: Channel = None
        self.notification_exchange: Exchange = None
        self.notification_queue: Queue = None

        create_task(self._start())
    
    async def _start(self):
        logger.info('Rabbit running...')

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
                    self.exchange = await self.channel.declare_exchange(self.notification_exchange_name, ExchangeType.DIRECT, durable=True)
                    self.queue = await self.channel.declare_queue(self.notification_queue_name)
                    
                    await self.queue.bind(self.exchange, routing_key=self.notification_queue_name)

                    await self.queue.consume(self._receive_delivery_func(receive_notifications), no_ack=True)

                    while True:
                        await sleep(10)
        
        except KeyboardInterrupt:
            ...
        except Exception:
            raise

        logger.info('Rabbit stopped')
    
    async def send_message():
        ...
    
    @staticmethod
    def _receive_delivery_func(handler):
        from app.container import get_container
        container = get_container()

        async def receive_delivery(message: IncomingMessage) -> None:
            try:
                logger.info(f'New delivery. Type: {message.type}. Size: {message.body_size}')
                await handler(container, message)
            except Exception as e:
                logger.exception(e)
        
        return receive_delivery
