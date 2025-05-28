#!/bin/bash
cd ~/ns-allinone-3.41/ns-3.41
if [ ! -f "build/config.status" ]; then
    echo "Configuring ns-3..."
    ./ns3 configure --enable-examples --enable-tests
fi
./ns3 "$@"

# Make it executable
chmod +x ~/setup_ns3.sh

# Create a simpler alias
echo 'alias ns3="~/setup_ns3.sh"' >> ~/.bashrc
source ~/.bashrc