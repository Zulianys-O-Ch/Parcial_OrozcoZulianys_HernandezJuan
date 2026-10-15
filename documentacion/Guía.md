Parcial práctico de

Ingeniería de Software

*La última transmisión*

-   Guía para estudiantes

Material inicial: esta guía y el archivo la\_ultima\_transmision.json. El docente entregará una solicitud de cambio acotada al cumplirse seis horas desde la apertura. Esta actividad integra las competencias centrales de las siete unidades.

Diseñen, implementen y prueben un motor de historias interactivas. Deberán convertir las necesidades de un cliente en requisitos, modelos, decisiones de arquitectura y software ejecutable, y después incorporar un cambio conservando la coherencia de la solución.

## Condiciones de realización

<table><tbody><tr><td><p><strong>Aspecto</strong></p></td><td><p><strong>Condición</strong></p></td></tr><tr><td><p>Modalidad</p></td><td><p>Parcial 100 % virtual y asincrónico, en parejas. Se califica exclusivamente la entrega digital. Ambos integrantes deben participar.</p></td></tr><tr><td><p>Duración</p></td><td><p>12 horas desde la apertura hasta el cierre publicado por el docente. La ventana incluye pausas, preparación y carga de la entrega.</p></td></tr><tr><td><p>Tecnología</p></td><td><p>Lenguaje y herramientas de su elección. Se acepta consola, escritorio o web. Debe ejecutarse localmente.</p></td></tr><tr><td><p>Entrega</p></td><td><p>Un archivo ZIP con informe, código, datos, pruebas y demostración. Consulten la sección de entrega.</p></td></tr><tr><td><p>Alcance</p></td><td><p>Motor pequeño con reglas booleanas. Se evalúan las decisiones de ingeniería y su evidencia; no la calidad literaria ni el diseño gráfico.</p></td></tr></tbody></table>

## El encargo del cliente

Un colectivo de escritores prepara una experiencia de ficción interactiva para un festival universitario. En la historia, una operadora de radio recibe una señal de una estación abandonada hace veinte años. Cada lector decide cómo responder y descubre un desenlace diferente según sus elecciones.

El colectivo necesita cargar narraciones desde archivos, ofrecer opciones condicionadas por lo ocurrido y detectar errores básicos del contenido. Su equipo desarrollará el motor que interpreta esas narraciones. La historia y las reglas de este documento son los datos iniciales del proyecto.

Preparación: antes de la apertura, comprueben que pueden ejecutar su lenguaje, leer JSON, correr una prueba automatizada y usar Git. Estas herramientas deben ser conocidas; la instalación y el aprendizaje inicial se realizan antes del parcial.

## Resultado esperado

Al finalizar, otra persona debe poder instalar y ejecutar la solución siguiendo el README, recorrer los tres finales, cargar una segunda historia sin cambiar el motor y comprobar que las pruebas pasan.

## Voces del cliente

Escritora principal: «Quiero agregar escenas y cambiar decisiones sin pedir que modifiquen el programa. No sé programar, pero puedo editar un archivo si me explican el formato».

Diseñador de la experiencia: «Las decisiones deben tener consecuencias. Algunas opciones solo deben aparecer cuando el lector haya descubierto cierta información».

Coordinadora del festival: «Si una historia contiene un error, necesitamos saber qué corregir. El lector no debe encontrarse con un cierre inesperado del programa».

Conflicto por resolver: la escritora quiere permitir retroceder siempre; el diseñador quiere decisiones irreversibles. En la versión inicial no implementen retroceso: documenten el conflicto, formulen una pregunta de aclaración y registren este acuerdo provisional. No presupongan una decisión posterior del cliente.

## Necesidades que debe cubrir la primera versión

Redacten sus propios requisitos funcionales, identifíquenlos como RF y vincúlenlos con las necesidades N01 a N06. Pueden descomponer una necesidad en varios requisitos atómicos. Cada RF debe indicar comportamiento observable y criterio de aceptación. La tabla delimita la cobertura; no sustituye su especificación.

