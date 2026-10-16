# greences (base de datos nueva en pgAdmin)

primero se creó el entorno virtual y se instalaron las librerías necesarias
luego pip install -r requirements.txt
copy .env.example .env
se copio la misma estructura del backend hecho en clase: app, routes, controllers, services, models, extensions, config y se edito
modelo nuevo:Reading,rutas nuevas: devices y readings
python -c "import secrets; print(secrets.token_hex(32))" ----> para crear un nueva clave secreta esa la pego en 
en el URL postgresql+pg8000://postgres:miclave@localhost:5432/greences  ---> psycog no pq no se Windows me bloqueaba y claude me dio esa solucion

y luego
flask --app run db init
flask --app run db migrate -m "create users and readings"
flask --app run db upgrade --->aquí se crean las tablas y se verificó en pgAdmin 

luego
python run.py

recorrido de un dato: ESP32 ---> POST /devices/insert --> devices_routes --> devices_controller(valida) --> readings_service(guarda) --> tabla readings 

routes es el mesero: recibe el pedido y dice a quién le toca.
controllers es el jefe de sala: revisa que el pedido venga bien armado (validar) y responde.
services es el cocinero: hace el trabajo real y habla con la base de datos.
models es la receta: cómo es cada tabla.

ESP32 → POST /devices/insert → route → controller (valida) → service (guarda) → tabla readings.


¿Por qué /devices/insert no tiene token? Porque el examen lo exige (Nota 4) y el ESP32 no tiene un flujo de login. Las rutas que muestran información sí están protegidas.

¿Cómo funciona el login con token? El usuario manda email y clave. El service busca el usuario y compara el hash. Si coincide, se firma un JWT con la clave secreta. El frontend lo manda en el header Authorization: Bearer, y @jwt_required() lo verifica.

¿Por qué hash y no la contraseña? Si se filtra la BD, nadie ve las claves reales. El hash no se puede revertir y lleva sal.

¿Para qué las capas? Cada archivo tiene una sola responsabilidad. Se puede cambiar la BD sin tocar las rutas, y es más fácil encontrar errores.

¿Qué es una migración? Un script versionado que crea o modifica las tablas a partir de los modelos, para no hacerlo a mano en pgAdmin.

¿Cómo calculan máximos y mínimos? Con funciones de agregación SQL (MAX y MIN) en una consulta, no en Python.

¿Cómo sabe el backend que el sistema está apagado? Si la última lectura tiene más de 30 s, devuelve estado OFF con ceros.

¿Por qué la fecha la pone el servidor? Porque el ESP32 no tiene un reloj confiable, y así todas las fechas son consistentes.

¿Qué es CORS? Un permiso del navegador. Como el frontend está en otro origen (puerto o equipo), el servidor debe autorizar esas llamadas.

«El ESP32 captura y envía las variables del sistema, el backend recibe y procesa la información, y PostgreSQL almacena las lecturas. Después, el frontend consulta el backend para mostrar los datos guardados. Por eso puedo visualizar registros anteriores sin tener el ESP32 conectado; lo que no puedo recibir sin él son nuevas lecturas del dispositivo».