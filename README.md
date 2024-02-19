# README

Ejercicio de implementación de API para postulación de Ingeniero de Integraciones en Cero.ai.

## Requisitos

La implementación del cliente intermedio entre el bot de Cero.ai y la API de Dentalink requiere:
* Python >= 3.11
* Las dependencias que se encuentran en el archivo requirements.txt y que pueden ser instaladas automáticamente usando
>pip install -r requirements.txt

* Un token para acceder a la API de Dentalink que debe ser definida en un archivo llamado dentalinktoken.py que contenga la siguiente linea de código:
>DENTALINK_TOKEN = "pegar-token-aquí"
## Cómo usarla

Para utilizar el cliente se puede llamar el siguiente comando desde la terminal estando dentro de la carpeta que contiene el proyecto:
```python client.py```

Primero se llevará a cabo una rutina de testing para ver que funcione correctamente. Luego de esto se abrirá el cliente en la dirección
```http://127.0.0.1:8000/```
Como se trata de un cliente intermediario, este no presenta un index o homepage. Solamente tiene los endpoints requeridos que son:
* ```http://127.0.0.1:8000/appointments```
* ```http://127.0.0.1:8000/appintments/{appointment_id}```

También es posible ver la documentación general generada por SwaggerUI en ```http://127.0.0.1:8000/docs```