<table><tbody><tr><td><p><strong>ID</strong></p></td><td><p><strong>Comportamiento requerido</strong></p></td></tr><tr><td><p>N01</p></td><td><p>Los escritores necesitan distribuir relatos en archivos independientes y definir dónde y con qué información comienza cada partida.</p></td></tr><tr><td><p>N02</p></td><td><p>Los lectores necesitan leer la escena actual y ver únicamente decisiones compatibles con la información obtenida.</p></td></tr><tr><td><p>N03</p></td><td><p>Elegir debe producir las consecuencias indicadas en el relato y llevar al destino previsto. Los errores de entrada no deben alterar la partida.</p></td></tr><tr><td><p>N04</p></td><td><p>La experiencia debe recordar durante la partida qué ha ocurrido para que las elecciones posteriores tengan consecuencias coherentes.</p></td></tr><tr><td><p>N05</p></td><td><p>El lector necesita reconocer el desenlace y comenzar otra partida sin conservar información de la anterior.</p></td></tr><tr><td><p>N06</p></td><td><p>El escritor necesita saber por qué un archivo no es válido antes de que alguien lo juegue. Los errores mínimos se precisan en la sección de validación.</p></td></tr></tbody></table>

## Límites del ejercicio

No se requieren cuentas, base de datos, guardado entre ejecuciones, conexión a internet, editor visual, audio, imágenes ni lenguaje de expresiones. Solo se necesitan condiciones de igualdad sobre variables booleanas y efectos que asignen verdadero o falso. Se permite utilizar bibliotecas para leer archivos y ejecutar pruebas.

Elijan tres requisitos no funcionales medibles, con procedimiento y evidencia de verificación. Relaciónenlos con el caso: modificabilidad del contenido, claridad de errores, confiabilidad o facilidad de uso. Eviten expresiones sin medida como «rápido» o «amigable». Verifíquenlos localmente, con datos y procedimientos reproducibles; no se exigen usuarios externos, servicios pagos ni infraestructura especial.

Utilicen el archivo adjunto la\_ultima\_transmision.json, que ya contiene estas seis escenas y todas las opciones. Pueden ampliar la redacción sin cambiar las rutas ni las reglas. Las tres últimas escenas son finales; están incluidas en el total de seis.

<table><tbody><tr><td><p><strong>Escena</strong></p></td><td><p><strong>Texto de referencia</strong></p></td></tr><tr><td><p>E1 La señal</p></td><td><p>Son las 02:13. Una voz pide ayuda desde la estación Aurora, abandonada hace veinte años. La operadora decide revisar la transmisión.</p></td></tr><tr><td><p>E2 El archivo</p></td><td><p>La señal incluye un código antiguo. Es posible consultar el archivo para averiguar su procedencia o continuar sin investigar.</p></td></tr><tr><td><p>E3 La respuesta</p></td><td><p>La voz pide activar la antena. Con la información disponible, la operadora debe decidir si confía en ella o corta la comunicación.</p></td></tr><tr><td><p>E4 Rescate</p></td><td><p>La operadora reconoce el código de emergencia, activa la antena y guía a un equipo de rescate. La transmisión provenía de una expedición aislada.</p></td></tr><tr><td><p>E5 El eco</p></td><td><p>La operadora activa la antena sin comprobar el origen. Solo recibe un mensaje automático antiguo. La voz se repite hasta el amanecer.</p></td></tr><tr><td><p>E6 Silencio</p></td><td><p>La operadora interrumpe la comunicación. El origen de la señal queda sin resolver.</p></td></tr></tbody></table>

Estado inicial: escena E1; conoce\_origen = falso; confia\_en\_la\_voz = falso. E4, E5 y E6 no tienen opciones de avance.

<table><tbody><tr><td><p><strong>Origen</strong></p></td><td><p><strong>Opción y destino</strong></p></td><td><p><strong>Condición</strong></p></td><td><p><strong>Efectos</strong></p></td></tr><tr><td><p>E1</p></td><td><p>Revisar señal → E2</p></td><td><p>Ninguna</p></td><td><p>Ninguno</p></td></tr><tr><td><p>E2</p></td><td><p>Investigar archivo → E3</p></td><td><p>Ninguna</p></td><td><p>conoce_origen = verdadero</p></td></tr><tr><td><p>E2</p></td><td><p>Continuar sin investigar → E3</p></td><td><p>Ninguna</p></td><td><p>Ninguno</p></td></tr><tr><td><p>E3</p></td><td><p>Activar con código → E4</p></td><td><p>conoce_origen = verdadero</p></td><td><p>confia_en_la_voz = verdadero</p></td></tr><tr><td><p>E3</p></td><td><p>Activar sin verificar → E5</p></td><td><p>conoce_origen = falso</p></td><td><p>confia_en_la_voz = verdadero</p></td></tr><tr><td><p>E3</p></td><td><p>Cortar comunicación → E6</p></td><td><p>Ninguna</p></td><td><p>confia_en_la_voz = falso</p></td></tr></tbody></table>

En E3 deben verse exactamente dos opciones: cortar la comunicación y la activación que corresponda al valor de conoce\_origen. El motor debe evaluar las condiciones desde los datos, sin decisiones de código específicas para E1, E2 u otros identificadores de esta historia.

## Contrato de contenido

Pueden usar JSON, YAML u otro formato documentado. El siguiente contrato JSON sirve de referencia. Si lo adaptan, conserven su significado y expliquen la equivalencia en el README.

<table><tbody><tr><td><p><strong>Elemento</strong></p></td><td><p><strong>Campos y significado</strong></p></td></tr><tr><td><p>Historia</p></td><td><p>titulo: texto; inicio: ID de escena; variables: mapa de booleanos iniciales; escenas: lista de escenas.</p></td></tr><tr><td><p>Escena</p></td><td><p>id: identificador único; texto: contenido visible; final: booleano; opciones: lista, vacía si es final.</p></td></tr><tr><td><p>Opción</p></td><td><p>id: único dentro de la escena; texto: etiqueta visible; destino: ID existente; condiciones: mapa de igualdades; efectos: mapa de asignaciones.</p></td></tr><tr><td><p>Evaluación</p></td><td><p>Un mapa condiciones vacío habilita la opción. Todas las condiciones deben cumplirse. Un mapa efectos vacío conserva las variables.</p></td></tr></tbody></table>

Ejemplo de una opción de E2. Es un fragmento, no un archivo de historia completo:

{

"id": "investigar",

"texto": "Investigar archivo", "destino": "E3",

"condiciones": {},

"efectos": {"conoce\_origen": true}

}

## Validación y errores

Rechacen antes de iniciar un archivo ilegible o sin campos obligatorios, una escena inicial inexistente, IDs de escenas repetidos, IDs de opciones repetidos dentro de una escena, destinos inexistentes y condiciones o efectos que utilicen variables no declaradas o valores no booleanos. El mensaje debe indicar la causa y el campo o ID involucrado, cuando sea identificable.

Las escenas finales deben tener cero opciones y las no finales al menos una. Si durante una partida ninguna opción queda habilitada en una escena no final, informen el bloqueo y permitan reiniciar. No se exige analizar automáticamente todos los caminos posibles del relato.

## Ejemplos de aceptación

CA01. Dada una partida nueva, al elegir revisar señal e investigar archivo, la sesión queda en E3 con conoce\_origen verdadero; se muestran activar con código y cortar comunicación.

CA02. Dada E3 sin conocer el origen, activar sin verificar lleva a E5. No debe poder ejecutarse activar con código, aunque se intente enviar su identificador directamente al motor.

