# 📸 Instagram Clone

Aplicación web tipo Instagram para compartir fotos, dar “me gusta”, comentar y gestionar perfiles de usuario.

🌐 **Proyecto en producción**: [instagram.pruebas-alberto.online](https://instagram.pruebas-alberto.online)
---

🧩 🧠 Backend (Servidor)
🔹 Lenguaje:
Python 3.10

🔹 Framework principal:
Django 5.1
(usando vistas basadas en clases como DetailView, formularios personalizados, AJAX, etc.)

🔹 Base de datos:
MySQL
Base de datos: mydb
Usuario: django_user_db
Modo SQL: STRICT_TRANS_TABLES

🔹 Características principales del backend:
- Sistema de usuarios y perfiles (UserProfile model)
- Vista de detalle del perfil: ProfileDetailView
- Seguir/Dejar de seguir usuarios con formulario FollowForm
- Publicaciones con likes manejados por AJAX (sin recargar la página)
- Comentarios dinámicos con modales y actualización mediante JavaScript
- Archivos multimedia (imágenes de usuario, publicaciones, etc.) guardados en media/
- Plantillas reutilizables (_posts.html, etc.)
- Configuración profesional del entorno (entorno virtual, requirements.txt, .env)

🎨 💻 Frontend (Interfaz)
🔹 Frameworks/Librerías:
Bootstrap 5 → para diseño responsive y moderno
JavaScript / AJAX → para manejar likes, comentarios y seguir usuarios sin recargar la página
HTML5 + CSS3 → estructuración y estilo de las vistas
Iconos (Font Awesome o Bootstrap Icons)

🔹 Plantillas Django (Jinja-like):
Uso de extends, include, block para heredar layouts.
Plantilla base general (layout.html o similar).
Componentes parciales (_posts.html, modales de comentarios, etc.)

🗂️ 📸 Gestión de archivos:
Carpeta media/ → para fotos de perfil, publicaciones, etc.
Carpeta static/ → para CSS, JS y recursos estáticos.
Configurado en settings.py con rutas MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT.

☁️ 🚀 Despliegue (Producción)
🔹 Servidor:
DigitalOcean (Droplet con Ubuntu)
CloudPanel (para gestionar dominios y sitios web)
Subdominio: instagram.pruebas-alberto.online

🔹 Servicios configurados:
Gunicorn → servidor WSGI de Django
Nginx → proxy reverso para servir la app y archivos estáticos
Certbot (SSL) → para HTTPS
Git → control de versiones y despliegue automático

🧰 📦 Herramientas adicionales
Entorno virtual (venv) para aislar dependencias.
Archivo requirements.txt con librerías necesarias (Django, Pillow, mysqlclient, etc.).
VS Code como entorno de desarrollo principal.
Git + GitHub para control de versiones.
PowerShell / CMD / Terminal VS Code para ejecución de comandos.

🔒 Seguridad y buenas prácticas
Manejo de variables sensibles mediante .env.
.gitignore configurado para no subir env/, db.sqlite3, __pycache__, etc.
Formularios Django con CSRF tokens para seguridad.
Políticas de ejecución ajustadas para PowerShell.

## 🚀 Cómo Usar

### 1. Clonar el repositorio  
```bash
git clone https://github.com/AlbertoContento/Instagram.git
cd Instagram
```
### 2. Instalar requerimientos
```bash
pip install -r requirements.txt
```
### 3. Migramos y Ejecutamos el servidor
```bash
python manage.py migrate
python manage.py createsuperuser     # crea admin
python manage.py runserver

```
## 📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta LICENSE para más detalles.

## 🎨 Capturas de Pantalla 
Aquí tienes una vista previa de cómo luce el proyecto:
![Pantalla Principal](https://github.com/AlbertoContento/Instagram/blob/main/assets/Captura%20de%20pantalla.png)
![Pantalla Principal](https://github.com/AlbertoContento/Instagram/blob/main/assets/Captura%20de%20pantalla1.png)
![Pantalla Principal](https://github.com/AlbertoContento/Instagram/blob/main/assets/Captura%20de%20pantalla2.png)
