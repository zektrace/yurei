**yurei**

technical documentation and usage guide.

---

**philosophy**

yurei is built for speed and zero-dependency environments. it prioritizes the python standard library to eliminate supply-chain risks while maintaining cryptographic integrity.

**core modules**

`uid` · **identity**
- `uuid4()` -> random 128-bit identifier.
- `sha256_id(namespace, name, salt)` -> deterministic hex-id.
- `short_id(length=12)` -> url-safe alphanumeric token.

`auth` · **authentication**
- `hash_password(password, iterations=200_000)` -> pbkdf2-hmac-sha256 string.
- `verify_password(stored, attempt)` -> constant-time boolean check.

`cipher` · **encryption**
- `encrypt_bytes(plaintext, key)` -> authenticated base64url blob.
- `decrypt_bytes(blob_b64, key)` -> original bytes (raises ValueError on tamper).
*note: automatically handles key derivation if the key is a passphrase.*

`session` · **state**
- `create_token(payload, secret, ttl_seconds)` -> signed session token.
- `verify_token(token, secret)` -> dictionary or None if expired/invalid.

`store` · **persistence**
- `KVStore(path=None)` -> sqlite-backed or in-memory key-value store.
- `.set(key, value)` / `.get(key)` / `.delete(key)`.

---

**projects & challenges**

**01 . secure vault**
create a local storage system where filenames are `sha256_id` and contents are `encrypt_bytes`.
```python
id = sha256_id("vault", "notes.txt")
blob = encrypt_bytes(b"content", b"master-key")
# save as {id}.enc
```

**02 . stateless auth**
implement a login system using `hash_password` and generate `session` tokens for users.
```python
token = create_token({"uid": user_id}, b"server-secret", 3600)
```

**03 . data masking**
use `obfusc` to hide internal configuration strings (e.g., database uris) from casual inspection.
```python
masked = xor_obfuscate("postgres://...", b"salt")
```

---

**api reference**

| class / function | input | output |
| :--- | :--- | :--- |
| `KVStore` | `path: str` | `instance` |
| `encrypt_bytes` | `data: bytes, key: bytes` | `str (b64u)` |
| `hash_password` | `pwd: str` | `str (pbkdf2)` |
| `create_token` | `dict, bytes, int` | `str (token)` |

---

**author**

*self-hood (sh.)*
