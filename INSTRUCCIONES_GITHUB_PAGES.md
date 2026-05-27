# 🚀 Instrucciones para Activar GitHub Pages

## ✅ Archivos Creados

He creado los siguientes archivos para tu dashboard:

- ✅ **index.html** - Página principal del dashboard
- ✅ **style.css** - Estilos modernos y responsive
- ✅ **script.js** - Chatbot y funcionalidades interactivas
- ✅ **404.html** - Página de error personalizada
- ✅ **.nojekyll** - Optimización para GitHub Pages
- ✅ **_config.yml** - Configuración de GitHub Pages
- ✅ **README.md** - Documentación actualizada

## 🌐 Activar GitHub Pages (2 minutos)

### Paso 1: Ir a la configuración
1. Abre tu repositorio en GitHub: https://github.com/Jomucon21muri/API
2. Haz clic en **Settings** (⚙️ Configuración)

### Paso 2: Configurar Pages
1. En el menú lateral izquierdo, busca y haz clic en **Pages**
2. En la sección **Source** (Fuente):
   - **Branch**: Selecciona `main`
   - **Folder**: Selecciona `/ (root)`
3. Haz clic en **Save** (Guardar)

### Paso 3: Esperar el despliegue
- GitHub Pages tardará unos 2-5 minutos en procesar y publicar tu sitio
- Verás un mensaje verde cuando esté listo
- Tu sitio estará disponible en: **https://jomucon21muri.github.io/API/**

## 🎨 Personalizar tu Dashboard

### Cambiar la URL de tu web principal

En [index.html](index.html), busca y reemplaza todas las instancias de:
```html
https://tuempresa.com
```

Por la URL de tu sitio web real.

### Cambiar el nombre del proyecto

En [index.html](index.html), línea 6:
```html
<title>Dashboard - Tu Nombre Aquí</title>
```

Y en la línea 14:
```html
<span>Tu Nombre Aquí</span>
```

### Cambiar los colores

En [style.css](style.css), líneas 12-18, modifica:
```css
:root {
    --primary-color: #6366f1;  /* Cambia este color */
    --secondary-color: #8b5cf6; /* Cambia este color */
}
```

### Personalizar las respuestas del chatbot

En [script.js](script.js), líneas 45-60, modifica el objeto `botResponses`:
```javascript
const botResponses = {
    'hola': '¡Hola! ¿Cómo puedo ayudarte?',
    'ayuda': 'Tu mensaje personalizado...',
    // Añade más respuestas...
};
```

## 🤖 Funcionalidades del Chatbot

El chatbot ya responde a:
- ✅ Saludos (hola, buenos días)
- ✅ Ayuda
- ✅ Información sobre servicios
- ✅ Preguntas sobre la API
- ✅ Contacto
- ✅ Precios
- ✅ Soporte
- ✅ Y más...

## 📱 Características

✅ **Totalmente Responsive**
- Se adapta a móviles, tablets y desktop
- Menú hamburguesa en móvil

✅ **Chatbot Flotante**
- Botón flotante siempre visible
- Notificaciones
- Respuestas automáticas

✅ **Estadísticas en Tiempo Real**
- Se actualizan automáticamente
- Animaciones suaves

✅ **Navegación Suave**
- Scroll suave entre secciones
- Resaltado de sección activa

✅ **Enlace a Web Principal**
- Botón destacado en navbar
- Botón en sección hero
- Enlaces en footer

## 🔄 Hacer Cambios

Después de modificar cualquier archivo:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

GitHub Pages actualizará automáticamente en 1-2 minutos.

## 🆘 Solución de Problemas

### El sitio no carga
- Espera 5 minutos después de activar GitHub Pages
- Verifica que la rama sea `main` y la carpeta `/ (root)`
- Limpia la caché del navegador (Ctrl+F5)

### Los estilos no se aplican
- Verifica que `style.css` esté en la raíz del proyecto
- Revisa la consola del navegador (F12) por errores

### El chatbot no funciona
- Verifica que `script.js` esté en la raíz del proyecto
- Abre la consola del navegador (F12) para ver errores

## 📞 Contacto y Soporte

Si necesitas ayuda adicional, puedes:
1. Revisar el [README.md](README.md) completo
2. Abrir un Issue en GitHub
3. Contactarme directamente

---

**¡Tu dashboard está listo para desplegarse! 🎉**

URL final: **https://jomucon21muri.github.io/API/**
