## Laboratorio: ETL de ventas con Airflow, pruebas y CI

## TODAS LAS EVIDENCIAS DE LA EJECUCION DEL LABORATORIO, INCLUIDO CORRIDAS DEL DAG Y LA INTEGRACION CONTINUA SE ENCUENTRAN EN LA CARPETA EVIDENCIAS DEL REPOSITORIO

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


## Respuestas

1. TODO
2. TODO
3. TODO
4. TODO

## Pull request

TODO
