#!/bin/bash

for var in {1..1000}
do
  python3 pacman.py -p ExpectimaxAgent -m stuckmap -a depth=5 -n $var -q
done