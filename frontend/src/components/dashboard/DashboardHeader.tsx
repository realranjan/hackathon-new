import { Activity, AlertTriangle, BarChart3, Shield, Zap, Globe, TrendingUp, Users, Package, Settings, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { useAISimulation } from "@/contexts/AISimulationContext";
import { useState } from "react";

const DashboardHeader = () => {
  const { simulation, startSimulation, stopSimulation } = useAISimulation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    setMobileMenuOpen(false); // Close mobile menu when navigating
  };

  const handleNavClick = (e: React.MouseEvent, sectionId?: string) => {
    e.preventDefault();
    if (sectionId) {
      scrollToSection(sectionId);
    }
  };

  const navItems = [
    { label: "Dashboard", icon: Activity, action: () => handleNavClick({} as React.MouseEvent) },
    { label: "Analytics", icon: TrendingUp, action: () => scrollToSection('analytics-section') },
    { label: "Port Status", icon: Globe, action: () => scrollToSection('port-status') },
    { label: "Shipments", icon: Package, action: () => scrollToSection('shipments-section') },
    { label: "Alerts", icon: AlertTriangle, action: () => scrollToSection('alerts-section') },
    { label: "AI Agents", icon: Shield, action: () => scrollToSection('ai-agents') },
    { label: "AI Network", icon: Activity, action: () => scrollToSection('ai-network') },
  ];

  return (
    <div className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Mobile Header */}
        <div className="flex items-center justify-between py-3 lg:hidden">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg gradient-primary">
              <Shield className="h-4 w-4 text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-foreground">ZeroTouch</h1>
              <div className="flex items-center gap-2">
                <div className="status-indicator status-live w-2 h-2"></div>
                <span className="text-xs font-medium text-success">Live</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="sm" className="p-2">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-80">
                <SheetHeader className="text-left">
                  <SheetTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5" />
                    Navigation
                  </SheetTitle>
                </SheetHeader>
                <div className="mt-6 space-y-2">
                  {/* AI Demo Button */}
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className={cn(
                      "w-full gap-2 justify-start transition-all duration-300",
                      simulation.isActive && "bg-primary/10 border-primary text-primary"
                    )}
                    onClick={() => {
                      simulation.isActive ? stopSimulation() : startSimulation();
                      setMobileMenuOpen(false);
                    }}
                  >
                    <BarChart3 className="h-4 w-4" />
                    {simulation.isActive ? `AI Demo (${simulation.currentStep}/${simulation.totalSteps})` : "AI Demo"}
                  </Button>
                  
                  {/* Navigation Items */}
                  {navItems.map((item) => (
                    <Button
                      key={item.label}
                      variant="ghost"
                      size="sm"
                      className="w-full justify-start gap-2"
                      onClick={item.action}
                    >
                      <item.icon className="h-4 w-4" />
                      {item.label}
                    </Button>
                  ))}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>

        {/* Desktop Header */}
        <div className="hidden lg:block">
          {/* Top Brand Row */}
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg gradient-primary">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">
                  ZeroTouch Supply Chain Intelligence
                </h1>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-muted-foreground">Live Demo</span>
                  <div className="flex items-center gap-2">
                    <div className="status-indicator status-live"></div>
                    <span className="text-xs font-medium text-success">Real-time</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border bg-card">
                <span className="text-sm font-medium text-foreground">Dark Mode:</span>
                <ThemeToggle />
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                className={cn(
                  "gap-2 transition-all duration-300",
                  simulation.isActive && "bg-primary/10 border-primary text-primary animate-pulse"
                )}
                onClick={simulation.isActive ? stopSimulation : startSimulation}
                disabled={simulation.isActive}
              >
                <BarChart3 className={cn(
                  "h-4 w-4 transition-transform duration-300",
                  simulation.isActive && "rotate-180"
                )} />
                {simulation.isActive ? `AI Demo (${simulation.currentStep}/${simulation.totalSteps})` : "AI Demo"}
              </Button>
              <Button variant="default" size="sm" className="gap-2 gradient-primary border-0">
                <Zap className="h-4 w-4" />
                Start
              </Button>
            </div>
          </div>

          {/* Desktop Navigation Menu */}
          <div className="pb-4">
            <NavigationMenu>
              <NavigationMenuList>
                <NavigationMenuItem>
                  <button
                    className={cn(
                      navigationMenuTriggerStyle(),
                      "bg-accent text-accent-foreground font-medium cursor-pointer"
                    )}
                    onClick={(e) => handleNavClick(e)}
                  >
                    <Activity className="mr-2 h-4 w-4" />
                    Dashboard
                  </button>
                </NavigationMenuItem>
                
                <NavigationMenuItem>
                  <NavigationMenuTrigger>
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Analytics
                  </NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <div className="grid gap-3 p-6 w-[400px]">
                      <div className="grid grid-cols-2 gap-4">
                        <button 
                          className="flex items-center gap-2 p-3 rounded-md hover:bg-accent cursor-pointer w-full text-left"
                          onClick={(e) => handleNavClick(e, 'analytics-section')}
                        >
                          <BarChart3 className="h-4 w-4" />
                          <div>
                            <div className="text-sm font-medium">Risk Analytics</div>
                            <div className="text-xs text-muted-foreground">Risk heatmaps & trends</div>
                          </div>
                        </button>
                        <button 
                          className="flex items-center gap-2 p-3 rounded-md hover:bg-accent cursor-pointer w-full text-left"
                          onClick={(e) => handleNavClick(e, 'port-status')}
                        >
                          <Globe className="h-4 w-4" />
                          <div>
                            <div className="text-sm font-medium">Port Performance</div>
                            <div className="text-xs text-muted-foreground">Global port metrics</div>
                          </div>
                        </button>
                      </div>
                    </div>
                  </NavigationMenuContent>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <button 
                    className={cn(navigationMenuTriggerStyle(), "cursor-pointer")}
                    onClick={(e) => handleNavClick(e, 'shipments-section')}
                  >
                    <Package className="mr-2 h-4 w-4" />
                    Shipments
                  </button>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <button 
                    className={cn(navigationMenuTriggerStyle(), "cursor-pointer")}
                    onClick={(e) => handleNavClick(e, 'alerts-section')}
                  >
                    <AlertTriangle className="mr-2 h-4 w-4" />
                    Alerts
                  </button>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <NavigationMenuTrigger>
                    <Shield className="mr-2 h-4 w-4" />
                    AI Agents
                  </NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <div className="grid gap-3 p-6 w-[500px]">
                      <div className="grid grid-cols-1 gap-3">
                        <NavigationMenuLink 
                          className="flex items-center gap-3 p-3 rounded-md hover:bg-accent cursor-pointer"
                          onClick={() => scrollToSection('ai-network')}
                        >
                          <div className="p-2 rounded-md bg-primary/10">
                            <Shield className="h-4 w-4 text-primary" />
                          </div>
                          <div>
                            <div className="text-sm font-medium">Agent Network</div>
                            <div className="text-xs text-muted-foreground">View AI agent workflows and connections</div>
                          </div>
                        </NavigationMenuLink>
                        <NavigationMenuLink 
                          className="flex items-center gap-3 p-3 rounded-md hover:bg-accent cursor-pointer"
                          onClick={() => scrollToSection('ai-agents')}
                        >
                          <div className="p-2 rounded-md bg-secondary/10">
                            <Activity className="h-4 w-4 text-secondary" />
                          </div>
                          <div>
                            <div className="text-sm font-medium">AI Agents Panel</div>
                            <div className="text-xs text-muted-foreground">Monitor AI agent activities</div>
                          </div>
                        </NavigationMenuLink>
                      </div>
                    </div>
                  </NavigationMenuContent>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                    <Users className="mr-2 h-4 w-4" />
                    Users
                  </NavigationMenuLink>
                </NavigationMenuItem>

                <NavigationMenuItem>
                  <button 
                    className={cn(navigationMenuTriggerStyle(), "cursor-pointer")}
                    onClick={() => window.location.href = '/settings'}
                  >
                    <Settings className="mr-2 h-4 w-4" />
                    Settings
                  </button>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardHeader;