## Laboratorio: ETL de ventas con Airflow, pruebas y CI

## TODAS LAS EVIDENCIAS DE LA EJECUCION DEL LABORATORIO, INCLUIDO CORRIDAS DEL DAG Y LA INTEGRACION CONTINUA SE ENCUENTRAN EN EL ARCHIVO DEL REPOSITORIO "Taller Modulo 6 y 7.xls"

Taller Modulo 6 y 7.xlsx  -- https://github.com/lulebebe/etl-ventas-airflow/blob/51b587c4c745f0a2284e870ef61735542b00d5f9/Taller%20Modulo%206%20y%207.xlsx  -- Se pueden visualizar o descargar

Una cadena de tiendas de tecnología tiene locales en tres regiones: norte, sur y centro. Cada noche, el
sistema de caja deja un archivo CSV con las ventas del día en una carpeta compartida. el proceso a optimizar 
abre manualmente esos archivos en Excel, los limpia y pega los totales en un reporte. No se conoce qué filas se
descartan ni por qué.

#### CREAR REPOSITORIO Y CARGAR EL LABORATORIO

##### Crear carpeta de respaldo

<img width="700" height="270" alt="image" src="https://github.com/user-attachments/assets/e986c30d-a5bf-4a4c-8568-bf39bde05e80" />

#### Copiar laboratorio en carpeta de respaldo

<img width="700" height="79" alt="image" src="https://github.com/user-attachments/assets/e5a74a97-0113-46b2-b097-66e97149288c" />

#### Crear repositorio en GITHUB

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/ead4149b-c331-463f-ade6-9352828e4bf4" />

#### Cargar laboratorio  en el repositorio: git init, git branch, git add y git commit

<img width="700" height="99" alt="image" src="https://github.com/user-attachments/assets/53555411-9a1f-49f2-9563-8a73c9417dab" />

<img width="700" height="45" alt="image" src="https://github.com/user-attachments/assets/74b5f76a-407e-4d12-ac16-87900eee8551" />


#### copiar  en repositorio creado

<img width="700" height="42" alt="image" src="https://github.com/user-attachments/assets/a55b74eb-3d89-4de4-8abf-b257e4e1fa0e" />

#### git push

<img width="700" height="299" alt="image" src="https://github.com/user-attachments/assets/c4d2a53e-2909-44bc-868b-ababad273a01" />

#### Laboratorio cargado

<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/f69fd76d-bd32-489f-85c8-5d37bbae2cd2" />


### LEVANTAR AIRFLOW

#### Ejecutar el archivo preparar entorno

<img width="700" height="58" alt="image" src="https://github.com/user-attachments/assets/330c70f2-082f-4289-a4cf-437772d1c353" />

#### revisar archivo .env

<img width="700" height="255" alt="image" src="https://github.com/user-attachments/assets/0106d399-46c1-4acc-81b9-ad4457e10e68" />


#### revisar archivo dockerfile

<img width="700" height="331" alt="image" src="https://github.com/user-attachments/assets/06ad9120-4748-4472-893a-a7810dc47e23" />


#### revisar archivo dockerignore

<img width="700" height="331" alt="image" src="https://github.com/user-attachments/assets/0b7136fd-c388-4c4d-be71-7e514f80a16c" />


#### revisar archivo gitignore

<img width="415" height="360" alt="image" src="https://github.com/user-attachments/assets/0be747e5-b7f0-48d2-9fcb-8fa26c79445b" />


#### docker compose build

<img width="700" height="489" alt="image" src="https://github.com/user-attachments/assets/c0484ebe-1607-412e-be8f-1e639041a3ad" />


#### docker compose up airflow-init

<img width="700" height="271" alt="image" src="https://github.com/user-attachments/assets/2557ad1e-5eaf-4267-a8dd-28e105baed79" />


#### docker compose up -d --wait

<img width="700" height="236" alt="image" src="https://github.com/user-attachments/assets/21d787e0-c77d-4599-8f73-58963b8c4e01" />