CA03. Dada una copia del contenido con un destino E99 inexistente, la carga se rechaza con un mensaje que identifica el problema, sin abrir una sesión jugable.

Trabajen de forma incremental. Actualicen los artefactos cuando cambien las decisiones y mantengan un vocabulario consistente entre requisitos, diagramas y código.

<table><tbody><tr><td><p><strong>Unidad</strong></p></td><td><p><strong>Actividad y evidencia mínima</strong></p></td></tr><tr><td><p>1 Fundamentos</p></td><td><p>Definan problema, actores, alcance y dos riesgos. Prioricen atributos de calidad y expliquen una decisión de responsabilidad profesional sobre datos, autoría o dependencias.</p></td></tr><tr><td><p>2 Procesos</p></td><td><p>Elijan un proceso y compárenlo con una alternativa. Identifiquen cómo realizarán especificación, desarrollo, validación y evolución en esta entrega.</p></td></tr><tr><td><p>3 Agilidad</p></td><td><p>Mantengan backlog, tablero con responsables y capturas inicial y final. Justifiquen dos prácticas ágiles utilizadas y una alternativa descartada. Definan terminado y registren un aprendizaje con una acción de mejora.</p></td></tr><tr><td><p>4 Requerimientos</p></td><td><p>Especifiquen RF propios que cubran N01 a N06 y tres RNF medibles. Registren tres preguntas y respuestas o supuestos. Revisen los requisitos entre integrantes y documenten una ambigüedad o defecto con su corrección.</p></td></tr><tr><td><p>5 Modelado</p></td><td><p>Incluyan contexto, casos de uso, clases del dominio, secuencia de elegir una opción y estados de una sesión. Los diagramas deben ser pequeños y legibles; el mapa narrativo no sustituye los modelos del software.</p></td></tr><tr><td><p>6 Arquitectura</p></td><td><p>Presenten un diagrama de componentes o capas con responsabilidades y relaciones. Documenten dos decisiones: contexto, alternativas, elección y consecuencias. Justifiquen la separación entre contenido, reglas e interfaz.</p></td></tr><tr><td><p>7 Implementación</p></td><td><p>Implementen, prueben y versionen la solución. Expliquen una decisión de diseño detallado sobre responsabilidades o acoplamiento y documenten las bibliotecas utilizadas y sus licencias.</p></td></tr></tbody></table>

## Distribución sugerida del tiempo

<table><tbody><tr><td><p><strong>Actividad</strong></p></td><td><p><strong>Tiempo</strong></p></td></tr><tr><td><p>Comprensión y alcance</p></td><td><p>45 min</p></td></tr><tr><td><p>Requisitos y organización</p></td><td><p>1 h 15 min</p></td></tr><tr><td><p>Modelado y arquitectura</p></td><td><p>1 h 30 min</p></td></tr><tr><td><p>Primera implementación</p></td><td><p>3 h</p></td></tr><tr><td><p>Cambio y pruebas</p></td><td><p>1 h 30 min</p></td></tr><tr><td><p>Verificación y entrega</p></td><td><p>2 h</p></td></tr><tr><td><p>Pausas y contingencias</p></td><td><p>2 h</p></td></tr><tr><td><p>Total</p></td><td><p>12 h</p></td></tr></tbody></table>

El presupuesto suma 12 horas y no fija franjas consecutivas. En la hora 6 guarden el avance disponible como versión inicial, aunque esté incompleto, lean el cambio y replanifiquen. No se exige terminar toda la primera versión antes de recibirlo. Si no reciben respuesta a una duda durante la ventana, documenten un supuesto compatible con los requisitos explícitos y continúen.

## Segunda fase desde la hora 6

Al cumplirse seis horas desde la apertura, el docente publicará el documento Solicitud de cambio del parcial en la misma actividad del aula virtual donde recibieron esta guía. Cada pareja debe revisar esa actividad en ese momento y descargar el archivo, aunque no reciba una notificación automática. El cierre se mantiene en la hora 12. Hasta entonces, trabajen con el alcance inicial.

