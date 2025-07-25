import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CheckCircle, Circle, Clock, AlertTriangle } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const WorkflowProgress = () => {
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/workflow/progress/`)
      .then(res => res.json())
      .then(data => {
        setProgress(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load workflow progress");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading workflow progress...</div>;
  if (error) return <div>{error}</div>;

  const step = progress?.step || 0;
  const totalSteps = progress?.total_steps || 1;
  const progressPercentage = (step / totalSteps) * 100;

  return (
    <Card className="card-maritime lg:col-span-6">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-lg">
            <AlertTriangle className="h-5 w-5 text-primary" />
            Workflow Progress
          </div>
          <Badge variant="secondary" className="text-xs">
            Ready
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm mb-4">
            <span className="text-muted-foreground">
              Step {step} of {totalSteps}
            </span>
            <Progress value={progressPercentage} className="w-24" />
          </div>
          {/* You can add more detailed step info here if backend provides it */}
        </div>
      </CardContent>
    </Card>
  );
};

export default WorkflowProgress;