#### Actualizcion del repositorio  GITHUB

<img width="700" height="470" alt="image" src="https://github.com/user-attachments/assets/c3e97d53-0159-4a9d-90cf-ca007fbf5a68" />

<img width="700" height="61" alt="image" src="https://github.com/user-attachments/assets/d28f3020-525c-46fd-9778-c93fdbfe7ba3" />


#### se abre el local host 

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/86d4b5e6-e15a-49f9-866e-202ecc49da0e" />


#### carga inicial de airflow

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/e154c4fa-9b19-40f8-b262-9daeecbcac70" />


#### dag etl_ventas_diarias

<img width="700" height="652" alt="image" src="https://github.com/user-attachments/assets/5f057e40-8621-47d1-80af-82a493e728fc" />


### VALIDACION Y PRUEBAS UNITARIAS

#### ejecutar pytest general, se presentan fallos

<img width="700" height="695" alt="image" src="https://github.com/user-attachments/assets/a261cc22-0380-4ac4-a073-d55553229e6e" />

<img width="700" height="913" alt="image" src="https://github.com/user-attachments/assets/debaa162-e794-4f22-bda2-50efd6762c42" />

<img width="700" height="878" alt="image" src="https://github.com/user-attachments/assets/b70bd932-4c34-4e4a-89d5-65abdc541f95" />

<img width="700" height="825" alt="image" src="https://github.com/user-attachments/assets/f649a6a8-e7cd-4679-8291-abe403dca8f8" />

<img width="700" height="740" alt="image" src="https://github.com/user-attachments/assets/245c682e-ef06-4693-ad50-9feb6f9379ee" />


#### Se presentan fallas con el DAG
FAILED tests/test_integridad_dag.py::test_validar_calidad_no_reintenta - assert 1 == 0
FAILED tests/test_reglas.py::test_fila_valida_calcula_el_total - NotImplementedError: Completa validar_fila
FAILED tests/test_reglas.py::test_region_desconocida_se_rechaza - NotImplementedError: Completa validar_fila
FAILED tests/test_reglas.py::test_duplicado_conserva_la_primera_aparicion - NotImplementedError: Completa separar_ventas
FAILED tests/test_reglas.py::test_calidad_rechaza_sobre_el_umbral - NotImplementedError: Completa revisar_calidad

#### se completa codigo para validar_fila , separar_ventas y revisar_calidad en dags/ventas/reglas.py


#### De nuevo se ejecuta el pytest, se presenta un error en validar calidad, las demas fallas  ya no existen

<img width="700" height="754" alt="image" src="https://github.com/user-attachments/assets/e195c586-6c6e-4b76-b188-12ac1da37e5d" />


#### se actualiza test_reglas.py, se ejecuta nuevamente pytest para test_reglas.py, ya no hay fallas con el pytest

<img width="700" height="308" alt="image" src="https://github.com/user-attachments/assets/6f1097d2-de62-4d25-b330-c341ac0771cf" />


#### se revisa y actualiza docker compose para PYTHONPATH

<img width="632" height="342" alt="image" src="https://github.com/user-attachments/assets/20030c9a-2de2-458a-9fba-d95bf16248d5" />


#### se recrea el docker compose

<img width="700" height="242" alt="image" src="https://github.com/user-attachments/assets/4ff7d88d-437f-4106-aa09-5f289d3f9bbe" />


#### se actualiza  el modulo etl_ventas_diarias.py

<img width="710" height="720" alt="image" src="https://github.com/user-attachments/assets/d625a940-316f-4848-b316-f6fd0c7ae7d8" />



#### Se ejecuta el pytest sobre test_integridad, ya no hay fallas

<img width="700" height="403" alt="image" src="https://github.com/user-attachments/assets/8a5a98a5-766b-4314-8a6a-33f97a997cb5" />



#### Con todos los cambios que se han hecho se actualiza el repositorio de GITHUB

