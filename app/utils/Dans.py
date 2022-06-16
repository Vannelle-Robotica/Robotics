from turtle import delay

from app.hardware import motors, arduino

direction = "rr"
Speed = 60


def draai_in_het_rond(direction, Speed):
    motors.move(direction, Speed)


def stamp_met_je_voeten_op_de_grond():
    arduino.toggle_wheels()


def zwaai_je_armen_in_de_lucht():
    arduino.toggle_arm()


def ga_zitten_met_een_zucht():
    arduino.toggle_wheels()


def voorwielen_toggle():
    arduino.toggle_wheels_front()


def achterwielen_toggle():
    arduino.toggle_wheels_back()


def raak_de_rand(direction, Speed):
    motors.move(direction, Speed)
    delay(2000)
    direction = "b"
    motors.move(direction, Speed)


def refrein(direction, Speed):
    # het refrein duurt 12-13 seconde lang
    draai_in_het_rond(direction, Speed)  # ... sec
    delay(1000)
    stamp_met_je_voeten_op_de_grond()  # ... sec
    delay(1000)
    zwaai_je_armen_in_de_lucht()  # ... sec
    delay(1000)
    ga_zitten_met_een_zucht()  # ... sec
    delay(1000)
    draai_in_het_rond(direction, Speed)  # ... sec


def opvulling(direction, Speed):
    # komende opvulling
    achterwielen_toggle()
    delay(1000)
    voorwielen_toggle()
    achterwielen_toggle()
    delay(1000)
    voorwielen_toggle()
    achterwielen_toggle()

    # de rand aanraken
    raak_de_rand(direction, Speed)


def dans_script():
    # tijdstippen
    # 1 sec - 13 sec refrein
    refrein("rr", 60)
    # 34 seconde opvullen
    opvulling("f", 40)
    # 47 sec -73 sec refrein
    refrein("rr", 60)
    # 34 seconde opvullen
    opvulling("f", 40)
    # 107 sec - 120 sec refrein
    refrein("rr", 60)
