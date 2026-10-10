import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard, Users, MapPin, Route, Settings, LogOut,
  Stethoscope, ClipboardList, BarChart3
} from 'lucide-react';

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const initials = (user?.name || 'U')
    .split(' ')
    .map((w) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  const mrLinks = [
    { to: '/dashboard', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
    { to: '/visits', icon: <ClipboardList size={18} />, label: 'My Visits' },
    { to: '/doctors', icon: <Stethoscope size={18} />, label: 'Doctors' },
    { to: '/route', icon: <Route size={18} />, label: 'Route Map' },
  ];

  const managerLinks = [
    { to: '/dashboard', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
    { to: '/doctors', icon: <Stethoscope size={18} />, label: 'Doctors' },
    { to: '/analytics', icon: <BarChart3 size={18} />, label: 'Analytics' },
  ];

  const links = user?.role === 'manager' ? managerLinks : mrLinks;

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">
            <MapPin size={22} color="white" />
          </div>
          <h1>
            MR Route
            <span>Optimization System</span>
          </h1>
        </div>
      </div>

      <nav className="sidebar-nav">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            <span className="nav-icon">{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="sidebar-user-avatar">{initials}</div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{user?.name}</div>
            <div className="sidebar-user-role">{user?.role}</div>
          </div>
        </div>
        <button onClick={handleLogout} style={{ color: '#ef4444' }}>
          <LogOut size={18} />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
