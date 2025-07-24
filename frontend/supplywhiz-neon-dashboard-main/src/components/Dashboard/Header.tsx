
import { Bell, Search, Settings, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { useLocation, useNavigate } from "react-router-dom";

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const isActiveRoute = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="glass-card h-16 px-6 flex items-center justify-between border-b border-white/10">
      {/* Logo Section */}
      <div className="flex items-center space-x-8">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate("/")}>
          <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-lg">S</span>
          </div>
          <h1 className="text-xl font-bold text-gradient-primary">SupplyWhiz</h1>
        </div>
        
        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <Button 
            variant="ghost" 
            className={`font-medium ${isActiveRoute("/") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/")}
          >
            Dashboard
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/alerts") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/alerts")}
          >
            Alerts
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/analytics") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/analytics")}
          >
            Analytics
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/map") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/map")}
          >
            Map
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/monitoring") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/monitoring")}
          >
            Monitoring
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/agents") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/agents")}
          >
            AI Agents
          </Button>
          <Button 
            variant="ghost" 
            className={`${isActiveRoute("/settings") ? "text-primary hover:text-primary/80" : "hover:text-foreground"}`}
            onClick={() => navigate("/settings")}
          >
            Settings
          </Button>
        </nav>
      </div>

      {/* Right Section */}
      <div className="flex items-center space-x-4">
        {/* Search */}
        <div className="relative hidden md:block">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <Input 
            placeholder="Search..." 
            className="pl-10 w-64 bg-muted/50 border-white/10 focus:border-primary/50"
          />
        </div>

        {/* Notifications */}
        <Button variant="ghost" size="icon" className="relative hover:bg-muted/50">
          <Bell className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-destructive rounded-full animate-pulse"></span>
        </Button>

        {/* Settings */}
        <Button 
          variant="ghost" 
          size="icon" 
          className="hover:bg-muted/50"
          onClick={() => navigate("/settings")}
        >
          <Settings className="w-5 h-5" />
        </Button>

        {/* User Avatar */}
        <Avatar className="border-2 border-primary/20">
          <AvatarImage src="/placeholder.svg" />
          <AvatarFallback className="bg-gradient-primary text-primary-foreground">
            JD
          </AvatarFallback>
        </Avatar>
      </div>
    </header>
  );
};

export default Header;
