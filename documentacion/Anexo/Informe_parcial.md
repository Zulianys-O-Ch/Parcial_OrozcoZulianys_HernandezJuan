Universidad tecnológica de Bolivar

Ingeniería de Software Código 1206

**Parcial práctico de Ingeniería de Software**

# La última transmisión

Motor de historias interactivas: requisitos, modelado, arquitectura, implementación y cambio

### Integrantes

Zulianys Liseth Orozco Chavez T00078330 Juan David Hernandez Avila T00081559

Cartagena, octubre de 2026

## Fundamentos: problema, alcance y calidad

### Problema

Un colectivo de escritores prepara una ficción interactiva para un festival universitario. Sus inte-grantes no programan, pero necesitan crear y modificar escenas y decisiones sin pedir cambios en el programa. Sin una herramienta que interprete sus narraciones, cada ajuste de contenido depende de un desarrollador y un error en el relato puede llegar al lector como un cierre inesperado. El proyecto desarrolla un motor que carga narraciones desde archivos, ofrece solo las decisiones compatibles con lo ocurrido en la partida, conserva ese estado y valida el contenido antes de que alguien lo juegue.

### Actores

#### Actor Interés principal Necesidades

Escritora principal Editar escenas y decisiones en un archivo, sin tocar

el código

Diseñador de la experiencia Decisiones con consecuencias y opciones que

dependen de lo descubierto

Coordinadora del festival Saber qué corregir en una historia con errores; que

el lector no sufra cierres

Lector Leer, elegir, llegar a un desenlace y comenzar otra partida

N01, N06

N02, N03, N04 N06

N02, N03, N05

Equipo de desarrollo Entregar motor, pruebas y evidencia verificables N01–N06

### Alcance

**Incluye:** carga de historias desde archivos independientes; estado inicial declarado en el archivo; condiciones de igualdad sobre variables booleanas y efectos que asignan verdadero o falso; estado de la partida en memoria; reconocimiento de finales y reinicio; validación previa del contenido (nueve categorías de error); interfaz \[de consola: ajustar si es otra\]; ejecución local; la historia de referencia de seis escenas y una segunda historia.

**Excluye:** cuentas, base de datos, guardado entre ejecuciones, conexión a internet, editor visual, audio, imágenes, lenguaje de expresiones y análisis automático de todos los caminos del relato.

**Decisión pendiente del cliente:** la escritora quiere permitir retroceder siempre y el diseñador quiere decisiones irreversibles. La versión inicial no implementa retroceso; la pregunta de aclaración y el acuerdo provisional se registran en la sección de requisitos, sin presuponer la decisión del cliente.

### Riesgos

#### ID Riesgo Prob./Imp. Mitigación y verificación

R1 Contenido inválido escrito por personas no programadoras provoca cierres o bloqueos durante la partida.

R2 El motor queda acoplado a la historia de referencia (identificadores de escena en el código) y la escritora vuelve a depender de programadores.

Alta / Alto Validación previa de las nueve

categorías de error con mensaje de causa y campo o ID, y manejo controlado de entradas inválidas. Se verifica con pruebas parametrizadas (RNF02, RNF03).

Media / Alto El motor evalúa condiciones y

destinos solo desde los datos; revisión del código en busca de identificadores de escena y prueba con una segunda historia sin editar el motor (RNF01).

### Priorización de atributos de calidad

1.  **Modificabilidad del contenido (RNF01).** Es la razón de ser del proyecto: la escritora pide agregar escenas y cambiar decisiones sin modificar el programa.
2.  **Claridad de errores (RNF02).** Un escritor no programador solo puede aprovechar esa libertad si sabe qué corregir; la coordinadora lo pide de forma explícita.
3.  **Confiabilidad (RNF03).** El lector no debe encontrarse con un cierre inesperado. Se atiende en buena medida con la misma validación previa de los dos atributos anteriores.

No se priorizan el rendimiento, la seguridad ni la portabilidad avanzada: las historias son pequeñas, se ejecutan localmente y no hay usuarios con datos sensibles. El costo aceptado es que la validación previa añade trabajo al cargar, despreciable a esta escala.

### Decisión de responsabilidad profesional: autoría y dependencias

Hay trazabilidad de autoría, instalación reproducible y licencias conocidas. El motor no almacena ni transmite datos personales, porque el estado vive solo en memoria durante la partida. El costo es la disciplina de llevar el registro mientras se trabaja.

## Requerimientos

### Requerimientos funcionales

##### ID Requisito Criterio de aceptación

**N01.** Los escritores necesitan distribuir relatos en archivos independientes y definir dónde y con qué infor-mación comienza cada partida.

RF1.1 **Carga de historia externa.** El sistema debe permitir cargar los datos de la histo-ria desde un archivo externo independiente del código fuente.

