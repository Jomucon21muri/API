# 🤖 INICIO RÁPIDO - Bot de Telegram

Guía de 5 minutos para crear tu bot de Telegram.

## Pasos rápidos

### 1️⃣ Crear el bot en Telegram (2 min)

1. Abre Telegram y busca: **@BotFather**
2. Envía: `/newbot`
3. Dale un nombre (ej: "API Financiera Reporter")
4. Dale un username que termine en "bot" (ej: "mi_api_financiera_bot")
5. **Guarda el token** que te da (ejemplo: `123456789:ABCdefGHI...`)

### 2️⃣ Configurar el bot (1 min)

```powershell
cd telegram_bot
Copy-Item .env.example .env
notepad .env
```

Pega tu token en el archivo `.env`:
```env
TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI
API_BASE_URL=http://localhost:5000/api
AUTHORIZED_USERS=
```

### 3️⃣ Instalar dependencias (1 min)

```powershell
pip install -r requirements.txt
```

### 4️⃣ Iniciar el bot (1 min)

**Primero, asegúrate de que tu API esté corriendo:**
```powershell
cd ..\api
python app.py
```

**En otra terminal, inicia el bot:**
```powershell
cd ..\telegram_bot
.\start_bot.ps1
```

O manualmente:
```powershell
python bot.py
```

### 5️⃣ Probar el bot (30 seg)

1. Abre Telegram
2. Busca tu bot por el username que creaste
3. Envía: `/start`
4. ¡Listo! Prueba `/reporte_diario`

## 🔐 Seguridad (Opcional)

Para restringir el bot solo a ti:

1. Habla con **@userinfobot** en Telegram para obtener tu ID
2. Edita `.env` y añade tu ID:
   ```env
   AUTHORIZED_USERS=123456789
   ```

## 📋 Comandos principales

- `/reporte_diario` - Transacciones del día
- `/listar_transacciones` - Últimas 10 transacciones
- `/estadisticas` - Resumen general
- `/buscar_transaccion ID` - Buscar por ID
- `/cliente ID` - Info de cliente

## ⚠️ Troubleshooting

**"Bot no responde"**
- Verifica que el token en `.env` sea correcto
- Asegúrate de que el script `bot.py` esté ejecutándose

**"Error al conectar con la API"**
- Verifica que la API esté corriendo: `python ../api/app.py`
- Confirma que `API_BASE_URL` en `.env` sea correcta

**"No estás autorizado"**
- Añade tu ID de Telegram a `AUTHORIZED_USERS` en `.env`

## 📚 Más información

- **Guía completa**: [docs/bot-telegram-paso-a-paso.md](../docs/bot-telegram-paso-a-paso.md)
- **README del bot**: [telegram_bot/README.md](README.md)

---

**¡Eso es todo! Tu bot está listo en 5 minutos.** 🎉
