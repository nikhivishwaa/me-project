from functools import reduce

class Wall:
    def __init__(self, width:float|int|None = None, 
                height:float|int|None = None, area:float|int = 0,
                temperature:int|float=30, thermal_conductivity:float=0.5, 
                thickness:float=0.127)->None:
        self.width = width
        self.height = height
        self.area = area
        self.thermal_conductivity = thermal_conductivity
        self.thickness = thickness
        self.temperature_difference = temperature

    @property
    def area(self)->float|int:
        if self.height and self.width:
            return self.height * self.width

        else:
            return self.area_by_user

    @area.setter
    def area(self, area:int|float)->None:
        self.area_by_user = area

    @property
    def temperature_difference(self)->float|int:
        return self.temperature - 20

    @temperature_difference.setter
    def temperature_difference(self, temperature:int|float)->None:
        self.temperature = temperature

    @property
    def heat_gain(self):
        result = (self.area * self.temperature_difference * self.thermal_conductivity) / self.thickness
        result = round(result, 2)
        return result

    def __add__(self, other)->float:
        return self.heat_gain + other.heat_gain

class HeatGainThroughWalls:
    def __init__(self, walls:list)->None:
        self.walls = []
        for i in walls:
            wall = Wall(**i)
            self.walls.append(wall)
    @property
    def total_heat_gain(self)->float:
        result = 0
        for i in self.walls:
            result += i.heat_gain

        return result

    def __str__(self)->str:
        return f"{self.total_heat_gain:.2f} W"


class Window(Wall):
    def __init__(self, **kwargs)->None:
        kwargs['thermal_conductivity'] = .15
        kwargs['thickness'] = 0.004

        super().__init__(**kwargs)

class HeatGainThroughWindows:
    def __init__(self, windows:list)->None:
        self.windows = []
        for i in windows:
            window = Window(**i)
            self.windows.append(window)

    @property
    def total_heat_gain(self)->float:
        result = 0
        for i in self.windows:
            result += i.heat_gain

        return result

    def __str__(self)->str:
        return f"{self.total_heat_gain : .2f} W"

class HeatGainThroughRoof:
    def __init__(self, roof_dict:dict)->None:
            self.roof = Wall(**roof_dict)

    @property
    def total_heat_gain(self)->float:
        return self.roof.heat_gain

    def __str__(self)->str:
        return f"{self.total_heat_gain : .2f} W"


class HeatGainFromOccupants:
    def __init__(self, occupants:int=0)->None:
            self.occupants = occupants

    @property
    def total_heat_gain(self)->int:
        return self.occupants * 100

    def __str__(self)->str:
        return f"{self.total_heat_gain} W"

class HeatGainFromEquipments:
    def __init__(self, equipments:dict)->None:
            self.equipments = equipments
            self.power = {'computer':200,
                          'led_tubelight':20,
                          'fans':75}

    @property
    def total_heat_gain(self)->int:
        heat_gain = 0
        for equipment, qty in self.equipments.items():
            heat_gain += self.power[equipment] * qty

        return heat_gain

    def __str__(self)->str:
        return f"{self.total_heat_gain} W"

class TotalHeatLoad:
    def __init__(self, heatload:dict)->None:
        self.heatload = heatload
        self.heat_gain_classes = {'walls': HeatGainThroughWalls,
                                    'windows':HeatGainThroughWindows,
                                    'roof':HeatGainThroughRoof,
                                    'occupants':HeatGainFromOccupants,
                                    'equipments':HeatGainFromEquipments}

        self.heat_gain_objects = dict()
        self.total_heatload = 0.0

        for source, heatvalues in self.heatload.items():
            self.heat_gain_objects[source] = self.heat_gain_classes[source](heatvalues)
            self.total_heatload += self.heat_gain_objects[source].total_heat_gain

    def tons_of_airconditioning(self)->str:
        conversion_coefficient = 3517
        self.air_conditioning_required = self.total_heatload / conversion_coefficient
        result = f"{round(self.air_conditioning_required, 2)} tons"
        return result

    def __str__(self)->str:
        return f"{self.total_heatload:.2f} W"


if __name__ == '__main__':
    x = {'walls': [{"height":9.64, "width":3.66, "temperature":38},
                    {"height":9.64, "width":3.66, "temperature":30},
                    {"height":8, "width":3.66, "temperature":30},
                    {"height":8, "width":3.66, "temperature":30}],
         'windows':[{"area":3.902, "temperature":30}],
         'roof':{"area":74, "temperature":30},
         'occupants':32,
         'equipments':{'computer':32,
                          'led_tubelight':15,
                          'fans':6}}

    y = TotalHeatLoad(x)
    print(y)
    print(y.tons_of_airconditioning())
    # y = HeatGainThroughRoof(x['roof'])
    # y = HeatGainFromEquipments(x['equipments'])
    # y = HeatGainThroughWalls(x['walls'])
    # print(y)

    