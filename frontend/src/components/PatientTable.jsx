export default function PatientTable({ patients, onEdit, onDelete }) {
  if (patients.length === 0)
    return <p style={{ textAlign: "center", color: "#888" }}>No patients added yet.</p>

  return (
    <div style={{ overflowX: "auto" }}>
      <h2>📋 Patient Records</h2>
      <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", borderRadius: 10, overflow: "hidden", boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
        <thead>
          <tr style={{ background: "#1a73e8", color: "#fff" }}>
            {["Name", "DOB", "Email", "Glucose", "Haemoglobin", "Cholesterol", "AI Remarks", "Actions"].map(h => (
              <th key={h} style={{ padding: "12px 10px", textAlign: "left" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {patients.map((p, i) => (
            <tr key={p.id} style={{ background: i % 2 === 0 ? "#f8f9fa" : "#fff", borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "10px" }}>{p.full_name}</td>
              <td style={{ padding: "10px" }}>{p.date_of_birth}</td>
              <td style={{ padding: "10px" }}>{p.email}</td>
              <td style={{ padding: "10px" }}>{p.glucose}</td>
              <td style={{ padding: "10px" }}>{p.haemoglobin}</td>
              <td style={{ padding: "10px" }}>{p.cholesterol}</td>
              <td style={{ padding: "10px", fontSize: 13, color: "#555", maxWidth: 250 }}>{p.remarks}</td>
              <td style={{ padding: "10px" }}>
                <button onClick={() => onEdit(p)}
                  style={{ marginRight: 8, padding: "6px 12px", background: "#ff9800", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer" }}>
                  Edit
                </button>
                <button onClick={() => onDelete(p.id)}
                  style={{ padding: "6px 12px", background: "#e53935", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer" }}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

