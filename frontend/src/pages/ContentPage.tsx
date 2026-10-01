export function ContentPage() {
  const items = [
    { title: 'Product launch teaser', status: 'Scheduled', platform: 'Instagram + Facebook' },
    { title: 'Creator announcement', status: 'Draft', platform: 'Telegram' },
    { title: 'Brand campaign video', status: 'Published', platform: 'TikTok' },
  ];

  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Content library</p>
          <h1>Content</h1>
        </div>
        <button className="primary-button">Create post</button>
      </header>

      <div className="panel">
        <table className="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Platforms</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.title}>
                <td>{item.title}</td>
                <td>{item.platform}</td>
                <td><span className="status-pill">{item.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
