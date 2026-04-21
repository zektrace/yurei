<div align="center">
  <a href="https://github.com/ogkae/yurei/fork">
    <img width="480" alt="yurei banner" src="https://github.com/user-attachments/assets/5dc7c238-f972-4d0e-887a-78eff2492356" />
  </a>

  <code>dependency‑free cryptographic utilities for practical tooling.</code>

  [![Version](https://img.shields.io/badge/version-1.4.1-9b87f5?style=flat-square&logo=python&logoColor=white)](https://github.com/ogkae/yurei)
  [![Python](https://img.shields.io/badge/python-3.10+-9b87f5?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
  [![License](https://img.shields.io/badge/license-MIT-9b87f5?style=flat-square)](./LICENSE)
  [![stdlib](https://img.shields.io/badge/deps-0-9b87f5?style=flat-square)](https://docs.python.org/3/library/index.html)
</div>

---

<table>
<tr>
<td width="50%">
  
### Rationale
- **Robust for tooling:** Explicit validation and safe defaults.
- **Simple:** Minimal API surface, predictable behaviour.
- **Modular:** Single‑responsibility modules.
- **Portable:** Standard library only.

> [!NOTE] 
> `yurei` targets internal scripts and prototypes.  
> For sensitive workloads, prefer audited libraries such as `cryptography` (AES‑GCM / ChaCha20‑Poly1305).

</td>
<td width="50%">

### Installation
```bash
pip install -e .
```

### Quick Example
```python
from yurei import *

uid = uuid4()
pwd = hash_password("SecurePass123!")
assert verify_password(pwd, "SecurePass123!")

secret = os.urandom(32)
token = create_token({"uid": uid}, secret, ttl=3600)
assert verify_token(token, secret)

blob = encrypt_bytes(b"data", b"key")
assert decrypt_bytes(blob, b"key") == b"data"
```

</td>
</tr>
</table>

---

### Module Overview

| Module     | Responsibility                         | Primary Functions                            |
|------------|----------------------------------------|----------------------------------------------|
| `uid`      | identifiers and short tokens           | `uuid4`, `short_id`, `sha256_id`            |
| `auth`     | password hashing                       | `hash_password`, `verify_password`          |
| `session`  | signed tokens with TTL                 | `create_token`, `verify_token`              |
| `cipher`   | lightweight authenticated encryption   | `encrypt_bytes`, `decrypt_bytes`            |
| `store`    | persistent key‑value storage           | `KVStore`                                   |
| `obfusc`   | basic obfuscation                      | `xor_obfuscate`, `xor_deobfuscate`          |

---

### Internal Design (v1.4.1)

- **Pluggable storage backends:** `KVStore` abstracts over `in‑memory` and `sqlite` implementations, enabling future backends (e.g., Redis) without breaking the public API.
- **Clear separation of concerns:** Public facade (`KVStore`) delegates to internal backend modules (`_store_backends`).
- **Extensible architecture:** The structure accommodates new modules while preserving the existing contract.

---

<div align="center">

### zektrace

<a align="center">
</a>

<br />

<table>
<tr>
<td align="center">
  <a href="https://isocpp.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=cplusplus&logoColor=white" /></a>
  <a href="https://rust-lang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=rust&logoColor=white" /></a>
  <a href="https://go.dev"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=go&logoColor=white" /></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=python&logoColor=white" /></a>
  <a href="https://typescriptlang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=typescript&logoColor=white" /></a>
  <a href="https://julialang.org"><img src="https://img.shields.io/badge/%20-000000?style=flat-square&logo=julia&logoColor=white" /></a>
</td>
<td align="center">
  <a href="mailto:stehpenderdealer@proton.me"><code>stehpenderdealer@proton.me</code></a>
</td>
</tr>
</table>

</div>
