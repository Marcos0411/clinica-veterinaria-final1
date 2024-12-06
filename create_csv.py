import pandas as pd

# Sample data
data = {
    "Nombre": ["Juan Perez", "Maria Lopez"],
    "Telefono": ["123456789", "987654321"],
    "Email": ["juan@example.com", "maria@example.com"],
    "DNI": ["12345678A", "87654321B"],
    "Direccion": ["Calle Falsa 123", "Avenida Siempre Viva 742"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_path = '/home/marcoscabeza/clinica-veterinaria-final1/registroDuenos.csv'
df.to_csv(csv_path, index=False)
