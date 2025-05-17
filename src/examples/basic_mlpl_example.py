#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic MLPL Example - Integrating ML with ns-3 for Channel Prediction

This example demonstrates how to:
1. Create a simple ns-3 wireless network
2. Collect channel state information during simulation
3. Train a simple ML model on this data
4. Use predictions to optimize transmission parameters
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# Add the project root to the Python path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import ns-3 modules
import ns.core as core
import ns.network as network
import ns.mobility as mobility
import ns.wifi as wifi
import ns.internet as internet
import ns.applications as applications

# Import project modules
from src.helper.channel_data_collector import ChannelDataCollector
from src.helper.ml_helper import MLHelper

def configure_nodes():
    """Configure ns-3 nodes with mobility and wireless devices."""
    print("Configuring simulation nodes...")
    
    # Create nodes
    nodes = network.NodeContainer()
    nodes.Create(3)  # 1 AP and 2 STAs
    
    # Configure mobility
    mobility_helper = mobility.MobilityHelper()
    
    # Position AP at center
    pos = mobility.ListPositionAllocator()
    pos.Add(mobility.Vector(0.0, 0.0, 0.0))  # AP position
    pos.Add(mobility.Vector(5.0, 5.0, 0.0))  # STA1 position
    pos.Add(mobility.Vector(-5.0, -5.0, 0.0))  # STA2 position
    
    mobility_helper.SetPositionAllocator(pos)
    mobility_helper.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobility_helper.Install(nodes)
    
    # Create and configure WiFi
    channel = wifi.YansWifiChannelHelper.Default()
    phy = wifi.YansWifiPhyHelper()
    phy.SetChannel(channel.Create())
    
    wifi_helper = wifi.WifiHelper()
    wifi_helper.SetStandard(wifi.WIFI_STANDARD_80211n_5GHZ)
    
    mac = wifi.WifiMacHelper()
    
    # Configure AP
    ssid = wifi.Ssid("MLPL-Example")
    mac.SetType("ns3::ApWifiMac", "Ssid", core.StringValue(ssid))
    ap_devices = wifi_helper.Install(phy, mac, nodes.Get(0))
    
    # Configure STAs
    mac.SetType("ns3::StaWifiMac", "Ssid", core.StringValue(ssid))
    sta_devices = wifi_helper.Install(phy, mac, network.NodeContainer(nodes.Get(1), nodes.Get(2)))
    
    # Configure Internet stack
    internet_stack = internet.InternetStackHelper()
    internet_stack.Install(nodes)
    
    # Assign IP addresses
    ipv4_helper = internet.Ipv4AddressHelper()
    ipv4_helper.SetBase(network.Ipv4Address("192.168.1.0"), network.Ipv4Mask("255.255.255.0"))
    interfaces = ipv4_helper.Assign(network.NetDeviceContainer(ap_devices, sta_devices))
    
    return nodes, ap_devices, sta_devices

def setup_applications(nodes):
    """Configure applications for data transmission."""
    print("Setting up applications...")
    
    # Create OnOff application on STA1 to send data to STA2
    port = 9
    on_off_helper = applications.OnOffHelper("ns3::UdpSocketFactory", 
                                            network.InetSocketAddress(network.Ipv4Address("192.168.1.3"), port))
    on_off_helper.SetAttribute("OnTime", core.StringValue("ns3::ConstantRandomVariable[Constant=1]"))
    on_off_helper.SetAttribute("OffTime", core.StringValue("ns3::ConstantRandomVariable[Constant=0]"))
    on_off_helper.SetAttribute("DataRate", core.DataRateValue(core.DataRate("1Mb/s")))
    on_off_helper.SetAttribute("PacketSize", core.UintegerValue(1000))
    
    tx_app = on_off_helper.Install(nodes.Get(1))  # Install on STA1
    tx_app.Start(core.Seconds(1.0))
    tx_app.Stop(core.Seconds(10.0))
    
    # Create packet sink on STA2 to receive data
    sink_helper = applications.PacketSinkHelper("ns3::UdpSocketFactory",
                                              network.InetSocketAddress(network.Ipv4Address::GetAny(), port))
    rx_app = sink_helper.Install(nodes.Get(2))  # Install on STA2
    rx_app.Start(core.Seconds(0.0))
    rx_app.Stop(core.Seconds(11.0))
    
    return tx_app, rx_app

