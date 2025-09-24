import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [list, setList] = useState([]);
  useEffect(() => {
    fetch('/leaderboard.json')
      .then(r => r.json())
      .then(setList)
      .catch(() => {});
  }, []);
  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Uganda Radar – Hot 20</h1>
      <ol className="list-decimal ml-6 space-y-1">
        {list.slice(0, 20).map((t, i) => (
          <li key={i}>
            <a className="text-blue-600 underline" href={t.url} target="_blank" rel="noreferrer">
              {t.title}
            </a>
            <span className="ml-2 text-gray-500">({t.heatscore})</span>
          </li>
        ))}
      </ol>
      <p className="text-xs text-gray-400 mt-6">Updates every 6 h · MVP</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
