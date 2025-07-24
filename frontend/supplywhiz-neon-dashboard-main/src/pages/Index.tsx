
import { useState, useEffect } from "react";
import { Zap, BarChart3, Map, Activity, AlertTriangle, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Dashboard/Header";
import AlertsFeed from "@/components/Dashboard/AlertsFeed";
import AgentReasoningPanel from "@/components/Dashboard/AgentReasoningPanel";
import AnalyticsSection from "@/components/Dashboard/AnalyticsSection";
import ActionPlanPanel from "@/components/Dashboard/ActionPlanPanel";
import { toast } from "sonner";

const Index = () => {
  const [showActionPlan, setShowActionPlan] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationSteps, setSimulationSteps] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState(0);
  
  const simulationSequence = [
    "🚨 Port Strike Detected - Rotterdam Harbor",
    "🤖 AI Agents Activated - Analyzing Impact",
    "📊 Risk Assessment - 156 Shipments at Risk",
    "🗺️ Alternative Routes Calculated",
    "📋 Action Plan Generated",
    "✅ Mitigation Strategy Ready"
  ];

  const handleAlertClick = (alert: any) => {
    setSelectedAlert(alert);
    setShowActionPlan(true);
  };

  const handleSimulateDisruption = async () => {
    setIsSimulating(true);
    setSimulationSteps([]);
    setCurrentStep(0);
    
    toast("🚨 Simulating Port Strike at Rotterdam...", {
      description: "AI agents are analyzing the situation"
    });

    // Simulate the sequence
    for (let i = 0; i < simulationSequence.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSimulationSteps(prev => [...prev, simulationSequence[i]]);
      setCurrentStep(i + 1);
      
      if (i === simulationSequence.length - 1) {
        // Show action plan after simulation
        const mockAlert = {
          id: Date.now().toString(),
          type: "Geopolitical" as const,
          title: "Port Strike - Rotterdam",
          location: "Rotterdam Port, Netherlands",
          severity: "high" as const,
          time: "Just now",
          description: "Major port workers union announces 48-hour strike affecting container operations",
          impact: "156 shipments at risk, €2.3M potential losses"
        };
        setSelectedAlert(mockAlert);
        setShowActionPlan(true);
        
        toast.success("✅ Action Plan Ready!", {
          description: "AI has generated mitigation strategies"
        });
      }
    }
    
    setIsSimulating(false);
  };

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8 space-y-8">
        {/* Hero Section with Enhanced CTA */}
        <section className="text-center space-y-6">
          <div className="space-y-3">
            <h1 className="text-4xl md:text-6xl font-bold text-gradient-primary">
              SupplyWhiz Dashboard
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              "Let's show you how it works. Here's our dashboard. We simulate a port strike—instantly, our agents get to work. You see which shipments are at risk and get an AI-generated action plan."
            </p>
          </div>
          
          <div className="space-y-4">
            <Button 
              variant="cta" 
              size="xl"
              onClick={handleSimulateDisruption}
              disabled={isSimulating}
              className="animate-bounce-in"
            >
              <Zap className="w-6 h-6 mr-3" />
              {isSimulating ? "Simulating..." : "Simulate Port Strike"}
            </Button>
            
            {/* Simulation Progress */}
            {simulationSteps.length > 0 && (
              <Card className="glass-card max-w-2xl mx-auto">
                <CardContent className="p-6">
                  <div className="space-y-3">
                    <h3 className="font-semibold text-lg flex items-center space-x-2">
                      <Activity className="w-5 h-5 text-accent animate-pulse" />
                      <span>Live Simulation Progress</span>
                    </h3>
                    <div className="space-y-2">
                      {simulationSteps.map((step, index) => (
                        <div key={index} className="flex items-center space-x-3 p-2 rounded-lg bg-muted/20">
                          <CheckCircle2 className="w-4 h-4 text-primary" />
                          <span className="text-sm">{step}</span>
                          {index === currentStep - 1 && isSimulating && (
                            <div className="w-4 h-4 border-2 border-accent border-t-transparent rounded-full animate-spin ml-auto" />
                          )}
                        </div>
                      ))}
                    </div>
                    <div className="w-full bg-muted rounded-full h-2 mt-4">
                      <div 
                        className="h-2 bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-500"
                        style={{ width: `${(currentStep / simulationSequence.length) * 100}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </section>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Alerts & Reasoning */}
          <div className="lg:col-span-1 space-y-6">
            <AlertsFeed onAlertClick={handleAlertClick} />
            <AgentReasoningPanel />
          </div>

          {/* Right Column - Analytics */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center space-x-4 mb-6">
              <BarChart3 className="w-6 h-6 text-accent" />
              <h2 className="text-2xl font-bold">Real-time Analytics & Visualizations</h2>
            </div>
            <AnalyticsSection />
          </div>
        </div>

        {/* Quick Action Cards */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Button 
            variant="glass" 
            className="h-20 flex-col space-y-2 text-left justify-start p-4"
            onClick={() => window.location.href = '/map'}
          >
            <Map className="w-6 h-6 text-accent" />
            <div>
              <div className="font-medium">3D Supply Map</div>
              <div className="text-xs text-muted-foreground">Interactive globe visualization</div>
            </div>
          </Button>
          
          <Button 
            variant="glass" 
            className="h-20 flex-col space-y-2 text-left justify-start p-4"
            onClick={() => window.location.href = '/monitoring'}
          >
            <Activity className="w-6 h-6 text-secondary" />
            <div>
              <div className="font-medium">Live Monitoring</div>
              <div className="text-xs text-muted-foreground">Real-time updates</div>
            </div>
          </Button>
          
          <Button 
            variant="glass" 
            className="h-20 flex-col space-y-2 text-left justify-start p-4"
            onClick={() => window.location.href = '/analytics'}
          >
            <BarChart3 className="w-6 h-6 text-accent" />
            <div>
              <div className="font-medium">Risk Analysis</div>
              <div className="text-xs text-muted-foreground">Predictive insights</div>
            </div>
          </Button>
          
          <Button 
            variant="glass" 
            className="h-20 flex-col space-y-2 text-left justify-start p-4"
            onClick={() => window.location.href = '/agents'}
          >
            <Zap className="w-6 h-6 text-primary" />
            <div>
              <div className="font-medium">AI Agents</div>
              <div className="text-xs text-muted-foreground">Intelligent automation</div>
            </div>
          </Button>
        </section>
      </main>

      {/* Enhanced Action Plan Modal */}
      <ActionPlanPanel 
        isOpen={showActionPlan}
        onClose={() => setShowActionPlan(false)}
        alertTitle={selectedAlert?.title}
      />
    </div>
  );
};

export default Index;
