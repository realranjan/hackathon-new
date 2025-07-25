import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const DisruptionSimulator = () => {
  const [input, setInput] = useState("");
  const [batchInput, setBatchInput] = useState("");
  const [result, setResult] = useState(null);
  const [batchResult, setBatchResult] = useState(null);
  const [allResult, setAllResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSimulate = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/simulate_disruptions/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify([{...JSON.parse(input)}])
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || data.error || "Simulation failed");
      } else {
        setResult(data);
      }
    } catch (e) {
      setError("Simulation failed");
    } finally {
      setLoading(false);
    }
  };
  const handleBatchSimulate = async () => {
    setLoading(true); setError(null);
    try {
      let payload;
      try {
        const parsed = JSON.parse(batchInput);
        payload = Array.isArray(parsed) ? parsed : [parsed];
      } catch (e) {
        setError("Batch input must be valid JSON (array or object)");
        setLoading(false);
        return;
      }
      const res = await fetch(`${API_BASE}/batch_simulate_disruptions/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || data.error || "Batch simulation failed");
      } else {
        setBatchResult(data);
      }
    } catch (e) {
      setError("Batch simulation failed");
    } finally {
      setLoading(false);
    }
  };
  const handleProcessAll = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/process_all_disruptions/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: batchInput || "[]"
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || data.error || "Process all disruptions failed");
      } else {
        setAllResult(data);
      }
    } catch (e) {
      setError("Process all disruptions failed");
    } finally {
      setLoading(false);
    }
  };
  return (
    <Card className="card-maritime">
      <CardHeader>
        <CardTitle>Disruption Simulator</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Textarea value={input} onChange={e => setInput(e.target.value)} placeholder='{"location":"Bangalore Port","event_type":"Strike","severity":"High","timestamp":"2024-06-01T12:00:00Z","source":"Simulated","mode":"road"}' rows={4} />
          <Button onClick={handleSimulate} disabled={loading} className="mt-2">Simulate Disruption</Button>
          {result && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(result, null, 2)}</pre>}
        </div>
        <div>
          <Textarea value={batchInput} onChange={e => setBatchInput(e.target.value)} placeholder='[{...}, {...}]' rows={4} />
          <Button onClick={handleBatchSimulate} disabled={loading} className="mt-2">Batch Simulate</Button>
          <Button onClick={handleProcessAll} disabled={loading} className="mt-2 ml-2">Process All (Simulated + Real)</Button>
          {batchResult && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(batchResult, null, 2)}</pre>}
          {allResult && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(allResult, null, 2)}</pre>}
        </div>
        {error && (
          <div className="text-red-500 mt-2">
            {typeof error === 'string' ? error : <pre className="bg-muted p-2 rounded text-xs">{JSON.stringify(error, null, 2)}</pre>}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
export default DisruptionSimulator; 