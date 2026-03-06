# 📋 Guía de Release para FreeLauncher

Esta guía explica cómo crear una nueva versión y hacer un release.

## 📝 Pasos para hacer un Release

### 1. Preparar el código
```bash
# Asegurate que todo funciona
make test
make lint

# Actualizar versión en src/utils/config.py
# Cambiar: APP_VERSION = "X.X.X"
```

### 2. Actualizar documentación
- Actualizar `README.md` con cambios
- Actualizar `CHANGELOG.md` si existe
- Commit los cambios:
```bash
git add .
git commit -m "Release v1.2.3"
```

### 3. Crear el tag
```bash
# Tag semántico
git tag -a v1.2.3 -m "Release version 1.2.3"

# Push al repositorio
git push origin v1.2.3
```

### 4. GitHub Actions automáticamente:
- ✅ Ejecuta tests
- ✅ Ejecuta linting
- ✅ Crea distribuciones (wheel, source)
- ✅ Construye imagen Docker
- ✅ Crea release en GitHub con todos los archivos

### 5. Verificar Release
- Ve a: https://github.com/marquistallman/OpenLauncherProyect/releases
- Descarga los archivos
- Prueba que los instaladores funcionan

---

## 🔨 Build Local

Si quieres hacer un build local sin crear un release:

```bash
# Build completo (tests + linting + compilación)
make release

# Solo compilación
make build

# Docker
make docker

# Limpiar todo
make clean-all
```

---

## 📦 Distribución en PyPI

Para distribuir en PyPI (opcional):

### 1. Crear cuenta en PyPI
- Ve a: https://pypi.org/account/register/
- Verifica tu email

### 2. Crear `.pypirc` (en tu home)
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

### 3. Upload
```bash
make build
python -m twine upload dist/*
```

---

## 🐳 Push a Docker Registry

### DockerHub
```bash
docker login
docker tag freelauncher:latest [USERNAME]/freelauncher:1.2.3
docker tag freelauncher:latest [USERNAME]/freelauncher:latest
docker push [USERNAME]/freelauncher:1.2.3
docker push [USERNAME]/freelauncher:latest
```

### GitHub Container Registry
```bash
docker login ghcr.io
docker tag freelauncher:latest ghcr.io/[USERNAME]/freelauncher:1.2.3
docker push ghcr.io/[USERNAME]/freelauncher:1.2.3
```

---

## 🔄 Versioning

Usa [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH**
  - MAJOR: Breaking changes
  - MINOR: Features (backwards compatible)
  - PATCH: Bug fixes

Ejemplos:
- `v1.0.0` - Initial release
- `v1.1.0` - New feature
- `v1.1.1` - Bug fix
- `v2.0.0` - Major rewrite

---

## 📊 Progress

Checklist para cada release:

- [ ] Código finalizado y probado
- [ ] Tests pasando
- [ ] Linting pasando
- [ ] Documentación actualizada
- [ ] Versión actualizada en `config.py`
- [ ] Cambios committeados
- [ ] Tag creado: `git tag v...`
- [ ] Tag pusheado: `git push origin v...`
- [ ] GitHub Actions completó
- [ ] Release visible en GitHub
- [ ] Descargables funcionan
- [ ] Instaladores probados

---

## 🐛 Rollback

Si necesitas revertir un release:

```bash
# Eliminar tag local
git tag -d v1.2.3

# Eliminar tag remoto
git push origin --delete v1.2.3

# Eliminar release en GitHub
# Manualmente en la web
```

---

## 📞 Soporte

¿Problemas con el release? Abre un issue en GitHub.
