#!/bin/bash
cd ~/ns-allinone-3.41/ns-3.41
if [ ! -f "build/config.status" ]; then
    echo "Configuring ns-3..."
    ./ns3 configure --enable-examples --enable-tests
fi
./ns3 "$@"