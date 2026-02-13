import { useState } from 'react'
import './App.css'

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState({ text: '', type: '' })
  const [loading, setLoading] = useState(false)
  const [view, setView] = useState('register') // 'register' or 'list'
  const [users, setUsers] = useState([])

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:5001/users')
      const data = await response.json()
      if (response.ok) {
        setUsers(data)
      }
    } catch (error) {
      console.error('Failed to fetch users:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ text: '', type: '' })

    try {
      const response = await fetch('http://localhost:5001/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({ text: data.message, type: 'success' })
        setEmail('')
        setPassword('')
      } else {
        // Updated to use data.message which is our new standard
        setMessage({ text: data.message || 'Something went wrong', type: 'error' })
      }
    } catch (error) {
      setMessage({ text: 'Failed to connect to server', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const toggleView = () => {
    if (view === 'register') {
      fetchUsers()
      setView('list')
    } else {
      setView('register')
    }
  }

  return (
    <div className="container">
      <div className="nav-header">
        <button className="nav-btn" onClick={toggleView}>
          {view === 'register' ? 'View User List' : 'Back to Register'}
        </button>
      </div>

      {view === 'register' ? (
        <>
          <h2>User Registration</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="example@email.com"
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Min 6 characters"
              />
            </div>
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>
          {message.text && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}

          <div className="flow-explanation">
            <h3>How it works:</h3>
            <ol>
              <li><strong>Frontend (React):</strong> This form captures your input and sends a <code>POST</code> request to <code>http://localhost:5001/register</code>.</li>
              <li><strong>Backend (Flask):</strong> The Flask server receives the data, validates the email and password, and checks if the user already exists.</li>
              <li><strong>Database (PostgreSQL):</strong> If everything is valid, Flask saves the user's data into the <code>users</code> table in Postgres.</li>
            </ol>
          </div>
        </>
      ) : (
        <div className="user-list">
          <h2>Registered Users</h2>
          {users.length === 0 ? (
            <p>No users registered yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Email</th>
                  <th>Password</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.email}</td>
                    <td>{user.password}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <button className="refresh-btn" onClick={fetchUsers}>Refresh List</button>
        </div>
      )}
    </div>
  )
}

export default App
