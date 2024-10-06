import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [view, setView] = useState('menu'); // Possible values: 'menu', 'login', 'signup'
  const [message, setMessage] = useState('');
  const [credentials, setCredentials] = useState({ username: '', password: '' });

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e, endpoint) => {
    e.preventDefault();
    setMessage('');

    try {
      const response = await axios.post(`http://13.58.192.2:8000/${endpoint}`, credentials);
      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
      if (error.response && error.response.data && error.response.data.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage(`An error occurred during ${endpoint}.`);
      }
    }
  };

  const renderForm = (type) => (
    <form onSubmit={(e) => handleSubmit(e, type)}>
      <h2>{type === 'login' ? 'Login' : 'Sign Up'}</h2>
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={credentials.username}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={credentials.password}
        onChange={handleChange}
        required
      />
      <button type="submit">{type === 'login' ? 'Login' : 'Sign Up'}</button>
      <button type="button" onClick={() => setView('menu')}>Back</button>
    </form>
  );

  return (
    <div className="App">
      <h1>User Authentication</h1>
      {view === 'menu' && (
        <div>
          <button onClick={() => setView('login')}>Login</button>
          <button onClick={() => setView('signup')}>Sign Up</button>
        </div>
      )}
      {view === 'login' && renderForm('login')}
      {view === 'signup' && renderForm('signup')}
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
