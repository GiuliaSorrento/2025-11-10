from dataclasses import dataclass

from model.order import Order


@dataclass
class Arco:
    ordine1: Order
    ordine2: Order
    peso: float
