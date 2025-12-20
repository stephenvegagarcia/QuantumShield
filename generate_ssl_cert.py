#!/usr/bin/env python3
"""
SSL Certificate Generator for QuantumShield
Generates self-signed SSL certificates for HTTPS
"""

from OpenSSL import crypto
import os

def generate_self_signed_cert(cert_dir="./ssl"):
    """
    Generate self-signed SSL certificate for HTTPS
    """
    # Create SSL directory if it doesn't exist
    os.makedirs(cert_dir, exist_ok=True)
    
    cert_file = os.path.join(cert_dir, "cert.pem")
    key_file = os.path.join(cert_dir, "key.pem")
    
    # Check if certificates already exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"✅ SSL certificates already exist at {cert_dir}/")
        return cert_file, key_file
    
    # Create key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)  # 4096-bit RSA key
    
    # Create certificate
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "California"
    cert.get_subject().L = "San Francisco"
    cert.get_subject().O = "QuantumShield Security"
    cert.get_subject().OU = "Security Division"
    cert.get_subject().CN = "localhost"
    
    # Set serial number and validity
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for 1 year
    
    # Set issuer and public key
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    
    # Add extensions for enhanced security
    cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        crypto.X509Extension(b"keyUsage", False, b"digitalSignature, keyEncipherment"),
        crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth"),
        crypto.X509Extension(b"subjectAltName", False, b"DNS:localhost, DNS:127.0.0.1, IP:127.0.0.1"),
    ])
    
    # Sign certificate with private key
    cert.sign(key, 'sha256')
    
    # Write certificate file
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    # Write private key file
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    print(f"✅ SSL certificate generated successfully!")
    print(f"   Certificate: {cert_file}")
    print(f"   Private Key: {key_file}")
    print(f"   Valid for: 365 days")
    print(f"   Key Size: 4096-bit RSA")
    
    return cert_file, key_file


if __name__ == "__main__":
    generate_self_signed_cert()
