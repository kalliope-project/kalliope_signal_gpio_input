import logging
from threading import Thread

import RPi.GPIO as GPIO
import time

from kalliope.core.SynapseLauncher import SynapseLauncher

from kalliope import Utils
from kalliope.core import SignalModule

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Pin:
    def __init__(self, pin_number=None, synapse_list=None, count=0, prev_inp=1):
        self.pin_number = pin_number
        self.synapse_list = synapse_list
        self.count = count
        self.prev_inp = prev_inp

        if self.synapse_list is None:
            self.synapse_list = list()

    def __str__(self):
        returned_dict = {
            "pin number": self.pin_number,
            "synapse_list:": self.synapse_list
        }
        return str(returned_dict)


class Gpio_input(SignalModule, Thread):

    def __init__(self, **kwargs):
        super(Gpio_input, self).__init__(**kwargs)
        Utils.print_info('[gpio_input] Starting gpio_input signal manager')
        # here is the list of synapse that deals with gpio_button signal
        self.list_synapses_with_gpio_buttons = list(super(Gpio_input, self).get_list_synapse())
        # get a list of Pin object with their attached synapse name to launch
        self.list_pin = self.get_list_pin_with_associated_synapse(self.list_synapses_with_gpio_buttons)

    def run(self):
        logger.debug("[gpio_input] Starting Gpio_buttons thread")

        # setup GPIO
        GPIO.setmode(GPIO.BCM)

        # init each GPIO pin
        for pin in self.list_pin:
            GPIO.setup(pin.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # get the default state
            pin.prev_inp = GPIO.input(pin.pin_number)
        # check forever each button
        try:
            while True:
                for pin in self.list_pin:
                    self.input_check(pin)
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

    @staticmethod
    def check_parameters(parameters):
        """
        overwrite method
        receive a dict of parameter from a gpio_input signal
        :param parameters: dict of gpio_input parameters
        :return: True if parameters are valid
        """
        # check mandatory parameters
        mandatory_parameters = ["pins"]
        if not all(key in parameters for key in mandatory_parameters):
            return False

        return True

    @staticmethod
    def get_list_pin_with_associated_synapse(list_synapse):
        """
        return a list of pin object with their respective list of synapse to execute when switched
        :return: list of Pin object
        """
        list_pins = list()

        for synapse in list_synapse:
            for signal in synapse.signals:
                if signal.name == "gpio_input":
                    for pin in signal.parameters["pins"]:
                        # check if the pin is already declared in the list
                        if not any(x.pin_number == pin for x in list_pins):
                            logger.debug("[gpio_input] Add the pin %s to the list" % pin)
                            # create a new Pin object
                            new_pin = Pin(pin_number=pin)
                            new_pin.synapse_list.append(synapse.name)
                            logger.debug("[gpio_input] Synapse %s added to pin %s" % (synapse.name, pin))
                            list_pins.append(new_pin)

                        else:
                            logger.debug("[gpio_buttons] Pin %s already in the list" % pin)
                            # only add the synapse to the pin object
                            for pin_to_find in list_pins:
                                if pin_to_find.pin_number == pin:
                                    pin_to_find.synapse_list.append(synapse.name)
                                    logger.debug("[gpio_buttons] Synapse %s added to pin %s" % (synapse.name, pin))

        return list_pins

    @staticmethod
    def input_check(pin_object):
        """
        This function check a Pin. If the status changed, start all attached synapse
        :param pin_object: pin to check
        :type pin_object: Pin
        """

        inp = GPIO.input(pin_object.pin_number)
        if inp != pin_object.prev_inp and inp:
            pin_object.count = pin_object.count + 1
            logger.debug("[gpio_input] Button pressed: %s" % pin_object.pin_number)
            logger.debug("[gpio_input] Button count: %s" % pin_object.count)
            logger.debug("[gpio_input] run synapse: %s" % pin_object.synapse_list)
            for synapse in pin_object.synapse_list:
                logger.debug("[gpio_input] start synapse name %s" % synapse)
                overriding_parameter_dict = dict()
                overriding_parameter_dict["gpio_input_pin_number"] = pin_object.pin_number
                overriding_parameter_dict["gpio_input_pin_counter"] = pin_object.count
                SynapseLauncher.start_synapse_by_name(synapse,
                                                      overriding_parameter_dict=overriding_parameter_dict)
        pin_object.prev_inp = inp
