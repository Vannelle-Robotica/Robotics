import time

direction = "rr"


class Dans:

    def __init__(self, arduino, motors):
        self.arduino = arduino
        self.motors = motors

    def draai_in_het_rond(self, direction, speed):
        self.motors.move(direction, speed)
        time.sleep(3)
        self.motors.move('s')

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

    def raak_de_rand(self, direction, speed):
        self.motors.move(direction, speed)
        time.sleep(2)
        self.motors.move('b', speed)
        time.sleep(2)
        self.motors.move('s')

    def refrein(self, direction, speed):
        # het refrein duurt 12-13 seconde lang
        self.draai_in_het_rond(direction, speed)  # ... sec
        for x in range(3):
            self.stamp_met_je_voeten_op_de_grond()  # ... sec
            time.sleep(1)
        for x in range(2):
            self.zwaai_je_armen_in_de_lucht()  # ... sec
            time.sleep(1)
        time.sleep(1)
        self.ga_zitten_met_een_zucht()  # ... sec
        time.sleep(1)
        self.draai_in_het_rond(direction, speed)  # ... sec

    def opvulling(self, direction, speed):
        # komende opvulling
        for x in range(2):
            self.achterwielen_toggle()
            time.sleep(2)
            self.achterwielen_toggle()
            self.voorwielen_toggle()
            time.sleep(2)
            self.voorwielen_toggle()
            self.achterwielen_toggle()
            time.sleep(2)
            self.achterwielen_toggle()
            time.sleep(2)
            for x in range(2):
                self.zwaai_je_armen_in_de_lucht()
                time.sleep(2)
            time.sleep(1)
            self.draai_in_het_rond(direction, speed)
            time.sleep(1)
        # de rand aanraken
        self.raak_de_rand(direction, speed)

    def dans_script(self):
        # tijdstippen
        # 1 sec - 13 sec refrein
        self.refrein("rr", 100)
        # 34 seconde opvullen
        self.opvulling("f", 40)
        # 47 sec -73 sec refrein
        self.refrein("rr", 60)
        # 34 seconde opvullen
        self.opvulling("f", 40)
        # 107 sec - 120 sec refrein
        self.refrein("rr", 60)
