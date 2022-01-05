# -*- coding: utf-8 -*-
from paydi_lib.worker import Worker
from src.workers.simple import Pos
from src.config import DefaultConfig
# Config consumer
"""
    - Config consumer
        [topic.group_id]: ClassHandler
"""
worker_config = {
    'test.group_id_1': Pos,

}


app = Worker(worker_config, DefaultConfig).run()