import { lazy, Suspense, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { HashRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Sidebar from './components/Sidebar';
import MobileNav from './components/MobileNav';

// Pages
const Login = lazy(() => import('./pages/Login'));
const MRDashboard = lazy(() => import('./pages/MRDashboard'));
const ManagerDashboard = lazy(() => import('./pages/ManagerDashboard'));
const DoctorList = lazy(() => import('./pages/DoctorList'));
const MLPredictions = lazy(() => import('./pages/MLPredictions'));
const RoutePlanning = lazy(() => import('./pages/RoutePlanning'));
const VisitHistory = lazy(() => import('./pages/VisitHistory'));
const WhatsApp = lazy(() => import('./pages/WhatsApp'));
const Settings = lazy(() => import('./pages/Settings'));
const Analytics = lazy(() => import('./pages/Analytics'));
const ManageStaff = lazy(() => import('./pages/ManageStaff'));

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
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(15, 23, 42, 0.95)',
              color: '#e2e8f0',
              border: '1px solid rgba(99, 102, 241, 0.2)',
              borderRadius: '10px',
              backdropFilter: 'blur(12px)',
              fontSize: '13px',
            },
            success: { iconTheme: { primary: '#10b981', secondary: '#0f172a' } },
            error: { iconTheme: { primary: '#ef4444', secondary: '#0f172a' }, duration: 5000 },
          }}
        />
        <Suspense fallback={<div className="page-loader">Loading...</div>}>
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
        </Suspense>
      </AuthProvider>
    </HashRouter>
  );
}
