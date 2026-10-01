export function SettingsPage() {
  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Preferences</p>
          <h1>Settings</h1>
        </div>
      </header>

      <div className="panel settings-grid">
        <div>
          <h3>Profile</h3>
          <label>
            Full name
            <input defaultValue="Alice Example" />
          </label>
        </div>
        <div>
          <h3>Security</h3>
          <label>
            Timezone
            <input defaultValue="UTC" />
          </label>
        </div>
      </div>
    </div>
  );
}
