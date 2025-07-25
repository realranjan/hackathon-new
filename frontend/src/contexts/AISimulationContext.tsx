import React, { createContext, useContext, useState, useCallback } from 'react';
import { toast } from '@/hooks/use-toast';

interface AISimulationState {
  isActive: boolean;
  currentStep: number;
  totalSteps: number;
  activeAgents: string[];
  processingData: boolean;
  alertsCount: number;
  shipmentsProcessed: number;
  riskLevel: 'low' | 'medium' | 'high';
}

interface AISimulationContextType {
  simulation: AISimulationState;
  startSimulation: () => void;
  stopSimulation: () => void;
  updateSimulation: (updates: Partial<AISimulationState>) => void;
}

const AISimulationContext = createContext<AISimulationContextType | undefined>(undefined);

export const useAISimulation = () => {
  const context = useContext(AISimulationContext);
  if (!context) {
    throw new Error('useAISimulation must be used within an AISimulationProvider');
  }
  return context;
};

export const AISimulationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [simulation, setSimulation] = useState<AISimulationState>({
    isActive: false,
    currentStep: 0,
    totalSteps: 8,
    activeAgents: [],
    processingData: false,
    alertsCount: 0,
    shipmentsProcessed: 0,
    riskLevel: 'low'
  });

  const updateSimulation = useCallback((updates: Partial<AISimulationState>) => {
    setSimulation(prev => ({ ...prev, ...updates }));
  }, []);

  const simulationSteps = [
    {
      step: 1,
      title: "AI Agents Initialization",
      agents: ["Risk Analyzer", "Port Monitor"],
      duration: 2000,
      action: () => {
        toast({
          title: "🤖 AI Agents Activated",
          description: "Risk Analyzer and Port Monitor agents are now online",
        });
      }
    },
    {
      step: 2,
      title: "Data Collection Phase",
      agents: ["Risk Analyzer", "Port Monitor", "Shipment Tracker"],
      duration: 1500,
      action: () => {
        updateSimulation({ processingData: true });
        toast({
          title: "📊 Data Collection Started",
          description: "Gathering real-time port and shipment data",
        });
      }
    },
    {
      step: 3,
      title: "Risk Assessment",
      agents: ["Risk Analyzer", "Compliance Checker"],
      duration: 2000,
      action: () => {
        updateSimulation({ riskLevel: 'medium', alertsCount: 3 });
        toast({
          title: "⚠️ Risk Analysis Complete",
          description: "Medium risk detected in Southeast Asia routes",
          variant: "destructive"
        });
      }
    },
    {
      step: 4,
      title: "Port Performance Analysis",
      agents: ["Port Monitor", "Performance Analyzer"],
      duration: 1800,
      action: () => {
        toast({
          title: "🏭 Port Analysis",
          description: "Shanghai port showing 15% efficiency improvement",
        });
      }
    },
    {
      step: 5,
      title: "Shipment Optimization",
      agents: ["Route Optimizer", "Shipment Tracker"],
      duration: 2200,
      action: () => {
        updateSimulation({ shipmentsProcessed: 247 });
        toast({
          title: "🚢 Route Optimization",
          description: "247 shipments optimized, saving 12% transit time",
        });
      }
    },
    {
      step: 6,
      title: "Predictive Analytics",
      agents: ["Demand Forecaster", "Weather Analyzer"],
      duration: 1600,
      action: () => {
        toast({
          title: "🔮 Predictive Analysis",
          description: "Weather delays predicted for Pacific routes",
        });
      }
    },
    {
      step: 7,
      title: "Compliance Verification",
      agents: ["Compliance Checker", "Document Processor"],
      duration: 1400,
      action: () => {
        updateSimulation({ alertsCount: 1 });
        toast({
          title: "✅ Compliance Check",
          description: "All shipments verified, 1 minor documentation issue found",
        });
      }
    },
    {
      step: 8,
      title: "Report Generation",
      agents: ["Report Generator"],
      duration: 1000,
      action: () => {
        updateSimulation({ processingData: false, riskLevel: 'low' });
        toast({
          title: "📈 Analysis Complete",
          description: "Comprehensive supply chain report generated",
        });
      }
    }
  ];

  const startSimulation = useCallback(() => {
    if (simulation.isActive) return;

    setSimulation(prev => ({
      ...prev,
      isActive: true,
      currentStep: 0,
      activeAgents: [],
      alertsCount: 0,
      shipmentsProcessed: 0,
      riskLevel: 'low'
    }));

    toast({
      title: "🚀 AI Demo Started",
      description: "Supply Chain Intelligence System is now simulating...",
    });

    // Execute simulation steps
    simulationSteps.forEach((stepData, index) => {
      setTimeout(() => {
        updateSimulation({ 
          currentStep: stepData.step,
          activeAgents: stepData.agents 
        });
        stepData.action();

        // Complete simulation on last step
        if (index === simulationSteps.length - 1) {
          setTimeout(() => {
            setSimulation(prev => ({ ...prev, isActive: false, currentStep: 0 }));
            toast({
              title: "✨ Demo Complete",
              description: "AI simulation finished successfully!",
            });
          }, stepData.duration);
        }
      }, simulationSteps.slice(0, index).reduce((acc, step) => acc + step.duration, 0));
    });
  }, [simulation.isActive, updateSimulation]);

  const stopSimulation = useCallback(() => {
    setSimulation(prev => ({
      ...prev,
      isActive: false,
      currentStep: 0,
      activeAgents: [],
      processingData: false
    }));
    toast({
      title: "⏹️ Demo Stopped",
      description: "AI simulation has been stopped",
    });
  }, []);

  return (
    <AISimulationContext.Provider value={{ simulation, startSimulation, stopSimulation, updateSimulation }}>
      {children}
    </AISimulationContext.Provider>
  );
};