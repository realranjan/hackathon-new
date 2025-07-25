import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AIActionPlan = () => {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/genai_plan/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: input
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError("AI plan generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handlePopulateFromLatest = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/alerts/`);
      const data = await res.json();
      // Flatten all risk reports from all alerts
      const allRiskReports = (data.alerts || []).flatMap(a => a.risk_report || []);
      setInput(JSON.stringify(allRiskReports, null, 2));
    } catch (e) {
      setError("Failed to fetch latest risk reports");
    } finally {
      setLoading(false);
    }
  };
  return (
    <Card className="card-maritime">
      <CardHeader>
        <CardTitle>AI Action Plan Generator</CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea value={input} onChange={e => setInput(e.target.value)} placeholder='[{"product_id":"P1001","risk_score":85,...}]' rows={4} />
        <Button onClick={handleGenerate} disabled={loading} className="mt-2">Generate Plan</Button>
        <Button onClick={handlePopulateFromLatest} disabled={loading} className="mt-2 ml-2">Populate from Latest</Button>
        {result && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(result, null, 2)}</pre>}
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </CardContent>
    </Card>
  );
};
export default AIActionPlan; 