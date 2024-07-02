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

        for i in (self.area, self.thermal_conductivity, self.thickness):
            if i < 0:
                raise ValueError("all values must be positive.")

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
        if self.temperature < 20:
            raise ValueError("Temperature must be greater than or equal to 20.")
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
    """calculates the heat gain by each 4 walls."""
    def __init__(self, walls:list)->None:
        self.walls = []
        for i in walls:
            wall = Wall(**i)
            self.walls.append(wall)

        self.heat_gain_by_each = dict() # containing heat gain from each 4 walls

    @property
    def total_heat_gain(self)->float:
        result = 0
        for index, wall in enumerate(self.walls, 1):
            self.heat_gain_by_each[f'wall-{index}'] = wall.heat_gain
            result += self.heat_gain_by_each[f'wall-{index}']

        return result

    def detailed_heat_gain(self)->dict:
        """return the total heat gain along with calulated heat gain of each 4 walls."""
        detail_data = {
            'total_heat_gain': f'{self.total_heat_gain: .2f} W'.strip(),
            'heat_gain_by_each_wall':  {key:f'{value: .2f} W'.strip() for key, value in self.heat_gain_by_each.items()},
        }

        return detail_data

    def __str__(self)->str:
        return f"{self.total_heat_gain:.2f} W"


class Window(Wall):
    """extends the wall's class funtionality by changing the default values of thermal_conductivity and thickness """
    def __init__(self, **kwargs)->None:
        kwargs['thermal_conductivity'] = .15
        kwargs['thickness'] = 0.004

        super().__init__(**kwargs)

class HeatGainThroughWindows:
    """calculates the heat gain by one or more windows of the house or workplace."""
    def __init__(self, windows:list)->None:
        self.windows = []
        self.heat_gain_by_each = dict()
        for i in windows:
            window = Window(**i)
            self.windows.append(window)

    @property
    def total_heat_gain(self)->float:
        if len(self.windows) > 1:   # have multiple window
            result = 0
            for index, window in enumerate(self.windows, 1):
                self.heat_gain_by_each[f'window-{index}'] = window.heat_gain
                result += self.heat_gain_by_each[f'window-{index}']

            return result

        # otherwise if only one window is available
        elif len(self.windows):
            self.heat_gain_by_each['window-1'] = self.windows[0].heat_gain
            return self.heat_gain_by_each['window-1']

        return 0.0 # no window

    def detailed_heat_gain(self)->dict:
        """return the total heat gain along with all windows calulated heat gain"""
        detail_data = {
            'total_heat_gain': f'{self.total_heat_gain: .2f} W'.strip(),
            'heat_gain_by_each_window':  {key:f'{value: .2f} W'.strip() for key, value in self.heat_gain_by_each.items()},
        }

        return detail_data

    def __str__(self)->str:
        return f"{self.total_heat_gain : .2f} W"

class HeatGainThroughRoof:
    """calculates the heat gain by the roof of house or workplace."""
    def __init__(self, roof_dict:dict)->None:
        if len(roof_dict) and roof_dict.get('area', None) is None:
            # add area to roof_dict and remove length and breadth
            roof_dict['area'] = roof_dict['length'] * roof_dict['breadth']
            roof_dict.pop('length')
            roof_dict.pop('breadth')

        self.roof = Wall(**roof_dict)

    @property
    def total_heat_gain(self)->float:
        return self.roof.heat_gain

    def __str__(self)->str:
        return f"{self.total_heat_gain : .2f} W"


class HeatGainFromOccupants:
    """calculates the heat gain by occupants / members of a workplace or home."""
    def __init__(self, occupants:int=0)->None:
            self.occupants = occupants

    @property
    def total_heat_gain(self)->int:
        return self.occupants * 100

    def __str__(self)->str:
        return f"{self.total_heat_gain} W"

class HeatGainFromEquipments:
    """calculates the heat gain by various equipments such as computer, led_tubelight and fans."""
    def __init__(self, equipments:dict)->None:
            self.equipments = equipments
            self.power = {'computer':200,
                          'led_tubelight':20,
                          'fans':75}
            self.heat_gain_by_each = dict()

    @property
    def total_heat_gain(self)->int:
        result = 0
        for equipment, qty in self.equipments.items():
            self.heat_gain_by_each[equipment] = self.power[equipment] * qty
            result += self.heat_gain_by_each[equipment]

        return result

    def detailed_heat_gain(self)->dict:
        """return the total heat gain along with calulated heat gain by each equipment."""
        detail_data = {
            'total_heat_gain': f'{self.total_heat_gain: .2f} W'.strip(),
            'heat_gain_by_each_equipment':  {key:f'{value: .2f} W'.strip() for key, value in self.heat_gain_by_each.items()},
        }

        return detail_data

    def __str__(self)->str:
        return f"{self.total_heat_gain} W"

class TotalHeatLoad:
    def __init__(self, heatload:dict)->None:
        self.heatload = heatload
        self.heat_gain_classes = {
            'walls': HeatGainThroughWalls,
            'windows':HeatGainThroughWindows,
            'roof':HeatGainThroughRoof,
            'occupants':HeatGainFromOccupants,
            'equipments':HeatGainFromEquipments
        }

        self.detailed_heat_load = dict()
        self.heat_gain_objects = dict()
        self.total_heatload = 0.0

        for source, heatvalues in self.heatload.items():
            self.heat_gain_objects[source] = self.heat_gain_classes[source](heatvalues)
            self.total_heatload += self.heat_gain_objects[source].total_heat_gain
            if source in ('walls','windows','equipments'):
                self.detailed_heat_load[source] = self.heat_gain_objects[source].detailed_heat_gain()

            else:
                self.detailed_heat_load[source] = str(self.heat_gain_objects[source]).strip() # getting string representation

    def tons_of_airconditioning(self)->str:
        conversion_coefficient = 3517
        self.air_conditioning_required = self.total_heatload / conversion_coefficient
        result = f"{round(self.air_conditioning_required, 2)} tons"
        return result

    def __str__(self)->str:
        return f"{self.total_heatload:.2f} W"

class PermissionedTotalHeatLoad(TotalHeatLoad):
    def __init__(self, heatload:dict, permission:list)->None:
        permitted_heat_load = dict()
        for source in permission:
            if heatload.get(source, None) is not None:
                print(source)
                permitted_heat_load[source] = heatload[source]

        if not len(permitted_heat_load):
            self.success = False
            self.message = "No permitted heat sources found"

        else:
            try:
                super().__init__(permitted_heat_load)
                self.success = True
                self.message = "successfully calculated heat load"

            except Exception as e:
                self.success = False
                self.message = str(e)

    def get_result(self):
        if self.success:
            result = {
                'success': self.success,
                'message': self.message,
                "data": {
                    'total_heat_load': self.__str__(),
                    'detailed_heat_load': self.detailed_heat_load,
                    'air_conditioning': self.tons_of_airconditioning()
                }
            }

            if self.air_conditioning_required < 0 or self.total_heatload < 0:
                result['success'], self.success = False, False
            
            return result
        else:
            result = {
                'success': self.success,
                'message': self.message
            }
            return result

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

    