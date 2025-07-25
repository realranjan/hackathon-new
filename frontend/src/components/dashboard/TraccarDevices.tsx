import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const TraccarDevices = () => {
  const [devices, setDevices] = useState([]);
  const [shipments, setShipments] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState("");
  const [selectedShipment, setSelectedShipment] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/list_traccar_devices/`).then(res => res.json()).then(data => setDevices(data.devices || []));
    fetch(`${API_BASE}/shipments/`).then(res => res.json()).then(data => setShipments(data.shipments || []));
  }, []);

  const handleAssociate = async () => {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/associate_traccar_device/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: selectedShipment, device_id: selectedDevice })
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError("Association failed");
    }
  };

  return (
    <Card className="card-maritime">
      <CardHeader>
        <CardTitle>Traccar Device Management</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex gap-2 mb-2">
          <Select value={selectedShipment} onValueChange={setSelectedShipment}>
            <SelectTrigger className="w-48"><SelectValue placeholder="Select Shipment" /></SelectTrigger>
            <SelectContent>
              {shipments.map(s => <SelectItem key={s.product_id} value={s.product_id}>{s.product_id}</SelectItem>)}
            </SelectContent>
          </Select>
          <Select value={selectedDevice} onValueChange={setSelectedDevice}>
            <SelectTrigger className="w-48"><SelectValue placeholder="Select Device" /></SelectTrigger>
            <SelectContent>
              {devices.map(d => <SelectItem key={d.id} value={d.id}>{d.name || d.id}</SelectItem>)}
            </SelectContent>
          </Select>
          <Button onClick={handleAssociate} disabled={!selectedDevice || !selectedShipment}>Associate</Button>
        </div>
        {result && <pre className="bg-muted p-2 rounded text-xs mt-2">{JSON.stringify(result, null, 2)}</pre>}
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </CardContent>
    </Card>
  );
};
export default TraccarDevices; 