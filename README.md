# Kalliope Gpio input signal

## Synopsis

Launch synapses from from a Raspberry Pi digital input received on a GPIO pin.

This Kalliope signal can be used for example with the following hardware:
- button
- Magnetic switch
- PIR sensor

## Installation

```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_gpio_input.git
```

## Options

| parameter | required | default | choices | comment                       |
|-----------|----------|---------|---------|-------------------------------|
| pins      | YES      |         |         | List of GPIO PIN number (BCM) |


## Values sent to the synapse

| Name                   | Description                                                                  | Type | sample |
|------------------------|------------------------------------------------------------------------------|------|--------|
| gpio_input_pin_number  | PIN number pressed                                                           | int  | 17     |
| gpio_input_pin_counter | Number of time the pin number has switched status since Kalliope has started | int  | 23     |

## Synapses example

Simple example
```yml
- name: "gpio-test"
  signals:
    - gpio_input:
        pins:
          - 4          
  neurons:
    - say:
        message: "Button pressed !"  
```

This synapse is bind to multiple pin and will give you the PIN number that has changed status
```yml
- name: "gpio-test2"
  signals:
    - gpio_input:
        pins:
          - 27
          - 17
          - 22
  neurons:
    - say:
        message: "you've have pressed the button attached to the pin {{ gpio_input_pin_number }} {{ gpio_input_pin_counter }} time"  
```

This signal can be used for example to mute and unmute Kalliope
```yml
- name: "gpio-unmute"
  signals:
    - gpio_input:
        pins:
          - 27
  neurons:
    - mute
        status: False
    - say:
        message: "I'm now listenning to you"
        
- name: "gpio-mute"
  signals:
    - gpio_input:
        pins:
          - 27          
  neurons:
    - mute
        status: True
    - say:
        message: "I'm not listenning anymore"
```


## Notes

> **Note:** This signal only work on Raspberry Pi
