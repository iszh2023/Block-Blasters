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
    hub.port.A.motor.run_for_seconds(3.0)
    time.sleep(0.5)
    hub.led('red')
    hub.sound.beep(880.0, 1.0)
    for i in range(5):
        print('Hello Spike!')
        hub.port.A.motor.stop()

if __name__ == "__main__":
    main()