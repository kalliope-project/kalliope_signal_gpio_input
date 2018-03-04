# Gpio_buttons

## Synopsis

Launch synapses from a button connected to GPIO pins of your Raspberry Pi.

## Installation
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_gpio_buttons.git
```

## Options

| parameter | required | default | choices | comment                       |
|-----------|----------|---------|---------|-------------------------------|
| pins      | YES      |         |         | List of GPIO PIN number (BCM) |


## Values sent to the synapse

| Name                     | Description                                                               | Type | sample |
|--------------------------|---------------------------------------------------------------------------|------|--------|
| gpio_buttons_pin_number  | PIN number pressed                                                        | int  | 17     |
| gpio_buttons_pin_counter | Number of time the pin number has been pressed since Kalliope has started | int  | 23     |

## Synapses example

Simple example
```yml
- name: "gpio-pin"
  signals:
    - gpio_buttons:
        pins:
          - 4          
  neurons:
    - say:
        message: "Button pressed !"  
```

This synapse is bind to multiple pin and will give you the PIN number that has changed status
```yml
- name: "gpio-pin"
  signals:
    - gpio_buttons:
        pins:
          - 27
          - 17
          - 22
  neurons:
    - say:
        message: "you've have pressed the button attached to the pin {{ gpio_buttons_pin_number }} {{ gpio_buttons_pin_counter }} time"  
```

This signal can be used for example to mute and unmute Kalliope
```yml
- name: "gpio-unmute"
  signals:
    - gpio_buttons:
        pins:
          - 27
  neurons:
    - mute
        status: False
    - say:
        message: "I now listenning to you"
        
- name: "gpio-mute"
  signals:
    - gpio_buttons:
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
