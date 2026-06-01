import { useState, useEffect } from "react"
import PatientForm from "./components/PatientForm"
import PatientTable from "./components/PatientTable"
import axios from "axios"

const API = "http://localhost:8000"

export default function App() {
  const [patients, setPatients] = useState([])
  const [editingPatient, setEditingPatient] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchPatients = async () => {
    const res = await axios.get(`${API}/patients`)
    setPatients(res.data)
  }

  useEffect(() => { fetchPatients() }, [])

  const handleSubmit = async (formData) => {
    setLoading(true)
    try {
      if (editingPatient) {
        await axios.put(`${API}/patients/${editingPatient.id}`, formData)
      } else {
        await axios.post(`${API}/patients`, formData)
      }
      setEditingPatient(null)
      await fetchPatients()
    } catch (err) {
      alert(err.response?.data?.detail || "Something went wrong")
    }
    setLoading(false)
  }

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this patient?")) return
    await axios.delete(`${API}/patients/${id}`)
    await fetchPatients()
  }

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "2rem", fontFamily: "Segoe UI, sans-serif" }}>
      <h1 style={{ color: "#1a73e8", textAlign: "center" }}>🏥 MIRA — Health Prediction System</h1>
      <PatientForm
        onSubmit={handleSubmit}
        editingPatient={editingPatient}
        onCancel={() => setEditingPatient(null)}
        loading={loading}
      />
      <PatientTable
        patients={patients}
        onEdit={setEditingPatient}
        onDelete={handleDelete}
      />
    </div>
  )
}