RF1.2 **Inicialización del estado.** El sistema de-be establecer la escena inicial y los valo-res por defecto de las variables booleanas a partir de la información declarada en el archivo.

Al especificar la ruta de un archivo válido, el mo-tor lee su contenido en memoria de forma exitosa sin modificar el código fuente del programa.

Al iniciar una partida nueva, el sistema sitúa al jugador en el identificador indicado en el campo

«inicio» y carga el mapa de variables en su es-tado original. Dos archivos distintos cargan dos historias distintas.

##### ID Requisito Criterio de aceptación

**N02.** Los lectores necesitan leer la escena actual y ver únicamente decisiones compatibles con la información obtenida.

RF2.1 **Presentación de la escena.** El sistema debe mostrar en pantalla el texto descrip-tivo correspondiente a la escena activa.

RF2.2 **Filtrado de opciones por condiciones.** El sistema debe evaluar el mapa de condi-ciones de cada opción contra el estado ac-tual de las variables y mostrar únicamente las opciones habilitadas.

Al cambiar de escena, se imprime el contenido exacto del campo «texto» de la nueva escena.

Si una opción requiere que una variable sea ver-dadera y en el estado actual es falsa, la opción no se imprime en pantalla. Un mapa de condiciones vacío habilita la opción automáticamente.

**N03.** Elegir debe producir las consecuencias indicadas en el relato y llevar al destino previsto. Los errores de entrada no deben alterar la partida.

RF3.1 **Transición de escenas.** Al recibir una elección válida, el sistema debe cambiar la escena activa al identificador indicado en el campo «destino» de dicha opción.

RF3.2 **Inmunidad ante errores de entrada.** El sistema debe rechazar cualquier entra-da del usuario que no corresponda a una opción actualmente habilitada.

Si la opción seleccionada tiene como destino

«E4», la siguiente pantalla muestra el conteni-do de la escena «E4».

Si el usuario ingresa un comando inválido o se-lecciona una opción inhabilitada o inexistente, el sistema lo rechaza en el motor, vuelve a pedir la entrada y el estado de la partida queda intacto.

**N04.** La experiencia debe recordar durante la partida qué ha ocurrido para que las elecciones posteriores tengan consecuencias coherentes.

RF4.1 **Aplicación de efectos.** Tras una selec-ción válida, el sistema debe actualizar el estado en memoria aplicando las asigna-ciones indicadas en el mapa de «efectos» de la opción elegida.

Si la opción elegida contiene el efecto

«conoce\_origen = verdadero», la variable conoce\_origen cambia a verdadero en la memoria de la sesión actual y permanece así hasta que la partida termine.

**N05.** El lector necesita reconocer el desenlace y comenzar otra partida sin conservar información de la anterior.

RF5.1 **Detección de final.** El sistema debe de-tectar cuándo la escena activa está mar-cada como final e informar el desenlace al usuario.

RF5.2 **Reinicio de sesión limpia.** Tras alcanzar un final o ser bloqueado, el sistema debe permitir iniciar una nueva partida restau-rando por completo el estado original de la historia.

RF5.3 **Detección de bloqueo.** Si durante una partida la escena activa no es final y nin-guna de sus opciones está habilitada, el sis-tema debe informar el bloqueo y permitir reiniciar.

Al llegar a una escena final (como E4, E5 o E6 del relato de referencia), el sistema imprime el texto de la escena y un mensaje que indica el fin del recorrido, y no solicita ninguna elección.

Al solicitar un reinicio, el sistema regresa a la escena de inicio y el mapa de variables pierde todos los cambios generados durante la partida anterior.

Dada una historia de prueba con una escena no final cuyas opciones no se cumplen con el estado actual, el sistema muestra un mensaje de blo-queo sin cerrarse y ofrece reiniciar la partida.

**N06.** El escritor necesita saber por qué un archivo no es válido antes de que alguien lo juegue.

RF6.1 **Validación previa de estructura y da-tos.** Antes de abrir la sesión jugable, el sistema debe escanear el archivo y recha-zarlo si presenta errores críticos (ilegible, falta de campos, inicio inexistente, IDs re-petidos, destinos fantasma o variables no declaradas/no booleanas, cantidad de op-ciones incompatible con el carácter final).

Si se intenta cargar un archivo con un destino

«E99» que no existe en las escenas, la partida no inicia.

##### ID Requisito Criterio de aceptación

RF6.2 **Diagnóstico de validación.** Al rechazar un archivo, el sistema debe mostrar un mensaje claro indicando la causa exacta y, si es posible, el campo o ID que provocó el error.

Frente al error del RF6.1, el sistema muestra por consola un mensaje que indica la causa y el ID de la escena u opción involucrada, por ejemplo:

«*Escena ’E2’, opción ’investigar’: destino ’E99’ no existe*».

