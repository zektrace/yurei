<div align="center">
  <h2>Yurei</h2>
  <p>dependency-free cryptographic primitives for internal tooling.</p>
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-black?style=flat-square" alt="python">
    <img src="https://img.shields.io/badge/license-BSD3 Clause-black?style=flat-square" alt="license">
    <img src="https://img.shields.io/badge/status-stable-black?style=flat-square" alt="status">
  </p>
</div>

---

**overview**

yurei *(幽霊 - ghost)* is a minimalist security toolkit designed for environments where external dependencies are restricted. it provides core cryptographic operations using only the python standard library, focusing on ease of use and implementation integrity.

**modules**

- `auth` · timing-safe password hashing via pbkdf2-hmac-sha256.
- `cipher` · authenticated symmetric encryption (encrypt-then-mac).
- `session` · hmac-signed stateful tokens with ttl verification.
- `store` · lightweight persistent or in-memory key-value storage.
- `uid` · cryptographically secure uuid4 and deterministic identifiers.
- `obfusc` · xor-based data obfuscation for non-security contexts.

**usage**

```python
from yurei import encrypt_bytes, decrypt_bytes, hash_password

# authenticated encryption
blob = encrypt_bytes(b"data", b"passphrase")
data = decrypt_bytes(blob, b"passphrase")

# secure hashing
hash = hash_password("secret")
```

**installation**

```bash
pip install git+https://github.com/self-hood/yurei.git@v1.1.3
```

**author**

*self-hood (sh.)*

**license**

[BSD-3-Clause license.](https://github.com/self-hood/yurei/blob/main/LICENSE)
