#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Channel Data Collector - Helper class for collecting and processing ns-3 channel data.
"""

import numpy as np
import ns.core as core

class ChannelDataCollector:
    """
    Class to collect and process channel data from ns-3 simulations.
    
    This class connects to PHY-level traces in ns-3 to gather information about
    the wireless channel, such as SNR, RSSI, noise, and distance between nodes.
    The collected data can be used for machine learning purposes.
    """
    
    def __init__(self):
        """Initialize collector with empty data storage."""
        self.data = []
        self.connected_devices = set()
    
    def __monitorSniffRx(self, context, packet, channelFreqMhz, txVector, signalNoise):
        """Callback function for ns-3 MonitorSniffRx trace."""
        # Extract context information
        context_parts = context.split('/')
        node_id = int(context_parts[-3])
        
        # Extract signal information
        snr = 10 * np.log10(signalNoise.signal / signalNoise.noise)
        rssi = 10 * np.log10(signalNoise.signal)
        noise = 10 * np.log10(signalNoise.noise)
        
        # Get mobility information
        mobility = self.__get_node_mobility(node_id)
        
        # Calculate distance (simplified - assuming node 0 is transmitter)
        tx_mobility = self.__get_node_mobility(0)
        distance = self.__calculate_distance(mobility, tx_mobility)
        
        # Get tx power from txVector
        tx_power = txVector.GetTxPowerLevel()
        
        # Store data point
        self.data.append([
            core.Simulator.Now().GetSeconds(),
            node_id,
            snr,
            rssi,
            noise,
            distance,
            tx_power
        ])
    
    def __get_node_mobility(self, node_id):
        """Get mobility model for a node by ID (simplified)."""
        # In a full implementation, we would find the node object
        # Here, we'll return dummy positions for demonstration
        if node_id == 0:  # AP
            return mobility.Vector(0, 0, 0)
        elif node_id == 1:  # STA1
            return mobility.Vector(5, 5, 0)
        else:  # STA2
            return mobility.Vector(-5, -5, 0)
    
    def __calculate_distance(self, pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        dz = pos1.z - pos2.z
        return np.sqrt(dx*dx + dy*dy + dz*dz)
    
    def ConnectToPhyTraces(self, ap_devices, sta_devices):
        """Connect to PHY-level traces for all devices."""
        # Connect to AP device
        ap_device = ap_devices.Get(0)
        device_path = "/NodeList/" + str(ap_device.GetNode().GetId()) + "/DeviceList/" + str(ap_device.GetIfIndex())
        
        # Connect to MonitorSniffRx trace
        core.Config.Connect(device_path + "/Phy/MonitorSniffRx", 
                          core.MakeCallback(self.__monitorSniffRx, self))
        
        self.connected_devices.add(ap_device)
        
        # Connect to STA devices
        for i in range(sta_devices.GetN()):
            sta_device = sta_devices.Get(i)
            device_path = "/NodeList/" + str(sta_device.GetNode().GetId()) + "/DeviceList/" + str(sta_device.GetIfIndex())
            
            # Connect to MonitorSniffRx trace
            core.Config.Connect(device_path + "/Phy/MonitorSniffRx", 
                              core.MakeCallback(self.__monitorSniffRx, self))
            
            self.connected_devices.add(sta_device)
        
        print(f"Connected to traces for {len(self.connected_devices)} devices")
    
    def GetData(self):
        """Return collected data."""
        return self.data
    
    def ClearData(self):
        """Clear collected data."""
        self.data = []

# Export class
__all__ = ['ChannelDataCollector']
