import React from 'react';
import { Menu, Navigation } from 'lucide-react';

export default function MobileNav({ onOpenMenu }) {
  return (
    <header className="mobile-topbar">
      <div className="mobile-topbar-brand">
        <div className="mobile-logo-icon">
          <Navigation size={18} color="white" />
        </div>
        <div className="mobile-brand-text">
          <div className="mobile-brand-title">MedRoute</div>
          <span className="mobile-brand-subtitle">Route & Visit Engine</span>
        </div>
      </div>
      <button 
        type="button" 
        className="mobile-menu-trigger" 
        onClick={onOpenMenu}
        aria-label="Toggle navigation drawer"
      >
        <Menu size={22} />
      </button>
    </header>
  );
}
