export function DashboardPage() {
  const metrics = [
    { label: 'Connected accounts', value: '12', tone: 'blue' },
    { label: 'Scheduled posts', value: '38', tone: 'green' },
    { label: 'Published', value: '148', tone: 'purple' },
    { label: 'Failed', value: '4', tone: 'red' },
  ];

  const recentPosts = [
    { title: 'Summer campaign teaser', platform: 'Instagram', status: 'Published' },
    { title: 'Telegram product update', platform: 'Telegram', status: 'Scheduled' },
    { title: 'Launch countdown', platform: 'Facebook', status: 'Draft' },
  ];

  const upcomingPosts = [
    { time: 'Today 14:00', title: 'Creator Q&A post' },
    { time: 'Tomorrow 08:30', title: 'Campaign recap' },
    { time: 'Wed 17:45', title: 'Flash sale announcement' },
  ];

  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Overview</p>
          <h1>Dashboard</h1>
        </div>
      </header>

      <section className="metrics-grid">
        {metrics.map((metric) => (
          <div key={metric.label} className={`metric-card ${metric.tone}`}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </div>
        ))}
      </section>

      <section className="two-column-grid">
        <div className="panel">
          <h2>Recent content</h2>
          <ul className="list">
            {recentPosts.map((post) => (
              <li key={post.title}>
                <div>
                  <strong>{post.title}</strong>
                  <small>{post.platform}</small>
                </div>
                <span className="status-pill">{post.status}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h2>Upcoming posts</h2>
          <ul className="list">
            {upcomingPosts.map((item) => (
              <li key={item.title}>
                <div>
                  <strong>{item.title}</strong>
                  <small>{item.time}</small>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
