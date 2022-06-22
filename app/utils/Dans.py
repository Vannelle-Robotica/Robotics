from turtle import delay

from app.hardware.arduino import Arduino
from app.hardware.motors import Motors

direction = "rr"
Speed = 60


class Dans:

    def __init__(self):
        # Initialize Arduino connection
        print('Initializing Arduino connection')
        self.arduino = Arduino(0x8)

        # Initialize Motors
        self.motors = Motors()

    def draai_in_het_rond(self, direction, Speed):
        self.motors.move(direction, Speed)

    def stamp_met_je_voeten_op_de_grond(self):
        self.arduino.toggle_wheels()

    def zwaai_je_armen_in_de_lucht(self):
        self.arduino.toggle_arm()

    def ga_zitten_met_een_zucht(self):
        self.arduino.toggle_wheels()

    def voorwielen_toggle(self):
        self.arduino.toggle_wheels_front()

    def achterwielen_toggle(self):
        self.arduino.toggle_wheels_back()

    def raak_de_rand(self, direction, Speed):
        for x in range(5):
            self.motors.move(direction, Speed)
        delay(2000)
        direction = "b"
        for x in range(5):
            self.motors.move(direction, Speed)

    def refrein(self, direction, Speed):
        # het refrein duurt 12-13 seconde lang
        for x in range(5):
            self.draai_in_het_rond(direction, Speed)  # ... sec
        for x in range(3):
            self.stamp_met_je_voeten_op_de_grond()  # ... sec
        for x in range(2):
            self.zwaai_je_armen_in_de_lucht()  # ... sec
        for x in range(1):
            self.ga_zitten_met_een_zucht()  # ... sec
        for x in range(5):
            self.draai_in_het_rond(direction, Speed)  # ... sec

    def opvulling(self, direction, Speed):
        # komende opvulling
        self.achterwielen_toggle()
        delay(2000)
        self.achterwielen_toggle()
        self.voorwielen_toggle()
        delay(2000)
        self.voorwielen_toggle()
        self.achterwielen_toggle()
        delay(2000)
        self.achterwielen_toggle()
        delay(2000)

        # de rand aanraken
        self.raak_de_rand(direction, Speed)

    def dans_script(self):
        # tijdstippen
        # 1 sec - 13 sec refrein
        self.refrein("rr", 60)
        # 34 seconde opvullen
        self.opvulling("f", 40)
        # 47 sec -73 sec refrein
        self.refrein("rr", 60)
        # 34 seconde opvullen
        self.opvulling("f", 40)
        # 107 sec - 120 sec refrein
        self.refrein("rr", 60)
