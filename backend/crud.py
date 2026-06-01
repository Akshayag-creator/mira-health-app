from database import get_connection

def get_all_patients():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def get_patient(patient_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row

def create_patient(patient: dict):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        patient["full_name"], patient["date_of_birth"], patient["email"],
        patient["glucose"], patient["haemoglobin"], patient["cholesterol"], patient["remarks"]
    ))
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return get_patient(new_id)

def update_patient(patient_id: int, patient: dict):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE patients
        SET full_name=%s, date_of_birth=%s, email=%s,
            glucose=%s, haemoglobin=%s, cholesterol=%s, remarks=%s
        WHERE id=%s
    """, (
        patient["full_name"], patient["date_of_birth"], patient["email"],
        patient["glucose"], patient["haemoglobin"], patient["cholesterol"],
        patient["remarks"], patient_id
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return get_patient(patient_id)

def delete_patient(patient_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
    connection.commit()
    affected = cursor.rowcount
    cursor.close()
    connection.close()
    return affected > 0