Al recibir el cambio: identifiquen la versión de partida; registren los requisitos, modelos, componentes y pruebas afectados; ajusten el backlog; incorporen la modificación y actualicen la trazabilidad. Documenten qué cambió y qué evidencia demuestra su funcionamiento.

## Pruebas mínimas de la primera versión

Cubran los siguientes cinco escenarios unitarios y un escenario de integración mediante pruebas automatizadas. Cada caso debe contener entradas, resultado esperado y aserciones. Se aceptan pruebas parametrizadas: importa la cobertura de escenarios, no la cantidad de funciones de prueba.

<table><tbody><tr><td><p><strong>Caso</strong></p></td><td><p><strong>Comprobación obligatoria</strong></p></td></tr><tr><td><p>U1</p></td><td><p>Las condiciones cumplidas y no cumplidas habilitan únicamente las opciones correspondientes.</p></td></tr><tr><td><p>U2</p></td><td><p>Una elección válida aplica los efectos y avanza al destino correcto.</p></td></tr><tr><td><p>U3</p></td><td><p>Una opción inexistente o no habilitada deja intacto el estado.</p></td></tr><tr><td><p>U4</p></td><td><p>Los errores de contenido obligatorios producen rechazo o diagnóstico controlado. Usen datos parametrizados para cubrir las variantes.</p></td></tr><tr><td><p>U5</p></td><td><p>Reiniciar restaura la escena y las variables iniciales.</p></td></tr><tr><td><p>I1</p></td><td><p>La lectura de un archivo real y el motor funcionan juntos: carga y decisiones hasta alcanzar un final.</p></td></tr></tbody></table>

## Cobertura de validación

Incluyan casos para archivo ilegible o estructura incorrecta, campos obligatorios ausentes, inicio inexistente, IDs de escenas u opciones duplicados dentro de su ámbito, destino inexistente, variable no declarada, valor no booleano y cantidad de opciones incompatible con el carácter final de una escena. Comprueben también la respuesta ante una escena no final sin opciones habilitadas durante una partida.

La solicitud de cambio añadirá un escenario unitario y extenderá los casos pertinentes. El mínimo final será de seis escenarios unitarios y uno de integración. Pueden agrupar variantes en una prueba parametrizada sin perder sus aserciones individuales.

## Verificación del producto

Recorran los tres finales, carguen una segunda historia y verifiquen los tres RNF con procedimientos locales. Conserven los resultados reales y declaren los fallos pendientes. Capturas manuales pueden complementar la evidencia, pero no sustituyen las pruebas automatizadas exigidas.

## Contenido del archivo ZIP

Entreguen un único ZIP por pareja: Parcial\_ApellidoNombre\_ApellidoNombre.zip. Usen el primer apellido y el primer nombre de cada integrante, sin espacios ni tildes. Ejemplo: Laura Pérez y Andrés Gómez entregan Parcial\_PerezLaura\_GomezAndres.zip. Incluyan los nombres completos de ambos en el informe y el README.