### Requerimientos no funcionales

##### ID Requisito medible Cómo verificarlo

RNF01 — Modifica-bilidad

RNF02 — Claridad de errores

RNF03 — Confiabili-dad

Una segunda historia con al menos tres escenas, una condición y un efecto debe ejecutarse sin modificar los archivos del motor.

Cada categoría de error de contenido debe producir un diagnóstico identificable, sin iniciar una partida inválida.

Las seis pruebas iniciales exigidas y la prueba de integración deben finalizar correctamente.

Cargar la segunda historia y registrar su recorrido.

Ejecutar los casos de contenido incorrecto y guardar los mensajes reales.

Ejecutar la suite completa y guardar el resultado.

### Preguntas y supuestos

Durante la ventana del parcial no hay respuesta del cliente, por lo que cada pregunta se acompaña de un supuesto compatible con los requisitos explícitos.

##### ID Pregunta de aclaración Supuesto adoptado Afecta

P1 La escritora quiere permitir re-troceder siempre y el diseña-dor quiere decisiones irreversi-bles. ¿Debe el lector poder re-troceder a una escena anterior: siempre, nunca o solo en las de-cisiones que el escritor marque?

P2 ¿Los valores iniciales del mapa

«variables» también deben ser booleanos?

P3 ¿En qué orden se muestran las opciones habilitadas y cómo las elige el lector?

Acuerdo provisional: la versión inicial no imple-menta retroceso. Dentro de una partida las deci-siones no se deshacen y la única forma de volver al inicio es reiniciar. No se presupone la decisión posterior del cliente.

Sí. El contrato define «variables» como un mapa de booleanos iniciales, por lo que un valor inicial no booleano se rechaza como error de contenido, igual que un valor no booleano en condiciones o efectos.

Se muestran en el orden en que aparecen en el ar-chivo y el lector elige por el número de la lista. El motor identifica cada opción por su ID, de mo-do que el rechazo de una opción no habilitada no depende de la interfaz.

RF3.1, RF5.2

RF1.2, RF6.1

RF2.2, RF3.2

### Defecto detectado en la revisión de requisitos

-   -   -   **Requisito afectado:** RF5.1 (detección de finalización), en su versión previa.
        -   **Defecto:** una sola condición cubría dos situaciones distintas: escena «marcada como final o con cero opciones habilitadas». Una escena final y una escena no final bloqueada, es decir, con opciones pero ninguna habilitada, tienen causas y respuestas diferentes. El criterio de aceptación

las mezclaba en un solo mensaje («fin del recorrido o un bloqueo») y el bloqueo no tenía requisito ni criterio propio.

-   -   -   **Riesgo:** que una escena bloqueada se tratara como un final válido y el error del relato quedara oculto, sin una prueba que lo detectara.
        -   **Corrección:** RF5.1 queda limitado a las escenas finales y se agrega RF5.3 para el bloqueo, con su propio criterio de aceptación. RF5.2 (reinicio) conserva su identificador.
        -   **Artefactos afectados:** el modelo de estados distingue *Finalizada* de *Bloqueada*, y las pruebas incluyen un caso de bloqueo.
        -   **Cómo se detectó:** en la revisión de los requisitos, con apoyo de una herramienta de IA.
        -   **Otra inconsistencia corregida:** RF3.2 decía «ignorar» la entrada inválida, pero su criterio exigía mostrar un mensaje de error. Se unificó en «rechazar».

## Versión 2 — Solicitud de cambio de la hora 6

La versión 1 se conserva sin cambios en el commit base `f69bdc7` del repositorio. El anexo del cliente sustituye el acuerdo provisional de P1: el lector puede deshacer una elección, con un único nivel de retroceso. P1 queda resuelta; no se ofrece rehacer ni retroceso múltiple.

### Requisito nuevo y criterios de aceptación

**N07.** El lector necesita corregir su última decisión y revertir sus consecuencias sin perder el progreso anterior.

**RF7.1 — Deshacer la última elección válida.** Durante una sesión, el sistema debe restaurar exactamente la escena, las variables y las banderas de sesión al estado inmediatamente anterior a la última elección válida. El sistema ofrece un único nivel de deshacer: al utilizarlo, consume el historial; una nueva elección válida crea un nuevo punto de restauración. Las entradas inválidas no alteran el estado ni reemplazan el historial.

**RF7.2 — Disponibilidad del deshacer.** Al iniciar una sesión no debe existir un estado que deshacer. La acción debe estar disponible desde los finales E4, E5 y E6 para regresar a E3. Al reiniciar, el sistema debe limpiar el historial de deshacer junto con la restauración definida por RF5.2.

**Criterios de aceptación de RF7.1:**

