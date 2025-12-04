from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def generate_worm_keys():
    # Generar clave privada ECDSA P-256
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Serializar clave privada
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serializar clave pública
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    print("=== WORM_PRIVATE_KEY (copiar a .env) ===")
    private_str = private_pem.decode("utf-8")
    print(private_str)

    # Guardar en archivos
    with open("worm_private_key.pem", "w") as f:
        f.write(private_str)
    with open("worm_public_key.pem", "w") as f:
        f.write(public_pem.decode("utf-8"))

    print("\n✅ Claves generadas en worm_private_key.pem y worm_public_key.pem")


if __name__ == "__main__":
    generate_worm_keys()