<img width="700" height="199" alt="image" src="https://github.com/user-attachments/assets/a8aba6f9-2b11-4b5a-a068-7e4bff6586f1" />

<img width="700" height="140" alt="image" src="https://github.com/user-attachments/assets/344e063b-68b6-4f71-8132-f95581359106" />

<img width="700" height="92" alt="image" src="https://github.com/user-attachments/assets/f3417ff2-99e6-467d-9e63-aaf47ec216ac" />

<img width="700" height="282" alt="image" src="https://github.com/user-attachments/assets/fb52ef51-aa33-4cff-8451-853350f280c3" />


### EJECUCION DE LOS DAG

#### Visualizacion del DAG y sus cinco tareas

<img width="700" height="545" alt="image" src="https://github.com/user-attachments/assets/4f1e8679-b069-40da-b4e0-b0244f9cd902" />


#### se ejecuta el primer dag con el archivo del 5 de octubre, la ejecuciones exitosa

<img width="700" height="865" alt="image" src="https://github.com/user-attachments/assets/0f3dfb51-7073-48c9-bba0-9fe4f3ef5ddb" />


#### por defecto el trigger es con el archivo del 5 de octubre

<img width="700" height="444" alt="image" src="https://github.com/user-attachments/assets/87654e2d-b556-4bbe-ad4d-5666a82ea153" />

#### visualizacion grafica de la ejecucion

<img width="700" height="216" alt="image" src="https://github.com/user-attachments/assets/0cfda4c8-fe7a-497f-bc8b-1566e7ebf73e" />


#### segunda ejecucion, 6 de octubre, satisfactoria la ejecucion

<img width="700" height="660" alt="image" src="https://github.com/user-attachments/assets/4747c0f7-ee23-4572-a8a4-8ece1dd10c53" />


#### log de las dos ejecuciones, actualizar resumen

<img width="700" height="214" alt="image" src="https://github.com/user-attachments/assets/d1e01c17-8b73-4551-a3c9-0806adbde41a" />

<img width="700" height="232" alt="image" src="https://github.com/user-attachments/assets/d1371ec2-705e-49c5-8c11-ddb003638fb0" />


#### log de las tareas cargar para las dos ejecuciones


<img width="700" height="200" alt="image" src="https://github.com/user-attachments/assets/1af908ec-5375-4233-a0e7-4b1e1473ba4b" />

<img width="700" height="181" alt="image" src="https://github.com/user-attachments/assets/6c50155e-0318-43b5-8731-175705174b0f" />


#### ejecuciones que terminaron satisfactoriamente

<img width="700" height="180" alt="image" src="https://github.com/user-attachments/assets/e20004ce-9504-4c78-aff4-980665083a72" />

<img width="700" height="180" alt="image" src="https://github.com/user-attachments/assets/027b27ec-00f7-434b-8976-982ca4b95967" />


#### el dag del 7 de octubre falla en validar calidad


<img width="700" height="724" alt="image" src="https://github.com/user-attachments/assets/7b5e3ac9-3d05-4552-a756-32f38aba85f7" />


#### log  de la tarea valida calidad, se rechaza el 58,5% de las filas, el maximo es 20%


<img width="700" height="424" alt="image" src="https://github.com/user-attachments/assets/c600a89f-38cb-4790-bedd-84895435d24f" />

#### la mayoria de los rechazos  es por precio invalido

<img width="700" height="655" alt="image" src="https://github.com/user-attachments/assets/5cbe5655-b9c6-44c4-b74a-af4607880e16" />


#### visualizacion grafica de la ejecucion fallida


<img width="700" height="165" alt="image" src="https://github.com/user-attachments/assets/56386705-194c-4b45-9349-5ab1ef4cc9a7" />


#### se actualiza el archivo csv del 7 de octubre

<img width="700" height="720" alt="image" src="https://github.com/user-attachments/assets/9effb5d3-46d7-45a4-958c-46538b2b01c7" />


