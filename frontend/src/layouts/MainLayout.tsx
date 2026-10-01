import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/content', label: 'Content' },
  { to: '/content/new', label: 'Create Post' },
  { to: '/calendar', label: 'Calendar' },
  { to: '/analytics', label: 'Analytics' },
  { to: '/social-accounts', label: 'Social Accounts' },
  { to: '/media', label: 'Media Library' },
  { to: '/notifications', label: 'Notifications' },
  { to: '/settings', label: 'Settings' },
];

export function MainLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">S</div>
          <div>
            <strong>SocialFlow</strong>
            <small>Automation</small>
          </div>
        </div>

        <nav className="sidebar-nav">
          {links.map(({ to, label }) => (
            <NavLink key={to} to={to} className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="user-card">
          <div>
            <strong>{user?.name || 'User'}</strong>
            <small>{user?.email || 'No email'}</small>
          </div>
          <button className="ghost-button" onClick={logout}>Logout</button>
        </div>
      </aside>

      <main className="main-panel">
        <Outlet />
      </main>
    </div>
  );
}
