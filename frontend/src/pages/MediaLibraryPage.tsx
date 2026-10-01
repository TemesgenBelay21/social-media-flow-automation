export function MediaLibraryPage() {
  const media = [
    { name: 'hero-image.png', type: 'Image', size: '2.4 MB' },
    { name: 'ad-video.mp4', type: 'Video', size: '14 MB' },
    { name: 'product-shot.jpg', type: 'Image', size: '1.2 MB' },
  ];

  return (
    <div className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Library</p>
          <h1>Media</h1>
        </div>
        <button className="primary-button">Upload media</button>
      </header>

      <div className="panel">
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Size</th>
            </tr>
          </thead>
          <tbody>
            {media.map((item) => (
              <tr key={item.name}>
                <td>{item.name}</td>
                <td>{item.type}</td>
                <td>{item.size}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