#### ejecucion satisfactoria

<img width="700" height="158" alt="image" src="https://github.com/user-attachments/assets/b7bf808e-53ef-43d9-ae69-f209b1c87644" />


#### log de las tareas  actualizar resumen, transformar  y cargar del archivo del 7 de octubre


<img width="700" height="173" alt="image" src="https://github.com/user-attachments/assets/ea6454e1-7762-45a3-bb6d-b356e9aac9f3" />

<img width="700" height="114" alt="image" src="https://github.com/user-attachments/assets/bfd0e14c-1c2c-44ce-b8b3-9c21c0c2467f" />


<img width="700" height="202" alt="image" src="https://github.com/user-attachments/assets/0f1d477d-2f57-4e5f-a709-19c5b9400dea" />


#### verificacion sql de las tres ejecuciones  satisfactorias


<img width="700" height="836" alt="image" src="https://github.com/user-attachments/assets/5659d79d-139f-4445-bcfc-2c4379e289b7" />


#### se ejecuta nuevamente  el archivo del 5 de octubre


<img width="700" height="566" alt="image" src="https://github.com/user-attachments/assets/b0977440-5252-4055-8051-f4178e2714e6" />


#### la ejecucion es satisfactoria

<img width="700" height="736" alt="image" src="https://github.com/user-attachments/assets/7cd5dc15-3edb-42fd-a2be-fa017b82ed00" />

#### sin embargo en la base de datos  no se alteran los resultados por la doble ejecucion

<img width="700" height="852" alt="image" src="https://github.com/user-attachments/assets/a71b0f6f-5237-4eaa-a28d-a82d8440c08f" />


### INTEGRACION CONTINUA

#### Se actualiza previamente el archivo ci.yml de github, se actualiza el repositorio de GITHUB
#### Este YAML valida el código y ejecuta las pruebas automatizadas. No vuelve a procesar los tres CSV ni levanta PostgreSQL para ejecutar sql/verificacion.sql.

<img width="700" height="880" alt="image" src="https://github.com/user-attachments/assets/c2846b66-5255-4ec6-850b-0651d8aae15b" />


#### Se crea otra rama de GITHUB, feature/precio-cero

<img width="700" height="379" alt="image" src="https://github.com/user-attachments/assets/0650c75e-1a63-4161-9b24-deef476023f8" />

#### despues de actualizar reglas.py para que aceptara valores en cero, se actuaiza la version en la nueva rama


<img width="700" height="601" alt="image" src="https://github.com/user-attachments/assets/8bc6a8e3-cb3e-4e74-944e-17a79540933e" />

#### en GITHUB se compara y se realiza el pull request

<img width="700" height="192" alt="image" src="https://github.com/user-attachments/assets/1780aec1-883b-48df-8014-64dc1a074ffb" />


#### se abre la solicitud y se activa el pull


<img width="700" height="846" alt="image" src="https://github.com/user-attachments/assets/827241e6-7320-47cf-a503-9a7406dc2da1" />


#### El CI falla en ejecutar pruebas automatizadas

<img width="700" height="640" alt="image" src="https://github.com/user-attachments/assets/2b37f271-b42c-428c-93ec-c5a022007192" />


#### se visualiza  el CI fallido

<img width="700" height="659" alt="image" src="https://github.com/user-attachments/assets/0bbce578-b276-486a-b81c-867defb559c7" />

#### se revierte el cambio en GITHUB

<img width="700" height="590" alt="image" src="https://github.com/user-attachments/assets/e544049c-3926-4e8f-a55d-8b5b65f93c58" />


#### la nueva ejecucion de CI es satisfactoria

<img width="700" height="1014" alt="image" src="https://github.com/user-attachments/assets/72085087-2b8f-44f8-8ce6-12e667c17407" />

#### visualizacion de la ejecucion satisfactoria del CI

<img width="700" height="433" alt="image" src="https://github.com/user-attachments/assets/793cacf0-4983-4d49-84c2-9579231bfe71" />


