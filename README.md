<div align="center">
  <a href="https://github.com/ogkae/yurei/fork"><img width="460" alt="banner" src="https://github.com/user-attachments/assets/5dc7c238-f972-4d0e-887a-78eff2492356"/></a>

  **yurei** · librería python sin dependencias externas para utilidades criptográficas prácticas.

  [![Version](https://img.shields.io/badge/version-1.4.1-9b87f5?style=for-the-badge&logo=python)](https://github.com/ogkae/yurei)
  [![Python](https://img.shields.io/badge/python-3.10+-9b87f5?style=for-the-badge&logo=python)](https://www.python.org)
  [![License](https://img.shields.io/badge/license-MIT-9b87f5?style=for-the-badge)](./LICENSE)
</div>

## por qué yurei

- **simple**: api pequeña y directa.
- **modular**: cada módulo cubre una responsabilidad.
- **portable**: solo usa `stdlib`.
- **robusta para tooling interno**: validaciones explícitas y fallos seguros.

> ⚠️ para producción sensible, usa librerías auditadas como `cryptography` con aes-gcm o chacha20-poly1305.

## instalación

```bash
pip install -e .
```

## quick start

```python
from yurei import (
    uuid4,
    hash_password, verify_password,
    create_token, verify_token,
    encrypt_bytes, decrypt_bytes,
    KVStore,
)
import os

uid = uuid4()
pwd = hash_password("SecurePass123!")
assert verify_password(pwd, "SecurePass123!")

secret = os.urandom(32)
token = create_token({"uid": uid, "role": "admin"}, secret, ttl_seconds=3600)
assert verify_token(token, secret) is not None

blob = encrypt_bytes(b"payload", b"passphrase-fuerte")
assert decrypt_bytes(blob, b"passphrase-fuerte") == b"payload"

with KVStore("data.db") as db:
    db.set("user:1", {"uid": uid})
    print(db.get("user:1"))
```

## módulos

| módulo | objetivo | funciones clave |
|---|---|---|
| `uid` | ids y tokens | `uuid4`, `short_id`, `sha256_id` |
| `auth` | hashing de contraseñas | `hash_password`, `verify_password` |
| `session` | tokens firmados con ttl | `create_token`, `verify_token` |
| `cipher` | cifrado autenticado ligero | `encrypt_bytes`, `decrypt_bytes` |
| `store` | persistencia kv | `KVStore` |
| `obfusc` | ofuscación básica | `xor_obfuscate`, `xor_deobfuscate` |

## diseño interno (v1.4.1)

- `store` ahora usa **backends pluggables** (`in-memory` y `sqlite`) para crecer sin romper la api pública.
- separación clara entre capa pública (`KVStore`) y capa interna (`_store_backends`).
- estructura preparada para añadir nuevos backends (ej: redis) manteniendo el mismo contrato.

## hecho por zektrace

```text
<< 匿名性の最大の利点は、あなたが匿名であることだ >>
welcome to my profile
```

<div align="center">
<table>
<tr>
<td align="center">
  <a href="https://isocpp.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=cplusplus&logoColor=white"></a>
  <a href="https://rust-lang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=rust&logoColor=white"></a>
  <a href="https://go.dev"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=go&logoColor=white"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=python&logoColor=white"></a>
  <a href="https://typescriptlang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=typescript&logoColor=white"></a>
  <a href="https://julialang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=julia&logoColor=white"></a>
</td>
<td align="center">
  <a href="mailto:stehpenderdealer@proton.me"><code>stehpenderdealer@proton.me</code></a>
</td>
</tr>
</table>
</div>
