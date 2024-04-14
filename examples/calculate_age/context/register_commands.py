# Will execute the register function on the __init__ of the module
# To ensure that all commands and handlers are registered

from examples.calculate_age.context.calculate_age import CalculateAgeCommand, CalculateAgeHandler
from turbobus.constants import Provider


def register():
    Provider.set(CalculateAgeCommand, CalculateAgeHandler)
