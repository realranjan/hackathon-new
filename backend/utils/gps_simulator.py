import json
import os
import time
import logging
import sys
from pathlib import Path

# Add the parent directory to sys.path to ensure imports work correctly
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import update_shipment_location_by_gps

# Get the absolute path to the inventory file
BASE_DIR = Path(__file__).parent.parent.parent
INVENTORY_PATH = os.path.join(BASE_DIR, "data", "inventory.json")
SIM_DELAY = 2  # seconds between updates

# Demo: use hardcoded coordinates for known cities
CITY_COORDS = {
    "Bangalore": (12.97, 77.59),
    "Hubli": (15.36, 75.12),
    "Pune": (18.52, 73.86),
    "Mumbai": (19.07, 72.88),
    "Chennai": (13.08, 80.27),
    "Hyderabad": (17.38, 78.48),
    "Nagpur": (21.15, 79.09),
    "Delhi": (28.61, 77.21),
    "Raipur": (21.25, 81.63),
    "Kolkata": (22.57, 88.36),
    "Shanghai": (31.23, 121.47),
    "Hong Kong": (22.32, 114.17),
    "Singapore": (1.35, 103.82),
    "Beijing": (39.90, 116.40),
    "Kunming": (25.04, 102.72)
}

def simulate_shipment_gps(product_id: str, device_id: str | None = None, inventory_path: str = None):
    """Simulate GPS updates for a single shipment along its real route."""
    try:
        # Use provided inventory path or default
        path_to_use = inventory_path or INVENTORY_PATH
        
        # Check if file exists
        if not os.path.exists(path_to_use):
            logging.error(f"Inventory file not found at {path_to_use}")
            return
            
        with open(path_to_use) as f:
            inventory = json.load(f)
            
        shipment = next((item for item in inventory if item["product_id"] == product_id), None)
        if not shipment or "route" not in shipment:
            logging.warning(f"Shipment {product_id} not found or has no route.")
            return
            
        route = shipment["route"]
        logging.info(f"Simulating GPS updates for {product_id} along route: {' → '.join(route)}")
        
        for city in route:
            coords = CITY_COORDS.get(city)
            if not coords:
                logging.warning(f"No coordinates for {city}, skipping.")
                continue
                
            lat, lon = coords
            # Update backend (reverse geocode and update current_location)
            try:
                update_shipment_location_by_gps(product_id, lat, lon, path_to_use)
                logging.info(f"  - Moved {product_id} to {city} ({lat}, {lon})")
            except Exception as e:
                logging.error(f"Failed to update location for {product_id} at {city}: {e}")
                
            time.sleep(SIM_DELAY)
            
        logging.info(f"  - Finished simulating GPS updates for {product_id}.")
    except Exception as e:
        logging.error(f"Error simulating GPS for {product_id}: {e}")

def simulate_all_shipments(inventory_path: str = None):
    """Simulate GPS updates for all shipments in inventory.json."""
    try:
        # Use provided inventory path or default
        path_to_use = inventory_path or INVENTORY_PATH
        
        # Check if file exists
        if not os.path.exists(path_to_use):
            logging.error(f"Inventory file not found at {path_to_use}")
            return
        
        with open(path_to_use) as f:
            inventory = json.load(f)
        for item in inventory:
            product_id = item["product_id"]
            print(f"\n--- Simulating {product_id} ---")
            simulate_shipment_gps(product_id)
    except Exception as e:
        logging.error(f"Error simulating all shipments: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simulate GPS updates for a shipment or all shipments.")
    parser.add_argument("--product_id", help="Product ID of the shipment to simulate")
    parser.add_argument("--device_id", help="Traccar device ID (optional)")
    parser.add_argument("--all", action="store_true", help="Simulate all shipments in inventory.json")
    parser.add_argument("--inventory_path", help="Path to inventory.json file (optional)")
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    inventory_path = args.inventory_path or INVENTORY_PATH
    
    if args.all:
        simulate_all_shipments(inventory_path)
    elif args.product_id:
        simulate_shipment_gps(args.product_id, args.device_id, inventory_path)
    else:
        print("Specify --product_id or --all.")
        parser.print_help()