#### se busca en GITHUB la solicitud de pull para hacer el merge


<img width="700" height="567" alt="image" src="https://github.com/user-attachments/assets/911b437d-ab83-4de0-9ae3-3c4d0373fb77" />


#### se realiza el merge

<img width="700" height="998" alt="image" src="https://github.com/user-attachments/assets/f94fc8b4-57fe-4ac4-a2a2-363d8436b023" />

#### confirmacion del revert, pull request fusionada sobre la rama principal

<img width="700" height="618" alt="image" src="https://github.com/user-attachments/assets/268ccf35-fb47-4dd1-92e1-aae5ba6ab15d" />


## Respuestas

1. ¿Por qué falló la corrida del 7 de octubre? ¿Qué habría quedado en la base si no existiera
validar_calidad ?

La corrida del 7 de octubre falla dado que el nivel de rechazos  fue superior al 20%, llegando aun 58,5%.  Según log la de la tarea transformar la mayoría de los errores era por precio invalido en el archivo  CSV de entrada. 


<img width="700" height="424" alt="image" src="https://github.com/user-attachments/assets/ec07c7e6-1755-4e01-9d2b-1a56ef0654c8" />

<img width="700" height="655" alt="image" src="https://github.com/user-attachments/assets/8394da18-d454-4823-8a2f-a74c57518319" />


2. ¿Qué hace que repetir una fecha no duplique ventas? ¿Qué pasaría si cargar solo hiciera INSERT ?

Repetir el procesamiento del 5 de octubre no duplicó las ventas porque la tarea cargar está diseñada para ser idempotente: procesar varias veces la misma fecha produce el mismo resultado en las tablas, siempre que el archivo de entrada no cambie y la ejecución termine correctamente.

La clave está en estas instrucciones SQL de la tarea cargar de tu DAG etl_ventas_diarias.py
DELETE FROM ventas_limpias
WHERE fecha = %s;
DELETE FROM ventas_rechazadas
WHERE fecha_archivo = %s;

Además, la eliminación y las inserciones se realizan dentro de una única transacción. Si ocurre un error durante la carga, PostgreSQL puede revertir las operaciones y conservar los datos anteriores, en lugar de dejar la fecha parcialmente cargada.

Si se elimina DELETE y se conserva únicamente las inserciones, el resultado dependería de las restricciones de la tabla.
En ventas_limpias se tiene:
id_venta INTEGER PRIMARY KEY

La transacción fallaría y se revertiría la carga. Esto evita duplicar filas con el mismo identificador, pero no es una solución de idempotencia suficiente: la ejecución repetida terminaría con error en vez de completar correctamente.

En ventas_rechazadas si se vuelve a insertar rechazos de la misma fecha y línea, también se provoca una violación de clave primaria. Si cambian las líneas o sus claves, podrían aparecer registros duplicados lógicos.

3. ¿Por qué las pruebas del CI pueden correr sin PostgreSQL ni el scheduler? Nombra una cosa que
esas pruebas no comprueban.

Las pruebas del CI pueden ejecutarse sin PostgreSQL ni el scheduler de Airflow porque prueban principalmente la lógica del código y la estructura del DAG, sin ejecutar el ETL completo.

En el laboratorio:
- tests/test_reglas.py prueba las funciones de limpieza y validación de dags/ventas/reglas.py usando pytest.
- tests/test_integridad_dag.py comprueba que el DAG se cargue sin errores, que no tenga ciclos y que las tareas y sus dependencias estén correctamente configuradas.
  
Estas pruebas no necesitan una base de datos ni un scheduler en ejecución, pueden importar los módulos y verificar su comportamiento directamente.

Una cosa que no comprueban: que la carga real de ventas funcione correctamente contra PostgreSQL, incluyendo las transacciones, las inserciones y las restricciones de la base de datos. Para eso se necesitaria pruebas de integración con una instancia de PostgreSQL.

