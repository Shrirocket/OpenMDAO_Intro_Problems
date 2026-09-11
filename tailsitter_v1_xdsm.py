from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=True)

x.add_system("opt", OPT, r"\text{Optimizer}")
x.add_system("Aerodynamics", FUNC, "Aerodynamics")
x.add_system("solverBAT", SOLVER, r"\text{Newton\ Battery\ Mass}")
x.add_system("Propulsion", FUNC, "Propulsion")
x.add_system("Hover", FUNC, "Hover")
x.add_system("Cruise", FUNC, "Cruise")
x.add_system("Ascend Descend", FUNC, "Ascend\ and\ Descend")
x.add_system("Transition Dynamics", FUNC, "Transition\ Dynamics")
x.add_system("Battery and Mass", FUNC, "Battery\ and\ Mass")
x.add_system("Time", FUNC, "Time")


x.connect("opt", "Aerodynamics", "b, C_r, \lambda, \Lambda")
x.connect("opt","Propulsion", "v_{cruise},  C_l, C_d")

x.connect("Aerodynamics", "Propulsion", "S")
x.connect("Aerodynamics", "Battery and Mass", "m_{wing}")

x.connect("Propulsion", "Hover", "T_{hover}, P_{hover}")
x.connect("Hover", "Battery and Mass", "E_{hover}")

x.connect("Propulsion", "Cruise", "T_{cruise}, P_{cruise}")
x.connect("Cruise", "Time", "t_{cruise}")
x.connect("Cruise", "Battery and Mass", "E_{cruise}")

x.connect("opt","Ascend Descend", "v_{climb}, v_{descend}, C_l, C_d")
x.connect("Aerodynamics", "Ascend Descend", "S")
x.connect("Ascend Descend", "Time", "t_{takeoff}, t_{climb}, t_{descend}, t_{land}")
x.connect("Ascend Descend", "Battery and Mass", "E_{takeoff}, E_{climb}, E_{descend}, E_{land}")

x.connect("Transition Dynamics", "Time", "t_{transition}")
x.connect("Transition Dynamics", "Battery and Mass", "E_{transition}")

x.connect("Battery and Mass", "solverBAT", "m_{battery}, E_{total}")
x.connect("solverBAT", "Propulsion", "MTOW")
x.connect("solverBAT", "Ascend Descend", "MTOW")
x.connect("solverBAT", "Battery and Mass", "MTOW")

x.connect("Time", "opt", "t_{total}")

x.add_output("opt", "b^*, C_r^*, \lambda^*, \Lambda^*, C_l^*, C_d^*", side=LEFT)
x.add_output("Cruise", "v_{cruise}^*", side=LEFT)
x.add_output("Ascend Descend", "v_{climb}^*, v_{descend}^*", side=LEFT)


x.add_output("Time", "t_{total}^*", side=LEFT)

# x.add_output("D2", "y_2^*", side=LEFT)
# x.add_output("F", "f^*", side=LEFT)
# x.add_output("G", "g^*", side=LEFT)

x.write("tailsitter_v1_xdsm")

