import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard, Users, Route, Settings, LogOut,
  Stethoscope, ClipboardList, BarChart3, Target, MessageSquare,
  X, Navigation, ShieldCheck, MapPin, UserCog
} from 'lucide-react';

export default function Sidebar({ mobileOpen, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    if (onClose) onClose();
    navigate('/login');
  };

  const handleNavClick = () => {
    if (onClose) onClose();
  };

  const initials = (user?.name || 'MR')
    .split(' ')
    .map((w) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  const mrLinks = [
    { to: '/dashboard', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
    { to: '/doctors', icon: <Stethoscope size={18} />, label: 'Doctors' },
    { to: '/predictions', icon: <Target size={18} />, label: 'Visit Prioritization' },
    { to: '/route', icon: <Route size={18} />, label: 'Route Planning' },
    { to: '/visits', icon: <ClipboardList size={18} />, label: 'Visit History' },
    { to: '/whatsapp', icon: <MessageSquare size={18} />, label: 'WhatsApp Hub' },
    { to: '/settings', icon: <Settings size={18} />, label: 'Field Preferences' },
  ];

  const managerLinks = [
    { to: '/dashboard', icon: <LayoutDashboard size={18} />, label: 'Dashboard' },
    { to: '/doctors', icon: <Stethoscope size={18} />, label: 'Doctors' },
    { to: '/predictions', icon: <Target size={18} />, label: 'Visit Prioritization' },
    { to: '/analytics', icon: <BarChart3 size={18} />, label: 'Team Analytics' },
    { to: '/staff', icon: <UserCog size={18} />, label: 'Manage Staff' },
    { to: '/settings', icon: <Settings size={18} />, label: 'System Settings' },
  ];

  const links = user?.role === 'manager' ? managerLinks : mrLinks;

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      <div 
        className={`mobile-overlay ${mobileOpen ? 'visible' : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="sidebar-logo-icon">
              <Navigation size={20} color="white" />
            </div>
            <div>
              <div className="sidebar-logo-title-row">
                <h1>MedRoute</h1>
              </div>
              <span className="sidebar-subtitle">Route & Visit Engine</span>
            </div>
          </div>
          {/* Close button for mobile drawer */}
          <button 
            type="button" 
            className="sidebar-close-btn" 
            onClick={onClose}
            aria-label="Close navigation menu"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="sidebar-nav">
          <div className="sidebar-nav-label">Navigation Menu</div>
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={handleNavClick}
              className={({ isActive }) => isActive ? 'active' : ''}
            >
              <span className="nav-icon">{link.icon}</span>
              <span className="nav-label-text">{link.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-user-avatar">{initials}</div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">{user?.name || 'Parth Lokhande'}</div>
              <div className="sidebar-user-role">
                {user?.role === 'manager' ? 'Territory Manager' : 'Field Rep (MR-4092)'}
              </div>
              <div className="sidebar-user-territory">
                <MapPin size={10} style={{ display: 'inline', marginRight: 3 }} />
                {user?.territory || 'Pune Central & Deccan'}
              </div>
            </div>
          </div>

          <button 
            type="button" 
            className="sidebar-signout-btn" 
            onClick={handleLogout}
            aria-label="Sign out of account"
          >
            <LogOut size={16} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>
    </>
  );
}
