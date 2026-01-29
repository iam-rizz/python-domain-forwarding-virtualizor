# Virtualizor Forwarding Tool (vf)

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey" alt="Platform">
</p>

<p align="center">
  <a href="https://sonarqube.rizzcode.id/dashboard?id=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3"><img src="https://sonarqube.rizzcode.id/api/project_badges/measure?project=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3&metric=alert_status&token=sqb_e60dd5ca23f95574dc0f802335bda3563a86cb81" alt="Quality Gate Status"></a>
  <a href="https://sonarqube.rizzcode.id/dashboard?id=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3"><img src="https://sonarqube.rizzcode.id/api/project_badges/measure?project=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3&metric=software_quality_security_rating&token=sqb_e60dd5ca23f95574dc0f802335bda3563a86cb81" alt="Security Rating"></a>
  <a href="https://sonarqube.rizzcode.id/dashboard?id=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3"><img src="https://sonarqube.rizzcode.id/api/project_badges/measure?project=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3&metric=software_quality_reliability_rating&token=sqb_e60dd5ca23f95574dc0f802335bda3563a86cb81" alt="Reliability Rating"></a>
  <a href="https://sonarqube.rizzcode.id/dashboard?id=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3"><img src="https://sonarqube.rizzcode.id/api/project_badges/measure?project=iam-rizz_python-domain-forwarding-virtualizor_288276e0-63bb-476b-a1a6-14ae07eee7a3&metric=ncloc&token=sqb_e60dd5ca23f95574dc0f802335bda3563a86cb81" alt="Lines of Code"></a>
</p>

CLI tool untuk mengelola domain/port forwarding di lingkungan VPS Virtualizor dengan dukungan multi-host dan Rich TUI.

