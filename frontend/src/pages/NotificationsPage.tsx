export function NotificationsPage() {
  const notifications = [
    { title: 'Post published', body: 'Your Instagram post went live successfully.' },
    { title: 'Approval required', body: 'TikTok publishing access is waiting for app review.' },
    { title: 'Account status', body: 'Telegram bot connection remains active.' },
  ];

  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Inbox</p>
          <h1>Notifications</h1>
        </div>
      </header>

      <div className="panel">
        {notifications.map((item) => (
          <div key={item.title} className="notification-item">
            <strong>{item.title}</strong>
            <p>{item.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