<table><tbody><tr><td><p><strong>Elemento</strong></p></td><td><p><strong>Contenido obligatorio</strong></p></td></tr><tr><td><p>Informe PDF</p></td><td><p>Máximo ocho páginas de cuerpo, incluida la identificación. Agreguen un anexo PDF, fuera de ese límite, solo con diagramas, matriz y capturas de tablero. Referéncienlo desde el informe; no dupliquen contenido ni incluyan páginas de código.</p></td></tr><tr><td><p>Código y datos</p></td><td><p>Código fuente completo, historia de seis escenas y una segunda historia de mínimo tres escenas con una condición y un efecto. Esta segunda historia debe funcionar sin editar el motor.</p></td></tr><tr><td><p>README</p></td><td><p>Integrantes, versiones requeridas, instalación, comandos de ejecución y pruebas, formato de contenido, rutas para demostrar cada final y limitaciones conocidas.</p></td></tr><tr><td><p>Pruebas y resultados</p></td><td><p>Archivos de pruebas automatizadas y registro de su última ejecución. Incluyan verificación de los requisitos no funcionales y de los errores de contenido.</p></td></tr><tr><td><p>Evidencia de trabajo</p></td><td><p>Capturas inicial y final del tablero; historial exportado de Git con autores, fechas y mensajes; identificación de las versiones anterior y posterior al cambio.</p></td></tr><tr><td><p>Demostración</p></td><td><p>Grabación de pantalla MP4 de máximo seis minutos, preparada por ambos integrantes y con texto legible. Puede explicarse con voz o rótulos, sin cámara ni sesión en vivo. Inclúyanla en el ZIP o enlácenla desde el README con acceso para el docente.</p></td></tr></tbody></table>

## Guion de la demostración

Muestren los tres finales y cómo una condición cambia las opciones. Carguen la segunda historia con el mismo motor. Presenten el error de un destino inexistente, ejecuten las pruebas y demuestren el comportamiento solicitado en la segunda fase. Cierren explicando una decisión de arquitectura y el impacto del cambio.

## Trazabilidad y participación

Relacionen todos sus RF, incluidos los del cambio, y los tres requisitos no funcionales con los modelos pertinentes, los componentes o archivos que los atienden y la evidencia de verificación. No basta con marcar

«cumple»: indiquen nombres o rutas que permitan localizar cada evidencia.

Incluyan una breve declaración de aportes por integrante vinculada con archivos, tareas o cambios del historial. La entrega digital representa el 100 % de la nota del parcial y ambos integrantes reciben la misma calificación de la pareja. No habrá sustentación ni sesión sincrónica posterior.

## Fuentes y herramientas de apoyo

Identifiquen bibliotecas, fragmentos reutilizados, tutoriales y herramientas de IA que hayan utilizado, indicando para qué sirvieron y cómo verificaron sus resultados. Respeten las reglas institucionales y las indicaciones del docente sobre ayudas permitidas. Presenten resultados que hayan comprobado y distingan el trabajo propio del material adaptado.

La entrega digital de la pareja se valora sobre 100 puntos y representa el 100 % de la nota de ambos integrantes. Cada evidencia tiene un valor explícito; no se califican la calidad literaria ni la sofisticación gráfica.

<table><tbody><tr><td><p><strong>Criterio</strong></p></td><td><p><strong>Pts</strong></p></td><td><p><strong>Evidencias y distribución interna</strong></p></td></tr><tr><td><p>Problema y calidad</p></td><td><p>10</p></td><td><p>Problema, actores y alcance: 3. Dos riesgos con mitigación: 2. Priorización razonada de calidad: 3. Decisión de responsabilidad profesional: 2.</p></td></tr><tr><td><p>Proceso y agilidad</p></td><td><p>10</p></td><td><p>Proceso y alternativa: 2. Backlog y tablero con evolución: 2. Dos prácticas aplicadas y una alternativa descartada: 3. Definición de terminado: 2. Aprendizaje y acción de mejora: 1.</p></td></tr><tr><td><p>Requerimientos</p></td><td><p>20</p></td><td><p>RF propios, atómicos, identificados y con cobertura de N01 a N06: 6. Criterios de aceptación: 4. Tres RNF medibles con procedimiento: 6. Tres preguntas y respuestas o supuestos: 2. Defecto detectado y corrección: 2.</p></td></tr><tr><td><p>Modelado</p></td><td><p>15</p></td><td><p>Contexto, casos de uso, clases, secuencia y estados: 2 por modelo. Coherencia conjunta con requisitos y versión final: 5.</p></td></tr><tr><td><p>Arquitectura</p></td><td><p>15</p></td><td><p>Diagrama con responsabilidades y relaciones: 4. Dos decisiones con alternativas y consecuencias: 3 cada una. Separación entre contenido, motor e interfaz demostrada con la segunda historia: 5.</p></td></tr><tr><td><p>Implementación y pruebas</p></td><td><p>20</p></td><td><p>Carga, elecciones, estado, finales y reinicio: 6. Validaciones y manejo controlado de errores: 4. Cobertura inicial U1 a U5 e I1 con aserciones y resultados: 6. Ejecución reproducible y dependencias documentadas: 2. Verificación real de RNF: 2.</p></td></tr><tr><td><p>Cambio y trazabilidad</p></td><td><p>10</p></td><td><p>Análisis de impacto y versión previa: 2. Comportamiento nuevo y sus pruebas: 4. Artefactos actualizados y trazabilidad localizable: 4.</p></td></tr></tbody></table>