4. ¿Por qué tiene sentido que validar_calidad no reintente y que extraer sí?

Tiene sentido porque extraer puede fallar por problemas temporales, mientras que validar_calidad puede fallar por problemas en los datos que no se solucionan repitiendo la tarea.
- extraer sí reintenta: si ocurre un error temporal al leer el CSV, puede tener sentido intentarlo nuevamente. Por ejemplo, un archivo podría estar temporalmente inaccesible.
- validar_calidad no reintenta: si la tasa de rechazo supera el 20 %, volver a ejecutar la misma validación con los mismos datos normalmente producirá el mismo resultado. Es preferible corregir el archivo o las reglas antes de intentarlo otra vez.

## Pull request

Estas evidencias están en el archivo del repositorio: "Taller modulo 6 y 7.xls", que se puede visualizar y descargar
También estas evidencias están en este README, en una sección previa a esta. 
De todas formas se vuelven a presentar:

### INTEGRACION CONTINUA

#### Se actualiza previamente el archivo ci.yml de github, se actualiza el repositorio de GITHUB
#### Este YAML valida el código y ejecuta las pruebas automatizadas. No vuelve a procesar los tres CSV ni levanta PostgreSQL para ejecutar sql/verificacion.sql.

<img width="700" height="880" alt="image" src="https://github.com/user-attachments/assets/c2846b66-5255-4ec6-850b-0651d8aae15b" />


#### Se crea otra rama de GITHUB, feature/precio-cero

<img width="700" height="379" alt="image" src="https://github.com/user-attachments/assets/0650c75e-1a63-4161-9b24-deef476023f8" />

#### despues de actualizar reglas.py para que aceptara valores en cero, se actuaiza la version en la nueva rama


<img width="700" height="601" alt="image" src="https://github.com/user-attachments/assets/8bc6a8e3-cb3e-4e74-944e-17a79540933e" />

#### en GITHUB se compara y se realiza el pull request

<img width="700" height="192" alt="image" src="https://github.com/user-attachments/assets/1780aec1-883b-48df-8014-64dc1a074ffb" />


#### se abre la solicitud y se activa el pull


<img width="700" height="846" alt="image" src="https://github.com/user-attachments/assets/827241e6-7320-47cf-a503-9a7406dc2da1" />


#### El CI falla en ejecutar pruebas automatizadas

<img width="700" height="640" alt="image" src="https://github.com/user-attachments/assets/2b37f271-b42c-428c-93ec-c5a022007192" />


#### se visualiza  el CI fallido

<img width="700" height="659" alt="image" src="https://github.com/user-attachments/assets/0bbce578-b276-486a-b81c-867defb559c7" />

#### se revierte el cambio en GITHUB

<img width="700" height="590" alt="image" src="https://github.com/user-attachments/assets/e544049c-3926-4e8f-a55d-8b5b65f93c58" />


#### la nueva ejecucion de CI es satisfactoria

<img width="700" height="1014" alt="image" src="https://github.com/user-attachments/assets/72085087-2b8f-44f8-8ce6-12e667c17407" />

#### visualizacion de la ejecucion satisfactoria del CI

<img width="700" height="433" alt="image" src="https://github.com/user-attachments/assets/793cacf0-4983-4d49-84c2-9579231bfe71" />


#### se busca en GITHUB la solicitud de pull para hacer el merge


<img width="700" height="567" alt="image" src="https://github.com/user-attachments/assets/911b437d-ab83-4de0-9ae3-3c4d0373fb77" />


#### se realiza el merge

<img width="700" height="998" alt="image" src="https://github.com/user-attachments/assets/f94fc8b4-57fe-4ac4-a2a2-363d8436b023" />

#### confirmacion del revert, pull request fusionada sobre la rama principal

<img width="700" height="618" alt="image" src="https://github.com/user-attachments/assets/268ccf35-fb47-4dd1-92e1-aae5ba6ab15d" />

