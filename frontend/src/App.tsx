import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [health, setHealth] = useState<string>('Loading...')

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/health`)
        const data = await response.json()
        setHealth(JSON.stringify(data, null, 2))
      } catch (error) {
        setHealth(`Error: ${error instanceof Error ? error.message : String(error)}`)
      }
    }

    checkHealth()
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">AI Learning Path System</h1>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Backend Health Status</h2>
          <pre className="bg-gray-50 p-4 rounded-md">
            {health}
          </pre>
        </div>
      </div>
    </div>
  )
}

export default App
