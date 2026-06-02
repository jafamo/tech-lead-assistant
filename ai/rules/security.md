# Reglas: Seguridad

## Modelo de amenaza
La app NO protege los datos contra un atacante con acceso al filesystem. Los ficheros viven en plano por diseño (composability).

## Login
- Solo lock-screen de la UI. Sin cifrado de datos.
- Password hash con bcrypt (cost ≥ 12).
- Retardo exponencial tras intentos fallidos (1s, 2s, 4s...).
- Timeout de sesión por inactividad (configurable).

## API keys
- Solo en `.env`, nunca en la BD ni en logs.
- `.env` en `.gitignore`.
- Nunca loggear API keys ni contenido de respuestas LLM en nivel INFO+.

## Datos sensibles
- Las transcripciones y reports contienen información confidencial.
- La app recomienda FDE del SO en el primer arranque.
- Si se usa LLM cloud, modal de confirmación antes de la primera llamada.

## Escrituras
- Siempre atómicas (write-temp + rename) para evitar corrupción.
- Sin locking entre procesos (documentado).

## Dependencias
- Mantener actualizadas. Usar `pip-audit` o `safety` periódicamente.
- No instalar dependencias innecesarias.
