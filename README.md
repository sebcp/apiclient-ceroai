## Ejercicio de implementación de API para postulación de Ingeniero de Integraciones en Cero.ai

El ejercicio consta en implementar una API intermediaria entre el chatbot de Cero.ai con la API de Dentalink. Esta API debe ser capaz de traer los datos de las citas de Dentalink, filtrando por un rango de fechas, el estado en el que se encuentra la cita y la sucursal en la que está agendada. Además también deberá poder modificar el estado de una cita dada.

### Sobre la API

La API fue implementada en Python 3.11.6, usando principalmente las librerías FastAPI, pytest y requests.

### Consideraciones

Para la implementación se tomaron las siguientes consideraciones
* Se asume que se puede filtrar por todos, algunos o ninguno de los tres parámetros permitidos.
* Se asume que los posibles estados y las posibles sucursales de una cita solo pueden ser extraídos manualmente scrappeando la API a través del endpoint de cada atributo respectivamente. Esta solución puede no escalar bien con números muy altos de citas y usuarios concurrentes a la API. Es importante mencionar que no es posible filtrar desde el endpoint de citas por la sucursal, solo se pueden conseguir todas las citas de una sucursal y sobre eso filtrar por un rango de fechas y el estado. Debido a esto, para poder optimizarlo habría que modificar la API de Dentalink para que se puedan filtrar las citas por sucursal, habría que establecer un sistema de comunicación por mensajes con la API de Dentalink o habría que mantener una copia actualizada de la BBDD de la API de Dentalink para poder realizar cruces en el cliente.
* Se asume que, dado que la API es un intermediario entre solo dos puntos, solo realiza un reenvío de información y no debe preocuparse de mantener un sistema de mensajes.
* Aunque se realiza la verificación, se asume que los datos que provienen desde el bot deben venir en el mismo formato que el que utiliza la API de Dentalink. Es decir que las fechas son strings en formato 'YYYY-MM-DD' y los estados y las sucursales son enteros.
* Se asume que todas las queries SQL que realiza la API de Dentalink son hechas utilizando consultas preparadas o escapando el input del usuario. Se asume que no habrán ataques XSS y no es necesario revisar la existencia de código en JavaScript en el input del usuario.

### Requisitos

La implementación del cliente intermedio entre el bot de Cero.ai y la API de Dentalink requiere:
* Python >= 3.11
* Las dependencias que se encuentran en el archivo requirements.txt y que pueden ser instaladas automáticamente usando
>pip install -r requirements.txt

* Un token para acceder a la API de Dentalink que debe ser definida en un archivo llamado dentalinktoken.py que contenga la siguiente linea de código:
>DENTALINK_TOKEN = "pegar-token-aquí"
### Cómo usarla

Para utilizar el cliente se puede llamar el siguiente comando desde la terminal estando dentro de la carpeta que contiene el proyecto:
```python client.py```

Primero se llevará a cabo una rutina de testing para ver que funcione correctamente. Luego de esto se abrirá el cliente en la dirección
```http://127.0.0.1:8000/```
Como se trata de un cliente intermediario, este no presenta un index o homepage. Solamente tiene los endpoints requeridos que son:
* ```http://127.0.0.1:8000/appointments```
* ```http://127.0.0.1:8000/appintments/{appointment_id}```

También es posible ver la documentación general generada por SwaggerUI en ```http://127.0.0.1:8000/docs```