## Reglas para asignar puntos

En cada subcriterio se asigna el total si están todos sus elementos y son verificables; la mitad si existe evidencia correcta pero incompleta; cero si falta, es incorrecta o no puede comprobarse. En los elementos contables se evalúa cada unidad por separado: cada modelo vale 2, cada RNF 2 y cada decisión arquitectónica

3\. La cobertura de las seis necesidades dentro del subcriterio de RF vale 1 por necesidad.

Para implementación, los 6 puntos del flujo se distribuyen en carga 1, selección válida y rechazo de entradas inválidas 2, conservación de estado 1, finales 1 y reinicio 1. Cada uno de los seis escenarios iniciales automatizados aporta 1 punto. Los 4 puntos de validación se asignan proporcionalmente a las nueve categorías de error enumeradas en la sección de pruebas.

El mismo defecto no se penaliza dos veces dentro de un subcriterio. Un fallo de ejecución no anula automáticamente requisitos o modelos correctos: cada evidencia se califica por separado. El docente registrará la evidencia faltante o incorrecta que justifica una reducción.

# 8 Entrega virtual y revisión final

## Calificación final

El puntaje obtenido en la rúbrica de la entrega es la nota final sobre 100 para cada integrante. Si se requiere escala de 0 a 5, dividan ese puntaje entre 20. Ejemplo: 84 puntos equivalen a 4,2 sobre 5. No existe un componente adicional de evaluación oral.

## Publicación y descarga del cambio

Revisen la misma actividad del aula virtual al cumplirse seis horas desde la apertura. Allí encontrarán el documento Solicitud de cambio del parcial. Descárguenlo y conserven una copia junto a sus materiales de trabajo. La revisión de la actividad es obligatoria y no depende de recibir un correo o una notificación automática.

## Carga de la entrega

Un integrante realizará la entrega en nombre de la pareja en esa misma actividad del aula virtual. Antes del cierre, ambos deben verificar el nombre del ZIP, la identificación de los integrantes y que la plataforma confirme el envío. Conserven el comprobante o una captura de la confirmación.

Comprueben que el archivo se descomprime, que las instrucciones permiten ejecutar el programa y que los enlaces del video tienen permisos de acceso para el docente. La grabación es una evidencia del funcionamiento entregada dentro de las 12 horas; no habrá una reunión posterior para presentarla.

## Lista de revisión antes de entregar

-   La solución puede instalarse y ejecutarse siguiendo únicamente el README.
-   Los tres finales son alcanzables y las opciones dependen del estado.
-   La segunda historia funciona sin modificar el código del motor.
-   Los errores obligatorios producen respuestas controladas y comprensibles.
-   La solicitud de cambio está implementada y cubierta por pruebas.
-   Los requisitos, modelos y matriz corresponden a la versión entregada.
-   Se incluyeron resultados reales, fuentes y aportes de ambos integrantes.
-   El ZIP, el informe, el anexo y el video o su enlace abren correctamente.