
import { useState } from "react";
import { Zap, Bot, Play, Pause, Settings, Brain, TrendingUp, AlertTriangle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import Header from "@/components/Dashboard/Header";

const aiAgents = [
  {
    id: "1",
    name: "Risk Assessment Agent",
    type: "Risk Analysis",
    status: "active",
    confidence: 94,
    tasksCompleted: 1247,
    description: "Continuously analyzes supply chain data to identify potential risks and disruptions",
    capabilities: ["Weather monitoring", "Geopolitical analysis", "Market trend analysis"],
    lastAction: "Flagged typhoon risk in Asia-Pacific region",
    performance: 96
  },
  {
    id: "2",
    name: "Route Optimization Agent", 
    type: "Optimization",
    status: "active",
    confidence: 87,
    tasksCompleted: 892,
    description: "Optimizes shipping routes and logistics networks for efficiency and cost reduction",
    capabilities: ["Route planning", "Cost optimization", "Traffic analysis"],
    lastAction: "Rerouted 23 shipments around port congestion",
    performance: 91
  },
  {
    id: "3",
    name: "Supplier Monitoring Agent",
    type: "Monitoring", 
    status: "learning",
    confidence: 78,
    tasksCompleted: 634,
    description: "Monitors supplier performance, capacity, and potential issues across the network",
    capabilities: ["Supplier scoring", "Capacity monitoring", "Quality assessment"],
    lastAction: "Detected capacity reduction at 3 suppliers",
    performance: 85
  },
  {
    id: "4",
    name: "Incident Response Agent",
    type: "Response",
    status: "active",
    confidence: 92,
    tasksCompleted: 456,
    description: "Automatically responds to incidents and coordinates mitigation strategies",
    capabilities: ["Incident detection", "Response coordination", "Recovery planning"],
    lastAction: "Initiated backup supplier protocol",
    performance: 94
  },
  {
    id: "5",
    name: "Demand Forecasting Agent",
    type: "Forecasting",
    status: "training",
    confidence: 71,
    tasksCompleted: 289,
    description: "Predicts demand patterns and adjusts supply chain accordingly",
    capabilities: ["Demand prediction", "Inventory optimization", "Trend analysis"],
    lastAction: "Updated Q4 demand forecasts for electronics",
    performance: 82
  },
  {
    id: "6",
    name: "Compliance Monitoring Agent",
    type: "Compliance",
    status: "paused",
    confidence: 89,
    tasksCompleted: 567,
    description: "Ensures all operations comply with regulations and industry standards",
    capabilities: ["Regulatory compliance", "Documentation check", "Audit preparation"],
    lastAction: "Verified customs documentation for EU shipments",
    performance: 88
  }
];

const agentMetrics = {
  totalTasks: 4185,
  automatedResolutions: 3847,
  avgResponseTime: "2.3s",
  accuracyRate: "94.2%",
  costSavings: "$2.4M",
  timesSaved: "1,247 hours"
};

const Agents = () => {
  const [selectedAgent, setSelectedAgent] = useState(aiAgents[0]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active": return "bg-green-500";
      case "learning": return "bg-blue-500"; 
      case "training": return "bg-orange-500";
      case "paused": return "bg-gray-500";
      default: return "bg-gray-500";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active": return "🟢";
      case "learning": return "🔵";
      case "training": return "🟡";
      case "paused": return "⏸️";
      default: return "⚪";
    }
  };

  const toggleAgentStatus = (agentId: string) => {
    console.log(`Toggling agent ${agentId} status`);
  };

  return (
    <div className="min-h-screen bg-gradient-dark font-inter">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gradient-primary">AI Agents</h1>
            <p className="text-muted-foreground mt-2">Intelligent automation for supply chain management</p>
          </div>
          
          <div className="flex space-x-4">
            <Button variant="outline" className="flex items-center space-x-2">
              <Settings className="w-4 h-4" />
              <span>Agent Settings</span>
            </Button>
            <Button variant="cta">
              <Bot className="w-4 h-4 mr-2" />
              Deploy New Agent
            </Button>
          </div>
        </div>

        {/* Agent Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-6 gap-6 mb-8">
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Total Tasks</p>
                <p className="text-2xl font-bold text-primary">{agentMetrics.totalTasks.toLocaleString()}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Automated</p>
                <p className="text-2xl font-bold text-green-500">{agentMetrics.automatedResolutions.toLocaleString()}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Avg Response</p>
                <p className="text-2xl font-bold text-blue-500">{agentMetrics.avgResponseTime}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Accuracy</p>
                <p className="text-2xl font-bold text-purple-500">{agentMetrics.accuracyRate}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Cost Savings</p>
                <p className="text-2xl font-bold text-orange-500">{agentMetrics.costSavings}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Time Saved</p>
                <p className="text-2xl font-bold text-cyan-500">{agentMetrics.timesSaved}</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agent List */}
          <div className="lg:col-span-2">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-accent" />
                  <span>Active Agents</span>
                  <Badge variant="outline">{aiAgents.filter(a => a.status === "active").length} Active</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {aiAgents.map((agent) => (
                    <div 
                      key={agent.id} 
                      className={`p-4 rounded-lg glass-panel cursor-pointer card-hover ${
                        selectedAgent.id === agent.id ? "border-2 border-primary" : ""
                      }`}
                      onClick={() => setSelectedAgent(agent)}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="text-2xl">{getStatusIcon(agent.status)}</div>
                          <div>
                            <h4 className="font-semibold">{agent.name}</h4>
                            <p className="text-sm text-muted-foreground">{agent.type}</p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <Badge className={getStatusColor(agent.status)}>
                            {agent.status}
                          </Badge>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleAgentStatus(agent.id);
                            }}
                          >
                            {agent.status === "active" ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                          </Button>
                        </div>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-3">{agent.description}</p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 text-sm">
                          <span>Confidence: <span className="text-primary font-medium">{agent.confidence}%</span></span>
                          <span>Tasks: <span className="text-secondary font-medium">{agent.tasksCompleted}</span></span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <TrendingUp className="w-4 h-4 text-green-500" />
                          <span className="text-sm text-green-500">{agent.performance}%</span>
                        </div>
                      </div>
                      
                      <div className="mt-3">
                        <div className="flex justify-between text-xs text-muted-foreground mb-1">
                          <span>Performance</span>
                          <span>{agent.performance}%</span>
                        </div>
                        <Progress value={agent.performance} className="h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Agent Details */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="w-5 h-5" />
                  <span>Agent Details</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">{selectedAgent.name}</h4>
                  <p className="text-sm text-muted-foreground">{selectedAgent.description}</p>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Status</h5>
                  <Badge className={getStatusColor(selectedAgent.status)}>
                    {selectedAgent.status}
                  </Badge>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Confidence Score</h5>
                  <div className="flex items-center space-x-2">
                    <Progress value={selectedAgent.confidence} className="flex-1" />
                    <span className="text-sm font-medium">{selectedAgent.confidence}%</span>
                  </div>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Performance</h5>
                  <div className="flex items-center space-x-2">
                    <Progress value={selectedAgent.performance} className="flex-1" />
                    <span className="text-sm font-medium">{selectedAgent.performance}%</span>
                  </div>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Capabilities</h5>
                  <div className="space-y-1">
                    {selectedAgent.capabilities.map((capability, index) => (
                      <Badge key={index} variant="outline" className="text-xs mr-1 mb-1">
                        {capability}
                      </Badge>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Last Action</h5>
                  <p className="text-sm text-muted-foreground">{selectedAgent.lastAction}</p>
                </div>
                
                <div>
                  <h5 className="font-medium mb-2">Tasks Completed</h5>
                  <p className="text-2xl font-bold text-primary">{selectedAgent.tasksCompleted.toLocaleString()}</p>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Agent Controls</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Play className="w-4 h-4 mr-2" />
                  Start Agent
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Pause className="w-4 h-4 mr-2" />
                  Pause Agent
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Settings className="w-4 h-4 mr-2" />
                  Configure
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <AlertTriangle className="w-4 h-4 mr-2" />
                  View Logs
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Agents;