**[🇬🇧 Read in English](README.md)**

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Persyaratan](#-persyaratan)
- [Instalasi](#-instalasi)
- [Quick Start](#-quick-start)
- [Penggunaan](#-penggunaan)
- [File Konfigurasi](#-file-konfigurasi)
- [Referensi Command](#-referensi-command)
- [Contoh](#-contoh)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## ✨ Fitur

| Fitur | Deskripsi |
|-------|-----------|
| **Multi-Host Support** | Kelola beberapa server Virtualizor dari satu interface |
| **Rich TUI** | Output terminal yang informatif dengan tabel, panel, dan progress bar |
| **CRUD Operations** | Add, edit, delete forwarding rules dengan mudah |
| **Batch Operations** | Import/export rules dalam format JSON |
| **Secure Config** | Password tersimpan dengan encoding base64 |
| **Python 3.8-3.13** | Kompatibel dengan berbagai versi Python |
| **Interactive Mode** | Mode step-by-step untuk pemula |
| **JSON Output** | Export data dalam format JSON untuk scripting |

## Persyaratan

- Python 3.8 atau lebih baru
- Akses ke Virtualizor Panel dengan API credentials
- Network access ke server Virtualizor

## Instalasi

### Dari PyPI (Recommended)

```bash
pip install vf-forwarding
```

### Dari Source

```bash
git clone https://github.com/iam-rizz/python-domain-forwarding-virtualizor.git
cd python-domain-forwarding-virtualizor
pip install -e .
```

### Verifikasi Instalasi

```bash
vf --help
```

> **Note:** Dependencies (`requests`, `rich`) akan otomatis terinstall.

## Quick Start

```bash
# 1. Tambah host configuration
vf config add production \
  --url "https://panel.example.com:4083/index.php" \
  --key "YOUR_API_KEY" \
  --pass "YOUR_API_PASSWORD" \
  --default

# 2. Test koneksi
vf config test

# 3. Lihat daftar VM
vf vm list

# 4. Tambah forwarding rule (interactive)
vf forward add -i
```


## Penggunaan

##igurasi

#### Tambah Host Profile

```bash
# Basic
vf config add myhost --url "https://panel.com:4083/index.php" --key "apikey" --pass "password"

# Dengan set sebagai default
vf config add myhost --url "https:index.php" --key "apikey" --pass "password" --default
```

#### Kelola Host Profiles

```bash
# Lihat semua host
vf config list

# Set default host
vf config set-default production

# Test koneksi
vf config test              # Test default host config test staging      # Test specific host

# Hapus host
vf config remove staging
```

#### Gunakan Host Tertentu

```bash
# Gunakan --host atau -H untuk operasi dengan host tertentu
vf --host stagin
vf -H production forward list --vpsid 103
```

### 2. Virtual Machines

```bash
# Lihat semua VM
vf vm list

# Filter berdasarkan status
vf vm list --status up      # Hanya VM yang running
vf vm list --status down    # Hanya VM yang stopped

# Lihat VM dari semua host
vf vm list --all-hosts

# Output JSON (untuk scripting)
vf vm list --json
vf vm list --status up --json
```

### 3. Port Forwarding

#### Lihat Forwarding Rules

```bash
# Interactive (pilih VM dari list)
vf forward list

# Langsung ke VM tertentu
vf forward list --vpsid 103
vf forward list -v 103

# Auto-select jika hanya 1 VM
vf forward list --auto

# Output JSONforward list --vpsid 103 --json
```

#### Tambah Forwarding Rule

```bash
# Mode Interactive (recommended untuk pemula)
vf forward add -i
vf forward add --interactive

# HTTP Forwarding (auto port 80)
vf forward add --vpsid 103 --protocol HTTP --domain appom

# HTTPS Forwarding (auto port 443)
vf forward add --vpsid 103 --protocol HTTPS --domain secure.example.com

# TCP Forwarding (custom ports)
vf forward add \
  --vpsid 103 \
  --protocol TCP \
  --domain 45.158.126.xxx \
  --src-port 2222 \
  --dest-port 22

# Short options
vf forward add -v 103 -p HTTP -d app.example.com
vf forward add -v 103 -p TCP -d 45.158.126.xxx -s 2222 -t 22
```

#### Edit Forwarding Rule

```bash
# Mode Interactive
vf forward edit -i

# Edit protocol (auto-update ports)
vf forward edit --vpsid 103 --vdfid 596 --protocol HTTPS

# Edit domain
vf forward edit --vpsid 103 --vdfid 596 --domain new.example.com

# Edit ports
vf forward edit --vpsid 103 --vdfid 596 --src-port 8080 --dest-port 80

# Short options
vf forward edit -v 103 -f 596 -p HTTPS -d new.example.com
```

#### Hapus Forwarding Rule

```bash
# Mode Interactive (dengan konfirmasi)
vf forward delete -i

# Hapus single rule (dengan konfirmasi)
vf forward delete --vpsid 103 --vdfid 596

# Hapus multiple rules
vf forward delete --vpsid 103 --vdfid 596,597,598

# Hapus tanpa konfirmasi
vf forward delete --vpsid 103 --vdfid 596 --force

# Short options
vf forward delete -v 103 -f 596
vf forward delete -v 103 -f 596,597 --force
```

Batch Operations

#### Export Rules

```bash
# Export ke file JSON
vf batch export --vpsid 103 --to-file rules.json
vf batch export -v 103 -o backup.json
```

#### Import Rules

```bash
# Import dari file JSON
vf batch import --vpsid 103 --from-file rules.json
Dry run (validasi tanpa execute)
vf batch import --vpsid 103 --from-file rules.json --dry-run

# Short options
vf batch import -v 103 -f rules.json
vf batch import -v 103 -f rules.json --dry-run
```

## File Konfigurasi

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

### Format Batch Import/Export

```json
{
  "vpsid": "103",
  "rul": [
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
      "dest_ip".0.1",
      "dest_port": 443
    },
    {
      "protocol": "TCP",
      "src_hostname": "45.158.126.xxx",
      "src_port": 2222,
      "dest_ip": "10.0.0.1",
      "dest_port": 22
    }
  ]
}
```


## Referensi Command

### Global Options

| Option | Short | Deskripsi |
|--------|-------|-----------|
| `--host NAME` | `-H` | Gunakan host profile tertentu |
| `--no-color` | | Nonaktifkan output berwarna |
| `--verbose` | `-v` | Output verbose |
| `--debug` | | Mode debug (tampilkan stack traces) |
| `--help` | `-h` | Tampilkan bantuan |

### Config Commands

| Command | Deskripsi |
|---------|-----------|
| `vf config add NAME` | Tambah host profile baru |
| `vf config remove NAME` | Hapus host profile |
| `vf config list` | Lihat semua host profiles |
| `vf config set-default NAME` | Set default host |
| `vf config test [NAME]` | Test koneksi ke host |

### VM Commands

| Command | Deskripsi |
|---------|-----------|
| `vf vm list` | Lihat daftar VM |
| `vf vm list --status up/down` | Filter VM berdasarkan status |
| `vf vm list --all-hosts` | Lihat VM dari semua host |
| `vf vm list --json` | Output dalam format JSON |

### Forward Commands

| Command | Deskripsi |
|---------|-----------|
| `vf forward list` | Lihat forwarding rules |
| `vf forward add` | Tambah forwarding rule |
| `vf forward edit` | Edit forwarding rule |
| `vf forward delete` | Hapus forwarding rule(s) |

### Batch Commands

| Command | Deskripsi |
|---------|-----------|
| `vf batch import` | Import rules dari JSON file |
| `vf batch export` | Export rules ke JSON file |


## Contoh

### Workflow: Setup Web Server Forwarding

```bash
# 1. Setup host
vf config add myserver \
  --url "https://virt.myserver.com:4083/index.php" \
  --key "abc123" \
  --pass "secret" \
  --default

# 2. Cek VM yang tersedia
vf vm list --status up

# 3. Tambah HTTP forwarding untuk website
vf forward add -v 103 -p HTTP -d mysite.com

# 4. Tambah HTTPS forwarding
vf forward add -v 103 -p HTTPS -d mysite.com

# 5. Tambah SSH access via custom port
vf forward add -v 103 -p TCP -d 45.158.126.xxx -s 2222 -t 22

# 6. Verifikasi
vf forward list -v 103
```

### Workflow: Backup dan Restore Rules

```bash
# Backup rules dari VM
vf batch export -v 103 -o vm103_backup.json

# Restore ke VM lain
vf batch import -v 104 -f vm103_backup.json --dry-run  # Test dulu
vf batch import -v 104 -f vm103_backup.json            # Execute
```

### Workflow: Multi-Host Management

```bash
# Setup multiple hosts
vf config add production --url "https://prod.com:4083/index.php" --key "key1" --pass "pass1" --default
vf config add staging --url "https://staging.com:4083/index.php" --key "key2" --pass "pass2"

# Lihat VM dari semua host
vf vm list --all-hosts

# Operasi di host tertentu
vf -H staging vm list
vf -H production forward list -v 103
```


## 🔧 Troubleshooting

### Connection Error

```
✗ Failed to connect to API
```

**Solusi:**
1. Pastikan URL API benar (termasuk port 4083)
2. Cek koneksi network ke server
3. Pastikan firewall tidak memblokir

### Authentication Error

```
✗ Authentication failed
```

**Solusi:**
1. Verifikasi API Key di Virtualizor Panel
2. Pastikan API Password benar
3. Cek apakah API access diaktifkan di panel

### Port Already Reserved

```
✗ Port 8080 is already reserved/in use
```

**Solusi:**
1. Gunakan port lain yang tersedia
2. Cek allowed ports di HAProxy config
3. Lihat suggestions yang ditampilkan

### No VMs Found

```
! No VMs found
```

**Solusi:**
1. Pastikan host profile benar
2. Cek apakah ada VM di panel Virtualizor
3. Verifikasi API credentials memiliki akses ke VM

### Debug Mode

Untuk melihat detail error:

```bash
vf --debug vm list
vf --debug forward add -i
```


## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/iam-rizz/python-domain-forwarding-virtualizor.git
cd python-domain-forwarding-virtualizor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install dengan dev dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=virtualizor_forwarding

# Run specific test
pytest tests/test_models.py -v
```

### Project Structure

```
python-domain-forwarding-virtualizor/
├── virtualizor_forwarding/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py              # CLI entry point
│   ├── api.py              # Virtualizor API client
│   ├── config.py           # Configuration manager
│   ├── models.py           # Data models
│   ├── tui.py              # Rich TUI components
│   ├── utils.py            # Utility functions
│   └── services/
│       ├── __init__.py
│       ├── vm_manager.py
│       ├── forwarding_manager.py
│       └── batch_processor.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── README.md
├── README_ID.md
├── LICENSE
└── .gitignore
```

## Kontribusi

Kontribusi sangat diterima! Silakan submit Pull Request.

1. Fork repository
2. Buat feature branch (`git checkout -b feature/FiturBaru`)
3. Commit perubahan (`git commit -m 'Tambah FiturBaru'`)
4. Push ke branch (`git push origin feature/FiturBaru`)
5. Buka Pull Request

## Lisensi

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## Author

**Rizz**

- Email: rizkyadhypratama@gmail.com
- GitHub: [@iam-rizz](https://github.com/iam-rizz)

---

<p align="center">
  Dibuat dengan ❤️ untuk pengguna Virtualizor
</p>
