import { useState, useEffect } from "react"

const emptyForm = {
  full_name: "", date_of_birth: "", email: "",
  glucose: "", haemoglobin: "", cholesterol: ""
}

export default function PatientForm({ onSubmit, editingPatient, onCancel, loading }) {
  const [form, setForm] = useState(emptyForm)
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (editingPatient) {
      setForm({
        full_name: editingPatient.full_name,
        date_of_birth: editingPatient.date_of_birth,
        email: editingPatient.email,
        glucose: editingPatient.glucose,
        haemoglobin: editingPatient.haemoglobin,
        cholesterol: editingPatient.cholesterol,
      })
    } else {
      setForm(emptyForm)
    }
  }, [editingPatient])

  const validate = () => {
    const e = {}
    if (!form.full_name.trim()) e.full_name = "Name is required"
    if (!form.date_of_birth) e.date_of_birth = "Date of birth is required"
    else if (new Date(form.date_of_birth) > new Date()) e.date_of_birth = "Cannot be a future date"
    if (!form.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) e.email = "Invalid email"
    if (isNaN(form.glucose) || form.glucose <= 0) e.glucose = "Must be a positive number"
    if (isNaN(form.haemoglobin) || form.haemoglobin <= 0) e.haemoglobin = "Must be a positive number"
    if (isNaN(form.cholesterol) || form.cholesterol <= 0) e.cholesterol = "Must be a positive number"
    return e
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) { setErrors(errs); return }
    setErrors({})
    onSubmit({ ...form, glucose: +form.glucose, haemoglobin: +form.haemoglobin, cholesterol: +form.cholesterol })
    setForm(emptyForm)
  }

  const field = (label, name, type = "text") => (
    <div style={{ marginBottom: "1rem" }}>
      <label style={{ display: "block", marginBottom: 4, fontWeight: 500 }}>{label}</label>
      <input
        type={type} name={name} value={form[name]} onChange={handleChange}
        style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: errors[name] ? "1px solid red" : "1px solid #ccc", boxSizing: "border-box" }}
      />
      {errors[name] && <span style={{ color: "red", fontSize: 12 }}>{errors[name]}</span>}
    </div>
  )

  return (
    <div style={{ background: "#f8f9fa", padding: "1.5rem", borderRadius: 10, marginBottom: "2rem", boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
      <h2 style={{ marginTop: 0 }}>{editingPatient ? "✏️ Edit Patient" : "➕ Add New Patient"}</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 1.5rem" }}>
          {field("Full Name", "full_name")}
          {field("Date of Birth", "date_of_birth", "date")}
          {field("Email Address", "email", "email")}
          {field("Glucose (mg/dL)", "glucose", "number")}
          {field("Haemoglobin (g/dL)", "haemoglobin", "number")}
          {field("Cholesterol (mg/dL)", "cholesterol", "number")}
        </div>
        <div style={{ display: "flex", gap: "1rem" }}>
          <button type="submit" disabled={loading}
            style={{ padding: "10px 24px", background: "#1a73e8", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 600 }}>
            {loading ? "Getting AI Prediction..." : editingPatient ? "Update Patient" : "Add Patient"}
          </button>
          {editingPatient && (
            <button type="button" onClick={onCancel}
              style={{ padding: "10px 24px", background: "#e0e0e0", border: "none", borderRadius: 6, cursor: "pointer" }}>
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

