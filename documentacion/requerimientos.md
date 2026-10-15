## Requerimientos funcionales

### N01. Los escritores necesitan distribuir relatos en archivos independientes y definir dónde y con qué información comienza cada partida.
- **RF1.1 Carga de historia externa:**  
  El sistema debe permitir cargar los datos de la historia desde un archivo externo independiente del código fuente.  
  *Criterio:* Al especificar la ruta de un archivo válido, el motor lee su contenido en memoria sin modificar el código fuente.  

- **RF1.2 Inicialización del estado:**  
  El sistema debe establecer la escena inicial y los valores por defecto de las variables booleanas a partir del archivo.  
  *Criterio:* Al iniciar una partida nueva, el sistema sitúa al jugador en la escena indicada y carga el mapa de variables en su estado original.  

---

### N02. Los lectores necesitan leer la escena actual y ver únicamente decisiones compatibles con la información obtenida.
- **RF2.1 Presentación de la escena:**  
  El sistema debe mostrar en pantalla el texto descriptivo de la escena activa.  
  *Criterio:* Al cambiar de escena, se imprime el contenido exacto del campo «texto».  

- **RF2.2 Filtrado de opciones por condiciones:**  
  El sistema debe evaluar las condiciones de cada opción contra el estado actual y mostrar solo las habilitadas.  
  *Criterio:* Si una opción requiere una variable verdadera y está en falso, no se imprime. Un mapa vacío habilita la opción automáticamente.  

---

### N03. Elegir debe producir consecuencias y llevar al destino previsto. Los errores de entrada no deben alterar la partida.
- **RF3.1 Transición de escenas:**  
  Al recibir una elección válida, el sistema cambia la escena activa al destino indicado.  
  *Criterio:* Si la opción seleccionada tiene destino «E4», la siguiente pantalla muestra la escena «E4».  

- **RF3.2 Inmunidad ante errores de entrada:**  
  El sistema debe rechazar cualquier entrada que no corresponda a una opción habilitada.  
  *Criterio:* Si el usuario ingresa un comando inválido, el sistema lo rechaza, pide nueva entrada y el estado se mantiene intacto.  

---

### N04. La experiencia debe recordar durante la partida lo ocurrido para que las elecciones posteriores tengan coherencia.
- **RF4.1 Aplicación de efectos:**  
  Tras una selección válida, el sistema actualiza el estado aplicando los efectos de la opción.  
  *Criterio:* Si la opción contiene el efecto `conoce_origen = verdadero`, la variable cambia y permanece así hasta el fin de la partida.  

---

### N05. El lector necesita reconocer el desenlace y comenzar otra partida sin conservar información de la anterior.
- **RF5.1 Detección de final:**  
  El sistema detecta escenas finales e informa el desenlace.  
  *Criterio:* Al llegar a una escena final, se imprime el texto y un mensaje de fin, sin solicitar elección.  

- **RF5.2 Reinicio de sesión limpia:**  
  Tras un final o bloqueo, el sistema permite iniciar una nueva partida restaurando el estado original.  
  *Criterio:* Al reiniciar, se regresa a la escena inicial y las variables vuelven a su estado original.  

- **RF5.3 Detección de bloqueo:**  
  Si una escena no final no tiene opciones habilitadas, el sistema informa bloqueo y ofrece reinicio.  
  *Criterio:* En una escena bloqueada, se muestra mensaje de bloqueo y se permite reiniciar.  

---

### N06. El escritor necesita saber por qué un archivo no es válido antes de que alguien lo juegue.
- **RF6.1 Validación previa de estructura y datos:**  
  El sistema debe escanear el archivo y rechazarlo si presenta errores críticos.  
  *Criterio:* Si un archivo tiene un destino inexistente («E99»), la partida no inicia.  

- **RF6.2 Diagnóstico de validación:**  
  Al rechazar un archivo, el sistema debe mostrar un mensaje claro con la causa y el ID afectado.  
  *Criterio:* Ejemplo: *Escena 'E2', opción 'investigar': destino 'E99' no existe*.  

---

## Requerimientos no funcionales

- **RNF01 Modificabilidad:**  
  Una segunda historia con al menos tres escenas, una condición y un efecto debe ejecutarse sin modificar el motor.  
  *Verificación:* Cargar la segunda historia y registrar su recorrido.  

- **RNF02 Claridad de errores:**  
  Cada categoría de error debe producir un diagnóstico identificable, sin iniciar partidas inválidas.  
  *Verificación:* Ejecutar casos incorrectos y guardar mensajes reales.  

- **RNF03 Confiabilidad:**  
  Las pruebas iniciales y la de integración deben finalizar correctamente.  
  *Verificación:* Ejecutar la suite completa y guardar resultados.  
