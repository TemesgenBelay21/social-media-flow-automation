export function SocialAccountsPage() {
  const accounts = [
    { platform: 'Instagram', status: 'Connected', username: '@brandstudio' },
    { platform: 'Facebook', status: 'Connected', username: 'Brand Studio Page' },
    { platform: 'TikTok', status: 'Pending approval', username: '@brandstudio' },
    { platform: 'Telegram', status: 'Connected', username: '@socialflow_bot' },
  ];

  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Integrations</p>
          <h1>Social Accounts</h1>
        </div>
      </header>

      <div className="card-grid">
        {accounts.map((account) => (
          <div key={account.platform} className="account-card">
            <div className="account-card-header">
              <h3>{account.platform}</h3>
              <span className="status-pill">{account.status}</span>
            </div>
            <p>{account.username}</p>
            <button className="ghost-button">Disconnect</button>
          </div>
        ))}
      </div>
    </div>
  );
}
