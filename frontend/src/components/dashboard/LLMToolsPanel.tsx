import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const LLMToolsPanel = () => {
  const [chatInput, setChatInput] = useState("");
  const [chatResult, setChatResult] = useState(null);
  const [explainResult, setExplainResult] = useState(null);
  const [heatmapResult, setHeatmapResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChat = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: chatInput })
      });
      const data = await res.json();
      setChatResult(data);
    } catch (e) {
      setError("Chat failed");
    } finally {
      setLoading(false);
    }
  };
  const handleExplain = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/explain_risk/`);
      const data = await res.json();
      setExplainResult(data);
    } catch (e) {
      setError("Explainability failed");
    } finally {
      setLoading(false);
    }
  };
  const handleHeatmap = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/risk_heatmap/`);
      const data = await res.json();
      setHeatmapResult(data);
    } catch (e) {
      setError("Heatmap failed");
    } finally {
      setLoading(false);
    }
  };
  return (
    <Card className="card-maritime">
      <CardHeader>
        <CardTitle>LLM Tools</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Textarea value={chatInput} onChange={e => setChatInput(e.target.value)} placeholder='Ask the AI...' rows={2} />
          <Button onClick={handleChat} disabled={loading} className="mt-2">Chat</Button>
          {chatResult && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(chatResult, null, 2)}</pre>}
        </div>
        <div className="mb-4">
          <Button onClick={handleExplain} disabled={loading} className="mr-2">Explain Risk</Button>
          {explainResult && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(explainResult, null, 2)}</pre>}
        </div>
        <div>
          <Button onClick={handleHeatmap} disabled={loading}>Risk Heatmap</Button>
          {heatmapResult && <pre className="mt-2 bg-muted p-2 rounded text-xs">{JSON.stringify(heatmapResult, null, 2)}</pre>}
        </div>
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </CardContent>
    </Card>
  );
};
export default LLMToolsPanel; 