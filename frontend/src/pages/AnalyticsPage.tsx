export function AnalyticsPage() {
  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Insights</p>
          <h1>Analytics</h1>
        </div>
      </header>

      <div className="metrics-grid">
        <div className="metric-card blue"><span>Impressions</span><strong>128K</strong></div>
        <div className="metric-card green"><span>Reach</span><strong>94K</strong></div>
        <div className="metric-card purple"><span>Engagement</span><strong>4.8%</strong></div>
        <div className="metric-card red"><span>Clicks</span><strong>3.2K</strong></div>
      </div>
    </div>
  );
}
