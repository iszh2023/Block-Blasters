#!/usr/bin/env python3
"""
Generated Python code from Spike block diagram
"""

from spike import PrimeHub
import time

# Initialize the SPIKE Prime hub
hub = PrimeHub()

def main():
    """Main program entry point"""
    while True:
        hub.port.A.motor.run_for_seconds(2.0)
        hub.led('green')
        time.sleep(1.0)
    for i in range(3):
        hub.sound.beep(660.0, 0.3)
        print('Beep!')
    hub.port.B.motor.run_for_seconds(1.0)
    hub.led('red')

if __name__ == "__main__":
    main()