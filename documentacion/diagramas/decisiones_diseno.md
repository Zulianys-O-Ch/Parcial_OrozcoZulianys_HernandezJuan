# Decisiones de diseño — La última transmisión

## 1. Propósito

Este documento registra las decisiones iniciales de diseño y arquitectura de **La última transmisión**. Su propósito es explicar cómo se propone organizar el sistema para facilitar su implementación, mantenimiento y verificación frente a los requerimientos del proyecto.

Las decisiones descritas son una propuesta de diseño y deberán ajustarse si la implementación o los requerimientos acordados lo necesitan.

## 2. Organización general

Se propone dividir el sistema en componentes con responsabilidades diferenciadas:

- **Presentación:** interactúa con el jugador, muestra el texto de la escena, presenta las opciones disponibles y comunica errores o resultados.
- **Gestión de sesión:** controla la partida actual, mantiene la escena activa y permite iniciar o reiniciar una partida.
- **Motor de historias:** procesa la opción seleccionada, comprueba si está habilitada, aplica sus efectos y determina la escena de destino.
- **Carga de historias:** lee la historia almacenada en un archivo JSON externo.
- **Validación y diagnósticos:** comprueba la estructura y consistencia de la historia antes de iniciar la partida y prepara mensajes comprensibles cuando encuentra problemas.
- **Modelo del dominio:** representa los conceptos principales del sistema, como historia, escena, opción y estado de la partida.

Esta separación busca evitar que toda la lógica quede concentrada en un único módulo y facilita revisar y probar cada responsabilidad por separado.

## 3. Historias almacenadas en JSON

Se propone almacenar el contenido de las historias en archivos JSON externos al motor del juego. De esta forma, se podrán agregar o modificar historias mediante sus datos sin tener que cambiar la lógica principal, siempre que respeten la estructura definida por el proyecto.

Antes de utilizar una historia, el sistema deberá comprobar que el archivo se pueda leer y que sus datos cumplan las reglas de validación acordadas.

## 4. Modelo de datos y clases principales

El diseño inicial contempla las siguientes clases o componentes:

- **Historia:** representa una historia, sus escenas, el punto de inicio y las variables iniciales.
- **Escena:** representa una escena con su identificador, texto, opciones y, cuando corresponda, la indicación de que es final.
- **Opcion:** representa una elección, su destino, sus condiciones y los efectos que puede producir.
- **Sesion:** administra la escena actual, las variables de la partida y su estado.
- **CargadorJSON:** se encarga de leer los datos de la historia desde el archivo externo.
- **ValidadorHistoria:** verifica la estructura, los identificadores, los destinos y las referencias que correspondan según los requerimientos.
- **Diagnostico:** representa o prepara la información necesaria para explicar los errores detectados.

Estos nombres son una propuesta inicial. La implementación podrá adaptar las clases y sus métodos sin perder las responsabilidades descritas.

## 5. Validación y manejo de errores

La historia se deberá validar antes de comenzar a jugar. La validación deberá cubrir las reglas establecidas en los requerimientos, como la estructura de los datos y la consistencia de las referencias entre escenas.

Si se detecta un archivo inválido, el sistema deberá informar del problema mediante un mensaje claro y evitar iniciar una partida con datos que no hayan superado la validación. Los mensajes concretos dependerán de los errores que el sistema pueda identificar.

## 6. Selección de opciones y cambios de estado

Cuando el jugador seleccione una opción, el sistema deberá comprobar que exista y que esté habilitada en el estado actual de la partida.

- Si la opción es válida, el sistema podrá aplicar sus efectos y avanzar a la escena de destino.
- Si la opción no existe o no está habilitada, deberá informar del problema y conservar el estado de la partida sin aplicar efectos ni cambiar de escena.

Esta regla permite mantener la consistencia de la partida ante entradas inválidas.

## 7. Finalización, bloqueo y reinicio

El diseño contempla distinguir entre una partida en curso, una partida finalizada y una partida bloqueada.

- **Finalizada:** se alcanza una escena definida como final.
- **Bloqueada:** no quedan opciones habilitadas y la escena actual no se ha definido como final.
- **Reinicio:** permite volver al estado inicial de la historia según las reglas del proyecto.

La lógica deberá comprobar estas condiciones después de procesar una elección válida.

## 8. Pruebas y confiabilidad

Se propone verificar por separado los comportamientos principales mediante pruebas, incluyendo:

- Carga de historias válidas e inválidas.
- Validación de la estructura y las referencias entre escenas.
- Visualización de las opciones habilitadas.
- Rechazo de opciones inválidas sin alterar el estado.
- Aplicación de efectos y transición entre escenas.
- Detección de finales y situaciones bloqueadas.
- Reinicio de la partida.

Las pruebas y sus resultados se documentarán cuando se implemente el sistema. Este documento no afirma que dichas pruebas ya se hayan ejecutado.

## 9. Relación con los diagramas

Las decisiones anteriores se complementan con los diagramas de la carpeta `documentacion/`:

- `01_contexto.mmd`: actores y límites del sistema.
- `02_casos_uso.mmd`: acciones principales que ofrece el sistema.
- `03_clases.mmd`: clases propuestas y sus relaciones.
- `04_secuencia.mmd`: interacción durante la carga, validación y ejecución de una partida.
- `05_estados.mmd`: estados posibles de la partida y sus transiciones.
- `06_arquitectura.mmd`: organización de los componentes y sus responsabilidades.

Los diagramas y este documento deberán mantenerse coherentes con los requerimientos y con el código que finalmente se implemente.

## 10. Aspectos pendientes de confirmar

Antes de cerrar el diseño, el equipo deberá confirmar:

- El lenguaje de programación y la estructura concreta de archivos.
- El formato exacto del JSON y las reglas completas de validación.
- La representación de condiciones, efectos y variables.
- El comportamiento preciso esperado al reiniciar una partida.
- Los casos de prueba y las evidencias que se incluirán en la entrega.
