from enum import Enum


class RabbitExchange(str, Enum):
    notification = 'notification_exchange'
    data_request = 'wash_bonus_service'
    data = 'admins_exchange'


class RabbitQueue(str, Enum):
    notification = 'notification_queue'
    data_request = 'wash_bonus'
    data = 'bot_data_queue'


class RabbitMessageType(str, Enum):
    data = 'admin_service/data'
    organization_data = 'admin_service/organization'
    group_data = 'admin_service/server_group'
    wash_data = 'admin_service/wash_server'
    user_data = 'admin_service/admin_user'