1. Al comenzar una sesión, deshacer no está disponible y no modifica el estado.
2. Desde E2, elegir `investigar` lleva a E3 con `conoce_origen = true`; deshacer regresa a E2 con `conoce_origen = false`.
3. Después de deshacer, un segundo intento no cambia escena ni variables. Una nueva elección válida vuelve a habilitar un solo deshacer.
4. Una opción inexistente o deshabilitada se rechaza y conserva el punto de restauración previo.
5. Desde E4, E5 o E6 se puede deshacer la elección final y volver a E3 con todos los valores que existían antes de esa elección.
6. Reiniciar devuelve la sesión a E1 con las variables iniciales y elimina el historial; deshacer después del reinicio no produce cambios.

### Análisis de impacto del cambio

- **Requisitos:** el anexo reemplaza el supuesto provisional de P1. Se incorpora N07 y se especifican RF7.1 y RF7.2; el requisito existente de reinicio RF5.2 conserva su identificador y se coordina con RF7.2 para incluir la limpieza del historial.
- **Modelo de dominio y sesión:** no cambia el esquema de las historias. `Sesion` requiere conservar una copia profunda del estado anterior a una elección válida, incluyendo escena, variables y banderas `terminada` y `bloqueada`, y descartar esa copia al deshacer o reiniciar.
- **Flujo de elección:** la validación debe ocurrir antes de reemplazar el snapshot, de modo que tanto una opción inexistente como una deshabilitada preserven el estado y la posibilidad de deshacer existente. Una elección válida reemplaza el snapshot anterior con el estado inmediatamente previo a ella.
- **Interfaz:** se incorpora el comando `deshacer` cuando existe historial. La interfaz debe aceptarlo también al mostrar un final, para permitir el retorno requerido desde E4, E5 y E6; al volver a una escena activa, presenta nuevamente sus opciones según las variables restauradas.
- **Contenido y compatibilidad:** no se requieren cambios en JSON, historias ni dependencias externas. La regla aplica a cualquier historia cargada por el motor.
- **Pruebas y modelos:** U6 cubre restauración y consumo del nivel, preservación ante entradas inválidas y habilitación tras otra elección; U5 verifica que reiniciar borre el historial; I1 recorre la historia cargada y verifica el retorno desde cada final. Se actualizaron los diagramas de casos de uso, secuencia, clases y estados, además de la trazabilidad.

### Backlog de cambio

| Tarea | Estado | Artefacto |
|---|---|---|
| Definir RF7.1 y RF7.2 y criterios | Hecho | `documentacion/requerimientos.md`, este informe |
| Guardar/restaurar snapshot de sesión | Hecho | `motor/sesion.py` |
| Exponer el comando de retroceso | Hecho | `motor/interfaz.py` |
| Cubrir U6, reinicio U5 e integración I1 | Hecho | `pruebas/test_motor.py` |
| Actualizar modelos y trazabilidad | Hecho | `documentacion/Anexo/diagramas/diagramas.md` |
| Ejecutar suite y dejar evidencia | La suite pytest no pudo arrancar en este entorno porque pytest no está instalado; se registró la limitación y se ejecutó verificación directa del flujo V2 en `pruebas/resultados_pruebas.txt` | U1–U6, I1 |

### Trazabilidad V2

| Cambio | Diseño/código | Verificación |
|---|---|---|
| RF7.1: restauración exacta y nivel único | Estado de sesión y snapshot en `Sesion`; transiciones del diagrama de estados | U6: restauración, consumo, segundo intento y nueva elección |
| RF7.1: entrada inválida no reemplaza historial | Validación antes de guardar el snapshot en `Sesion.elegir` | U6: selección inexistente y opción deshabilitada conservan y permiten usar el snapshot |
| RF7.2: iniciar y reiniciar sin historial | Constructor y `reiniciar` limpian el punto de deshacer | U5: reinicio limpia historial |
| RF7.2: deshacer desde finales E4–E6 | Interfaz ofrece deshacer en estado final; snapshot incluye variables | I1 parametrizada: carga real, recorrido y restauración desde E4, E5 y E6 |

### Resultado de verificación y demostración

La suite pytest fue intentada, pero este entorno no tiene el paquete pytest instalado (y el `python` configurado inicialmente era un alias inaccesible); no se reporta como ejecutada. La verificación directa de los flujos V2 queda registrada en `pruebas/resultados_pruebas.txt`. Para la demostración manual: iniciar la historia principal; elegir `revisar`, luego `investigar`; deshacer y comprobar E2 con `conoce_origen = no`; intentar deshacer de nuevo y comprobar que no ocurre nada; continuar y observar en E3 las opciones `activar_sin_verificar` y `cortar`. Como recorrido adicional, llegar a E4, E5 o E6 y ejecutar `deshacer` en el aviso del final para volver a E3. Reiniciar y confirmar que deshacer ya no está disponible.
