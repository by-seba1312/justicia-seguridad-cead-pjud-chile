-- ==============================================================================
-- Vista Gold: vw_justicia_insolvencia_y_carga_judicial_regional
-- Proyecto: Data Lakehouse Nacional de Chile (southamerica-west1)
-- Sector: Justicia, Persecución Penal y Seguridad Pública
-- ==============================================================================

CREATE OR REPLACE VIEW `project-0ab8074c-14aa-434e-849.gold_nacional.vw_justicia_insolvencia_y_carga_judicial_regional` AS
SELECT 
  nombre_region,
  COUNT(DISTINCT cut_comuna) AS total_comunas,
  SUM(poblacion_2024) AS poblacion_regional_2024,
  ROUND(AVG(ingreso_medio_persona_esi_clp), 0) AS ingreso_medio_persona_promedio_clp,
  SUM(pjud_causas_ingresadas_totales) AS pjud_causas_ingresadas_totales,
  SUM(pjud_causas_falladas_totales) AS pjud_causas_falladas_totales,
  ROUND(SAFE_DIVIDE(SUM(pjud_causas_falladas_totales) * 100.0, NULLIF(SUM(pjud_causas_ingresadas_totales), 0)), 2) AS tasa_resolucion_judicial_pct,
  SUM(pjud_causas_civiles_y_cobranza) AS pjud_causas_civiles_y_cobranza,
  SUM(pjud_causas_familia) AS pjud_causas_familia,
  SUM(pjud_causas_laborales) AS pjud_causas_laborales,
  SUM(mp_delitos_ingresados) AS mp_delitos_ingresados,
  SUM(mp_sentencias_condenatorias) AS mp_sentencias_condenatorias,
  SUM(mp_archivos_provisionales) AS mp_archivos_provisionales,
  SUM(genchi_poblacion_penal_recluida) AS genchi_poblacion_penal_recluida,
  SUM(genchi_imputados_prision_preventiva) AS genchi_imputados_prision_preventiva,
  ROUND(AVG(NULLIF(genchi_indice_hacinamiento_pct, 0.0)), 2) AS genchi_indice_hacinamiento_promedio_pct,
  SUM(superir_quiebras_y_reorganizaciones_empresas) AS superir_quiebras_y_reorganizaciones_empresas,
  SUM(superir_liquidaciones_y_renegociaciones_personas) AS superir_liquidaciones_y_renegociaciones_personas,
  ROUND(SUM(superir_pasivo_concursal_uf), 2) AS superir_pasivo_concursal_uf,
  SUM(empresas_juridicas_profesionales_sii_m) AS empresas_juridicas_profesionales_sii_m,
  ROUND(SUM(ventas_juridicas_profesionales_uf), 2) AS ventas_juridicas_profesionales_uf,
  SUM(reclamos_sernac_financieros_cobranza) AS reclamos_sernac_financieros_cobranza,
  MAX(ejecucion_nacional_poder_judicial_mm_clp) AS ejecucion_nacional_poder_judicial_mm_clp,
  MAX(ejecucion_nacional_min_justicia_mm_clp) AS ejecucion_nacional_min_justicia_mm_clp
FROM `project-0ab8074c-14aa-434e-849.gold_nacional.v_carga_jurisdiccional_penitenciaria_e_insolvencia_comunal`
GROUP BY nombre_region
ORDER BY poblacion_regional_2024 DESC;
