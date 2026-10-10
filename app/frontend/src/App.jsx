import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import MRDashboard from './pages/MRDashboard';
import ManagerDashboard from './pages/ManagerDashboard';
import DoctorList from './pages/DoctorList';

function DashboardRouter() {
  const { user } = useAuth();
  if (user?.role === 'manager') return <ManagerDashboard />;
  return <MRDashboard />;
}

function AppLayout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <HashRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />

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

          <Route
            path="/visits"
            element={
              <ProtectedRoute allowedRoles={['mr']}>
                <AppLayout>
                  <MRDashboard />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          <Route
            path="/route"
            element={
              <ProtectedRoute allowedRoles={['mr']}>
                <AppLayout>
                  <MRDashboard />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </HashRouter>
  );
}
