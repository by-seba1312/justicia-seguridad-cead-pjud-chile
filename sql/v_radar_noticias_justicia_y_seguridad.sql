-- ==============================================================================
-- Vista Gold: v_radar_noticias_justicia_y_seguridad
-- Proyecto: Data Lakehouse Nacional de Chile (southamerica-west1)
-- Sector: Justicia, Persecución Penal y Seguridad Pública
-- ==============================================================================

CREATE OR REPLACE VIEW `project-0ab8074c-14aa-434e-849.gold_nacional.v_radar_noticias_justicia_y_seguridad` AS
WITH noticias_dedup AS (
  SELECT
    noticia_id,
    medio,
    categoria,
    titular,
    resumen,
    url_noticia,
    fecha_publicacion,
    fecha_ingesta,
    tags_sectoriales,
    score_sentimiento_estimado,
    ROW_NUMBER() OVER(PARTITION BY noticia_id ORDER BY fecha_ingesta DESC) AS rn
  FROM `project-0ab8074c-14aa-434e-849.core_hacienda_macro.fact_noticias_mercados_chile`
),
macro_hoy AS (
  SELECT
    valor_uf,
    dolar_observado,
    euro,
    tpm_pct,
    precio_cobre_usd_lb,
    COALESCE(petroleo_wti_usd, 70.0) AS petroleo_wti_usd
  FROM `project-0ab8074c-14aa-434e-849.core_hacienda_macro.dim_calendario_financiero`
  WHERE valor_uf IS NOT NULL
  ORDER BY fecha DESC
  LIMIT 1
)
SELECT
  n.noticia_id,
  n.fecha_publicacion,
  n.medio,
  n.categoria,
  n.titular,
  n.resumen,
  n.url_noticia,
  n.tags_sectoriales,
  n.score_sentimiento_estimado,
  CASE
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'FISCALIA|FISCALÍA|MINISTERIO PUBLICO|MINISTERIO PÚBLICO|FORMALIZ|PRISION PREVENTIVA|PRISIÓN PREVENTIVA') THEN 'PERSECUCION_PENAL_Y_FISCALIA'
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'CORTE SUPREMA|CORTE DE APELACIONES|PODER JUDICIAL|TRIBUNAL|JUEZ|SENTENCIA|FALLO') THEN 'PODER_JUDICIAL_Y_JURISPRUDENCIA'
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'CARABINEROS|PDI|DELINCUENCIA|HOMICIDIO|ROBO|CRIMEN ORGANIZADO|PORTONAZO|ENCERRONA') THEN 'SEGURIDAD_CIUDADANA_Y_POLICIAS'
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'GENDARMERIA|GENDARMERÍA|CARCEL|CÁRCEL|PENITENCIARI') THEN 'SISTEMA_PENITENCIARIO_GENDARMERIA'
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'CONTRALORIA|CONTRALORÍA|PROBIDAD|SUMARIO|MUNICIPAL') THEN 'CONTRALORIA_Y_PROBIDAD_PUBLICA'
    WHEN REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))), r'QUIEBRA|INSOLVENCIA|REORGANIZACION|REORGANIZACIÓN|LIQUIDACION|LIQUIDACIÓN|SUPERIR|DELITO ECONOMICO|DELITO ECONÓMICO') THEN 'INSOLVENCIA_Y_JUSTICIA_COMERCIAL'
    ELSE 'JUSTICIA_Y_REGULACION_GENERAL'
  END AS subtema_justicia_seguridad,
  m.valor_uf AS uf_vigente,
  m.dolar_observado AS dolar_observado_vigente,
  m.tpm_pct AS tpm_pct_vigente,
  m.precio_cobre_usd_lb AS cobre_usd_lb_vigente
FROM noticias_dedup n
CROSS JOIN macro_hoy m
WHERE n.rn = 1
  AND (
    'JUSTICIA' IN UNNEST(n.tags_sectoriales)
    OR REGEXP_CONTAINS(UPPER(CONCAT(IFNULL(n.titular,''), ' ', IFNULL(n.resumen,''))),
      r'JUSTICIA|PODER JUDICIAL|CORTE SUPREMA|CORTE DE APELACIONES|FISCALIA|FISCALÍA|MINISTERIO PUBLICO|MINISTERIO PÚBLICO|GENDARMERIA|GENDARMERÍA|DELINCUENCIA|HOMICIDIO|CRIMEN ORGANIZADO|CARABINEROS|PDI|CONTRALORIA|CONTRALORÍA|TRIBUNAL|PRISION PREVENTIVA|PRISIÓN PREVENTIVA|QUIEBRA|INSOLVENCIA|SUPERIR')
  )
ORDER BY n.fecha_publicacion DESC;
