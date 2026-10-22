import { useState } from 'react';
import { HashRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Sidebar from './components/Sidebar';
import MobileNav from './components/MobileNav';

// Pages
import Login from './pages/Login';
import MRDashboard from './pages/MRDashboard';
import ManagerDashboard from './pages/ManagerDashboard';
import DoctorList from './pages/DoctorList';
import MLPredictions from './pages/MLPredictions';
import RoutePlanning from './pages/RoutePlanning';
import VisitHistory from './pages/VisitHistory';
import WhatsApp from './pages/WhatsApp';
import Settings from './pages/Settings';
import Analytics from './pages/Analytics';
import ManageStaff from './pages/ManageStaff';

function DashboardRouter() {
  const { user } = useAuth();
  if (user?.role === 'manager') return <ManagerDashboard />;
  return <MRDashboard />;
}

function AppLayout({ children }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="app-layout">
      {/* Mobile Top Navbar (Visible on screens <= 768px) */}
      <MobileNav onOpenMenu={() => setMobileMenuOpen(true)} />

      {/* Desktop & Mobile Drawer Sidebar */}
      <Sidebar 
        mobileOpen={mobileMenuOpen} 
        onClose={() => setMobileMenuOpen(false)} 
      />

      {/* Main Page Content */}
      <main className="main-content" key={location.pathname}>
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <HashRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Unified Dashboard (MR & Manager) */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <DashboardRouter />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Doctors Database */}
          <Route
            path="/doctors"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <DoctorList />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* ML Model Predictions & Feature Importance */}
          <Route
            path="/predictions"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <MLPredictions />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Route Planning (OR-Tools VRPTW Engine) */}
          <Route
            path="/route"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <RoutePlanning />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Visit History & Detailing Logs */}
          <Route
            path="/visits"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <VisitHistory />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* WhatsApp Field Hub */}
          <Route
            path="/whatsapp"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <WhatsApp />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Field Representative Preferences & Settings */}
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Settings />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Manager Team Analytics */}
          <Route
            path="/analytics"
            element={
              <ProtectedRoute allowedRoles={['manager']}>
                <AppLayout>
                  <Analytics />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Manager Staff Management */}
          <Route
            path="/staff"
            element={
              <ProtectedRoute allowedRoles={['manager']}>
                <AppLayout>
                  <ManageStaff />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Root and Fallback redirects */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </HashRouter>
  );
}
