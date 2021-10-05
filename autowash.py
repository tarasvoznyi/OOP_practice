import dataclasses
from abc import ABC,abstractmethod

VEHICLES_ALLOWED_TYPES = ('bike', 'car', 'truck', 'bus')

WASH_LEVEL = {
    'Express': 0,
    'Inside': 1,
    'Outside': 2,
    'Complex': 3,
    'Full': 4,
    'Super': 5,
    'Shiny': 6
}
MAX_WASH_LVL = max(WASH_LEVEL.values())

class CarWashLux(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PepperWash(metaclass=CarWashLux):
    def __init__(self, workers, bikes=None, cars=None, buses=None, trucks=None):
        self.bikes = bikes
        self.cars = cars
        self.buses = buses
        self.trucks = trucks
        self.workers = workers

    @staticmethod
    def info():
        print(f'The PepperWash has the following types of vehicles: \n'
              f'- Bikes\n'
              f'- Cars\n'
              f'- Buses\n'
              f'- Trucks\n')

    def employee_info(self):
        print(f'Currently we have {len(self.workers)} workers and they are busy.')


    def daily_summery(self):
        vehicles_count = [x for x in [self.bikes, self.cars, self.buses, self.trucks] if x is not None ]
        print(f'Today we have such number of vehicles - {len(vehicles_count)}')


class VehicleMeta(ABC):
    def __init__(self, wash_type, vehicle_type, additional_service):
        self.wash_type = wash_type
        self._vehicle_type = vehicle_type
        self.additional_service = additional_service

    #@abstractmethod
    #def vehicle_type(self):
    #   raise NotImplementedError

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, vehicle_type):
        if vehicle_type in VEHICLES_ALLOWED_TYPES:
            self._vehicle_type = vehicle_type
            print(f'Your vehicle type is {self.vehicle_type}')
        else:
            raise Exception(f'Wrong type of vehicle. Not able to set {vehicle_type}')

    @abstractmethod
    def dirty_level(self):
        raise NotImplementedError


    @abstractmethod
    def is_clean(self):
        raise NotImplementedError

class Vehicle(VehicleMeta):
    def __init__(self, wash_type, vehicle_type, additional_service):
        self.clean_lvl = 0
        super().__init__(wash_type, vehicle_type, additional_service)



    def dirty_level(self):
        return WASH_LEVEL[self.wash_type]

    def clean(self):
         if  self.dirty_level() > self.clean_lvl:
             print('Now worker cleans vehicle')
             print(f'Wash level before cleaning - {self.clean_lvl}')
             self.clean_lvl += 1
             print(f'Wash level after cleaning - {self.clean_lvl}')



    def is_clean(self):
        return self.clean_lvl == self.dirty_level()




class WorkerMeta(ABC):
    def __init__(self, name, vehicle):
        self.name = name
        self.vehicle = vehicle

    @abstractmethod
    def check_dirty_lvl(self):
        raise NotImplementedError

    @abstractmethod
    def wash(self):
        raise NotImplementedError

    @abstractmethod
    def polish(self):
        raise NotImplementedError

class Worker(WorkerMeta):
    def __init__(self, name, vehicle):
        super().__init__(name, vehicle)


    def check_dirty_lvl(self):
        return f'Vehicle dirty level is {self.vehicle.dirty_level()}'

    def wash(self):
        while not self.vehicle.is_clean():
            self.vehicle.clean()
        print(f'{self.vehicle.vehicle_type} is clean')
        if self.vehicle.additional_service:
            self.polish()

    def polish(self):
        print(f'{self.vehicle.vehicle_type} polished')



bike_instance_0 = Vehicle('Outside', 'bike', True)
worker_instance_0 = Worker('John', bike_instance_0)
car_wash_instance = PepperWash(workers=[worker_instance_0], bikes=[bike_instance_0])

car_wash_instance.info()
car_wash_instance.daily_summery()
car_wash_instance.employee_info()

worker_instance_0.check_dirty_lvl()
worker_instance_0.wash()