def collect_channel_data(ap_devices, sta_devices, simulation_time=10.0):
    """Run simulation and collect channel data."""
    print("Setting up data collection...")
    
    # Create channel data collector
    channel_collector = ChannelDataCollector()
    channel_collector.ConnectToPhyTraces(ap_devices, sta_devices)
    
    print(f"Running simulation for {simulation_time} seconds...")
    # Schedule simulator
    core.Simulator.Stop(core.Seconds(simulation_time))
    core.Simulator.Run()
    core.Simulator.Destroy()
    
    # Get collected data
    channel_data = channel_collector.GetData()
    print(f"Collected {len(channel_data)} channel data points")
    
    return channel_data

def train_ml_model(channel_data):
    """Train ML model on collected channel data."""
    print("Processing data and training ML model...")
    
    # Convert to pandas DataFrame for easier processing
    df = pd.DataFrame(channel_data, 
                     columns=['time', 'node_id', 'snr', 'rssi', 'noise', 'distance', 'tx_power'])
    
    # Feature engineering
    df['prev_snr'] = df.groupby('node_id')['snr'].shift(1).fillna(df['snr'])
    df['snr_diff'] = df['snr'] - df['prev_snr']
    
    # Prepare data for ML
    X = df[['prev_snr', 'rssi', 'distance', 'tx_power', 'snr_diff']].values
    y = df['snr'].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train model using helper
    ml_helper = MLHelper()
    model = ml_helper.train_linear_model(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model MSE: {mse:.4f}")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
    plt.xlabel('Actual SNR')
    plt.ylabel('Predicted SNR')
    plt.title('SNR Prediction Performance')
    plt.savefig('results/snr_prediction.png')
    plt.close()
    
    return model, scaler

def optimize_tx_parameters(model, scaler):
    """Use ML model to optimize transmission parameters."""
    print("Optimizing transmission parameters using ML model...")
    
    # Example: Finding optimal tx power for a given distance
    distances = np.linspace(1, 15, 10)  # 1m to 15m
    tx_powers = np.linspace(5, 20, 4)   # 5dBm to 20dBm
    
    best_params = {}
    for distance in distances:
        best_snr = -float('inf')
        best_tx = None
        
        for tx_power in tx_powers:
            # Create feature vector (dummy values for prev_snr, rssi, snr_diff)
            features = np.array([[10, -60, distance, tx_power, 0]])
            scaled_features = scaler.transform(features)
            
            # Predict SNR
            predicted_snr = model.predict(scaled_features)[0]
            
            if predicted_snr > best_snr:
                best_snr = predicted_snr
                best_tx = tx_power
        
        best_params[distance] = (best_tx, best_snr)
    
    # Plot optimal parameters
    distances_list = list(best_params.keys())
    tx_values = [best_params[d][0] for d in distances_list]
    snr_values = [best_params[d][1] for d in distances_list]
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(distances_list, tx_values, 'o-')
    plt.xlabel('Distance (m)')
    plt.ylabel('Optimal Tx Power (dBm)')
    plt.title('ML-Optimized Tx Power vs Distance')
    
    plt.subplot(1, 2, 2)
    plt.plot(distances_list, snr_values, 'o-')
    plt.xlabel('Distance (m)')
    plt.ylabel('Predicted SNR (dB)')
    plt.title('Predicted SNR with Optimal Tx Power')
    
    plt.tight_layout()
    plt.savefig('results/tx_optimization.png')
    plt.close()
    
    print("Parameter optimization complete. Results saved to results directory.")
    return best_params

def main():
    """Main function to run the example."""
    print("Starting ns-3 + MLPL integration example...")
    
    # Create required directories
    os.makedirs('results', exist_ok=True)
    
    # Configure ns-3 simulation
    nodes, ap_devices, sta_devices = configure_nodes()
    
    # Setup applications
    tx_app, rx_app = setup_applications(nodes)
    
    # Run simulation and collect data
    channel_data = collect_channel_data(ap_devices, sta_devices)
    
    # Train ML model on collected data
    model, scaler = train_ml_model(channel_data)
    
    # Use ML model to optimize parameters
    best_params = optimize_tx_parameters(model, scaler)
    
    print("Example completed successfully!")
    print("Check the 'results' directory for output plots.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
