# Virtualizor Forwarding Tool

CLI tool untuk mengelola domain/port forwarding di lingkungan VPS Virtualizor dengan dukungan multi-host dan Rich TUI.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🖥️ **Multi-Host Support** - Kelola beberapa server Virtualizor dari satu interface
- 🎨 **Rich TUI** - Output terminal yang informatif dengan tabel, panel, dan progress bar
- 🔄 **CRUD Operations** - Add, edit, delete forwarding rules dengan mudah
- 📦 **Batch Operations** - Import/export rules dalam format JSON
- 🔐 **Secure Config** - Password tersimpan dengan encoding base64
- 🐍 **Python 3.8-3.13** - Kompatibel dengan berbagai versi Python

## Installation

```bash
# Install dari PyPI (coming soon)
pip install vf-forwarding

# Atau install dari source
git clone https://github.com/iam-rizz/python-domain-forwarding-virtualizor.git
cd python-domain-forwarding-virtualizor
pip install -e .
```

Dependencies (`requests`, `rich`) akan otomatis terinstall.

## Quick Start

### 1. Konfigurasi Host

```bash
# Tambah host baru
vf config add myhost \
  --url "https://panel.example.com:4083/index.php" \
  --key "your_api_key" \
  --pass "your_api_password" \
  --default

# Lihat daftar host
vf config list

# Test koneksi
vf config test
```

### 2. Lihat Virtual Machines

```bash
# Lihat semua VM
vf vm list

# Filter VM yang aktif
vf vm list --status up

# Output JSON
vf vm list --json
```


### 3. Kelola Port Forwarding

```bash
# Lihat forwarding rules
vf forward list --vpsid 103

# Tambah HTTP forwarding (auto port 80)
vf forward add \
  --vpsid 103 \
  --protocol HTTP \
  --domain app.example.com

# Tambah HTTPS forwarding (auto port 443)
vf forward add \
  --vpsid 103 \
  --protocol HTTPS \
  --domain secure.example.com

# Tambah TCP forwarding (manual ports)
vf forward add \
  --vpsid 103 \
  --protocol TCP \
  --domain 45.158.126.130 \
  --src-port 2222 \
  --dest-port 22

# Mode interaktif
vf forward add --interactive

# Edit forwarding
vf forward edit \
  --vpsid 103 \
  --vdfid 596 \
  --protocol HTTPS

# Hapus forwarding
vf forward delete --vpsid 103 --vdfid 596

# Hapus multiple (dengan konfirmasi)
vf forward delete --vpsid 103 --vdfid 596,597,598

# Hapus tanpa konfirmasi
vf forward delete --vpsid 103 --vdfid 596 --force
```

### 4. Batch Operations

```bash
# Export rules ke JSON
vf batch export --vpsid 103 --to-file rules.json

# Import rules dari JSON
vf batch import --vpsid 103 --from-file rules.json

# Dry run (validasi saja)
vf batch import --vpsid 103 --from-file rules.json --dry-run
```

## Configuration

Config file disimpan di `~/.config/virtualizor-forwarding/config.json`:

```json
{
  "hosts": {
    "production": {
      "name": "production",
      "api_url": "https://panel.example.com:4083/index.php",
      "api_key": "your_api_key",
      "api_pass": "base64_encoded_password"
    },
    "staging": {
      "name": "staging",
      "api_url": "https://staging.example.com:4083/index.php",
      "api_key": "staging_api_key",
      "api_pass": "base64_encoded_password"
    }
  },
  "default_host": "production",
  "version": "1.0"
}
```

## Batch Import Format

File JSON untuk batch import:

```json
{
  "rules": [
    {
      "protocol": "HTTP",
      "src_hostname": "app1.example.com",
      "src_port": 80,
      "dest_ip": "10.0.0.1",
      "dest_port": 80
    },
    {
      "protocol": "HTTPS",
      "src_hostname": "app2.example.com",
      "src_port": 443,
      "dest_ip": "10.0.0.1",
      "dest_port": 443
    }
  ]
}
```


## Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--host NAME` | `-H` | Gunakan host profile tertentu |
| `--no-color` | | Nonaktifkan output berwarna |
| `--verbose` | `-v` | Output verbose |
| `--debug` | | Mode debug |

## Commands Reference

### Config Commands

| Command | Description |
|---------|-------------|
| `config add NAME` | Tambah host profile baru |
| `config remove NAME` | Hapus host profile |
| `config list` | Lihat semua host profiles |
| `config set-default NAME` | Set default host |
| `config test [NAME]` | Test koneksi ke host |

### VM Commands

| Command | Description |
|---------|-------------|
| `vm list` | Lihat daftar VM |
| `vm list --status up` | Filter VM aktif |
| `vm list --all-hosts` | Lihat VM dari semua host |

### Forward Commands

| Command | Description |
|---------|-------------|
| `forward list` | Lihat forwarding rules |
| `forward add` | Tambah forwarding rule |
| `forward edit` | Edit forwarding rule |
| `forward delete` | Hapus forwarding rule(s) |

### Batch Commands

| Command | Description |
|---------|-------------|
| `batch import` | Import rules dari JSON |
| `batch export` | Export rules ke JSON |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=virtualizor_forwarding
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Author

**Rizky Adhy Pratama**
- Email: rizkyadhypratama@gmail.com
- GitHub: [@iam-rizz](https://github.com/iam-rizz)
