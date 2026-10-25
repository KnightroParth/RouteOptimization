import './LoadingSkeleton.css';

/**
 * Reusable skeleton loader for data-loading states.
 * Variants: card, table, chart, stat
 */
export default function LoadingSkeleton({ variant = 'card', count = 1 }) {
  const items = Array.from({ length: count }, (_, i) => i);

  if (variant === 'stat') {
    return (
      <div className="skeleton-stats-grid">
        {items.map((i) => (
          <div key={i} className="skeleton-stat-card">
            <div className="skeleton-line skeleton-line-sm" style={{ width: '60%' }} />
            <div className="skeleton-line skeleton-line-lg" style={{ width: '40%' }} />
            <div className="skeleton-line skeleton-line-xs" style={{ width: '80%' }} />
          </div>
        ))}
      </div>
    );
  }

  if (variant === 'table') {
    return (
      <div className="skeleton-table">
        <div className="skeleton-table-header">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="skeleton-line skeleton-line-sm" style={{ width: `${60 + i * 5}%` }} />
          ))}
        </div>
        {items.map((i) => (
          <div key={i} className="skeleton-table-row">
            {[1, 2, 3, 4, 5].map((j) => (
              <div key={j} className="skeleton-line skeleton-line-sm" style={{ width: `${50 + j * 8}%` }} />
            ))}
          </div>
        ))}
      </div>
    );
  }

  if (variant === 'chart') {
    return (
      <div className="skeleton-chart">
        <div className="skeleton-chart-bars">
          {[40, 65, 30, 80, 55, 70, 45, 60].map((h, i) => (
            <div key={i} className="skeleton-bar" style={{ height: `${h}%` }} />
          ))}
        </div>
      </div>
    );
  }

  // Default: card
  return (
    <div className="skeleton-cards">
      {items.map((i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton-line skeleton-line-lg" style={{ width: '70%' }} />
          <div className="skeleton-line skeleton-line-sm" style={{ width: '100%' }} />
          <div className="skeleton-line skeleton-line-sm" style={{ width: '85%' }} />
          <div className="skeleton-line skeleton-line-sm" style={{ width: '60%' }} />
        </div>
      ))}
    </div>
  );
}
