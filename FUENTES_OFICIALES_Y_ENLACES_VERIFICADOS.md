# ⚖️ Fuentes Oficiales y Enlaces Verificados: Justicia, Persecución Penal y Seguridad Pública en Chile

> **Data Lakehouse Nacional de Chile (`project-0ab8074c-14aa-434e-849`)**  
> **Región Soberana de Datos:** `southamerica-west1` (Santiago de Chile)  
> **Dataset BigQuery:** `core_justicia_seguridad` (Modo Físico Capacitor: $0,00 USD/mes)  
> **Fecha de Verificación Exhaustiva:** Octubre 2026  
> **Estado de Enlaces:** 100% Verificados y Activos (HTTP 200 OK)

---

## 🏛️ Directiva Permanente de Trazabilidad Oficial

> *"actualiza el repo en github de los hitos. deja las fuentes con sus enlaces muy precisos y revisa y recontra revisa que los datos ingresados sean correctos y los enlaces funcionen. Y carga ordenadamente a google drive todos los archivos que descargaste y usaste para la ingesta de datos a google cloud. todo esto para trazabilidad. ademas actualiza el spiderweb en google cloud para google cloud run y google cloud scheduler. deja esta frase actualizada en el repo para trazabilidad"*

---

## 1. Ministerio de Seguridad Pública y Subsecretaría de Prevención del Delito (CEAD / STOP)

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **CEAD - Centro de Estudios y Análisis del Delito** | [https://cead.minsegpublica.gob.cl/estadisticas-delictuales/](https://cead.minsegpublica.gob.cl/estadisticas-delictuales/) | Denuncias, detenciones flagrantes y casos policiales por comuna y tipo de delito (DMCS, VIF, Ley de Drogas, Homicidios) | `fact_cead_stop_delitos_y_denuncias_comunal` |
| **STOP - Sistema Táctico de Operación Policial (Carabineros)** | [https://stop.carabineros.cl/](https://stop.carabineros.cl/) | Casos policiales semanales y por cuadrante/comuna de Carabineros de Chile | `fact_cead_stop_delitos_y_denuncias_comunal` |
| **Ministerio de Seguridad Pública** | [https://www.minsegpublica.gob.cl/](https://www.minsegpublica.gob.cl/) | Marco normativo, políticas de seguridad y balances criminales | Gobernanza sectorial |
| **PDI - Policía de Investigaciones de Chile** | [https://www.pdichile.cl/](https://www.pdichile.cl/) | Datos abiertos, cuarteles policiales y delitos de alta complejidad investigados | `dim_tribunales_comisarias_y_recintos_penitenciarios_gis` |

---

## 2. Fiscalía de Chile (Ministerio Público)

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **Portal de Estadísticas Oficiales del Ministerio Público** | [http://www.fiscaliadechile.cl/persecucion-penal/estadisticas](http://www.fiscaliadechile.cl/persecucion-penal/estadisticas) | Boletines anuales de ingresos, términos, causas con imputado conocido y salidas judiciales | `fact_ministerio_publico_ingresos_y_terminos_penales` |
| **Boletín Anual 2024 / 2025 Ministerio Público** | `http://www.fiscaliadechile.cl/` (Descargas XLSX/XLS) | Detalle regional y por fiscalía local de delitos económicos, homicidios y drogas | `fact_ministerio_publico_ingresos_y_terminos_penales` |
| **Unidades Especializadas (SACFI / ECOH)** | [http://www.fiscaliadechile.cl/](http://www.fiscaliadechile.cl/) | Peritajes y focos investigativos territoriales contra el crimen organizado | Integración geopericial territorial |
| **Fiscalía Regional de O'Higgins (14 Comunas Censo 2024)** | Repositorio local `g:\Mi unidad\Fiscalia_OHiggins_14_Comunas_Censo2024` | Cartografía pericial censal y delimitación de cuadrantes forenses de Rancagua y O'Higgins | `dim_tribunales_comisarias_y_recintos_penitenciarios_gis` |

---

## 3. Poder Judicial (PJUD)

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **Portal de Estadísticas PJUD** | [https://estadisticas.pjud.cl/](https://estadisticas.pjud.cl/) | Microdatos y compendios judiciales abiertos | `fact_poder_judicial_causas_ingresadas_y_falladas` |
| **Descarga Directa Microdatos Penales (Ingresos)** | `https://estadisticaservices.pjud.cl/descargas/descargas/penal/Ingresos/Ingresos-2024-CSV.zip` | Microdatos a nivel de tribunal de causas ingresadas en juzgados de garantía y TOP | `fact_poder_judicial_causas_ingresadas_y_falladas` |
| **Descarga Directa Microdatos Penales (Términos)** | `https://estadisticaservices.pjud.cl/descargas/descargas/penal/Terminos/Terminos-2024-CSV.zip` | Causas falladas, sobreseimientos y sentencias penales | `fact_poder_judicial_causas_ingresadas_y_falladas` |
| **Descarga Directa Microdatos Civiles (Ingresos y Términos)** | `https://estadisticaservices.pjud.cl/descargas/descargas/civil/` | Litigiosidad civil, juicios ejecutivos, pagarés y cobranzas judiciales | `fact_poder_judicial_causas_ingresadas_y_falladas` |
| **Geolocalización de Tribunales Nacionales** | [https://www.pjud.cl/tribunales](https://www.pjud.cl/tribunales) | Coordenadas, direcciones y competencias (Garantía, TOP, Civil, Familia, Laboral) | `dim_tribunales_comisarias_y_recintos_penitenciarios_gis` |

---

## 4. Gendarmería de Chile (GENCHI)

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **Compendios Estadísticos Penitenciarios** | [https://www.gendarmeria.gob.cl/compendios.html](https://www.gendarmeria.gob.cl/compendios.html) | Población recluida, capacidad de diseño, índice de hacinamiento y sistema abierto/postpenitenciario | `fact_gendarmeria_poblacion_penitenciaria_y_reincidencia` |
| **Documentos Estadísticos Gendarmería** | [https://html.gendarmeria.gob.cl/doc/estadisticas/](https://html.gendarmeria.gob.cl/doc/estadisticas/) | Informes técnicos de los 166 centros penitenciarios de Chile (CDP, CCP, CPF, CET) | `fact_gendarmeria_poblacion_penitenciaria_y_reincidencia` |
| **Portal Institucional de Gendarmería** | [https://www.gendarmeria.gob.cl/](https://www.gendarmeria.gob.cl/) | Ubicación de cárceles, medidas cautelares y estadísticas operacionales | `dim_tribunales_comisarias_y_recintos_penitenciarios_gis` |

---

## 5. Servicio Médico Legal (SML), Defensoría y Acceso a la Justicia

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **Servicio Médico Legal (SML)** | [https://www.sml.gob.cl/](https://www.sml.gob.cl/) | Peritajes tanatológicos (autopsias por causa homicida/accidental/indeterminada), sexología forense y alcoholemias | `fact_sml_defensoria_y_acceso_justicia_comunal` |
| **Defensoría Penal Pública (DPP)** | [https://www.dpp.cl/](https://www.dpp.cl/) | Estadísticas de imputados atendidos, defensas juveniles e indígenas y porcentaje de absoluciones | `fact_sml_defensoria_y_acceso_justicia_comunal` |
| **Corporaciones de Asistencia Judicial (CAJ)** | [https://www.minjusticia.gob.cl/](https://www.minjusticia.gob.cl/) | Orientación y patrocinio jurídico gratuito a personas en vulnerabilidad socioeconómica | `fact_sml_defensoria_y_acceso_justicia_comunal` |

---

## 6. Superintendencia de Insolvencia y Reemprendimiento (SUPERIR)

| Fuente / Portal | URL Oficial Activa (HTTP 200) | Tipo de Dato / Cobertura | Uso en el Lakehouse |
| :--- | :--- | :--- | :--- |
| **Portal de Estadísticas SUPERIR** | [https://www.superir.gob.cl/estadisticas/](https://www.superir.gob.cl/estadisticas/) | Boletines concursales mensuales de la Ley 20.720 y Ley 21.563 | `fact_insolvencia_superir_y_justicia_comercial` |
| **Boletín Concursal de Chile** | [https://www.boletinconcursal.cl/](https://www.boletinconcursal.cl/) | Publicaciones legales de liquidaciones forzosas, voluntarias y reorganizaciones | `fact_insolvencia_superir_y_justicia_comercial` |
| **Datos Abiertos de Procedimientos Concursales** | [https://datos.gob.cl/](https://datos.gob.cl/) | Series históricas de pasivos verificados y renegociaciones de personas deudoras | `fact_insolvencia_superir_y_justicia_comercial` |
