# 🎉 ¡Tu bot está casi listo!

## ✅ Bot creado correctamente

- **Nombre**: API_PF_VIU_bot
- **Link**: https://t.me/API_PF_VIU_bot
- **Token**: Configurado en `.env`

---

## 🚀 Próximos pasos (2 minutos)

### 1️⃣ Configurar seguridad (RECOMENDADO)

Para que solo tú puedas usar el bot:

1. **Abre Telegram** y busca: `@userinfobot`
2. **Envía** `/start`
3. **Copia tu ID** (ejemplo: `123456789`)
4. **Edita el archivo** `.env` de esta carpeta
5. **Añade tu ID** en la línea `AUTHORIZED_USERS=`

```env
AUTHORIZED_USERS=123456789
```

> ⚠️ **Importante**: Si no haces esto, cualquier persona podrá usar tu bot.

### 2️⃣ Iniciar la API (si no está corriendo)

Abre una terminal PowerShell y ejecuta:

```powershell
cd "..\api"
python app.py
```

La API debe estar corriendo en `http://localhost:5000`

### 3️⃣ Iniciar el bot

En **otra terminal**, ejecuta:

```powershell
cd "telegram_bot"
.\test_bot.ps1
```

O directamente:

```powershell
.\start_bot.ps1
```

### 4️⃣ Probar el bot en Telegram

1. Abre Telegram
2. Busca: `@API_PF_VIU_bot` o ve a https://t.me/API_PF_VIU_bot
3. Presiona **INICIAR** o envía `/start`
4. Prueba comandos:
   - `/reporte_diario`
   - `/estadisticas`
   - `/listar_transacciones`

---

## 📋 Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar y ver menú |
| `/help` | Ayuda |
| `/reporte_diario` | Transacciones de hoy |
| `/reporte_semanal` | Últimos 7 días |
| `/reporte_mensual` | Mes actual |
| `/estadisticas` | Resumen general |
| `/listar_transacciones` | Últimas 10 transacciones |
| `/buscar_transaccion ID` | Buscar por ID |
| `/cliente ID` | Info de cliente |
| `/portfolio` | Reporte de portfolios |

---

## 🔧 Solución de problemas

### El bot no responde
✅ Verifica que el script `bot.py` esté ejecutándose sin errores  
✅ Revisa los logs en la consola PowerShell

### "No estás autorizado"
✅ Añade tu ID de Telegram en `.env` → `AUTHORIZED_USERS=`  
✅ Reinicia el bot después de editar `.env`

### Error de conexión a la API
✅ Asegúrate de que la API esté corriendo: `python ../api/app.py`  
✅ Verifica que `API_BASE_URL=http://localhost:5000/api` en `.env`

### No hay datos
✅ Ejecuta primero: `python ../api/init_db.py`  
✅ Luego: `python ../scripts/populate_db.py`

---

## 📂 Archivos importantes

- **`.env`** - Configuración del bot (TOKEN, usuarios autorizados)
- **`bot.py`** - Código del bot
- **`start_bot.ps1`** - Script de inicio automático
- **`test_bot.ps1`** - Script de prueba y configuración

---

## 🎯 Inicio rápido

### Opción más rápida:

```powershell
# Terminal 1 - API
cd "..\api"
python app.py

# Terminal 2 - Bot
cd "..\telegram_bot"
.\test_bot.ps1
```

---

**¡Listo!** Tu bot está configurado. Solo falta ejecutarlo y probarlo en Telegram. 🎉
