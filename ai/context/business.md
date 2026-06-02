# Contexto de negocio

## Qué es TLA

Tech Lead Assistant es una herramienta personal para tech leads que gestionan equipos pequeños (~6 personas). Centraliza la información de reuniones 1:1 y de seguimiento para:

- Llegar preparado a cada reunión con contexto histórico.
- Detectar patrones (temas recurrentes, blockers no resueltos, evolución del sentiment).
- Tener material objetivo para performance reviews trimestrales.
- Mantener trazabilidad de compromisos.

## Quién lo usa

Un único usuario: el tech lead. No es multi-usuario ni multi-tenant. Puede usarse desde varias máquinas si `data_root` está en red.

## Flujo de trabajo típico

1. El tech lead tiene una 1:1 con un miembro del equipo.
2. El dispositivo de grabación (Focusrec o similar) genera un fichero de transcripción en texto.
3. El tech lead sube la transcripción a la app.
4. Genera un report (internamente con LLM, o lo prepara externamente con IA y lo importa).
5. Antes de la siguiente 1:1, revisa el último report y el brief.
6. Periódicamente compara reports para performance reviews.
7. Periódicamente un agente externo genera estadísticas del equipo y las deposita para que la app las muestre.

## Datos sensibles

Las transcripciones y reports contienen información confidencial: feedback, preocupaciones, performance, sentiment. Los ficheros viven en plano (sin cifrado por la app) para permitir composability. La seguridad fuerte se delega al cifrado de disco del SO.

## Filosofía de diseño

La app no pretende ser la única interfaz sobre los datos. El filesystem es la fuente de verdad y cualquier herramienta puede operar sobre él. La app es el visualizador principal, pero Claude Code, scripts, editores de texto u otras herramientas son ciudadanos de primera clase.
