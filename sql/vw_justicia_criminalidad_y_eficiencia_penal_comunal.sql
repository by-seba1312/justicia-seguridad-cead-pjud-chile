-- ==============================================================================
-- Vista Gold: vw_justicia_criminalidad_y_eficiencia_penal_comunal
-- Proyecto: Data Lakehouse Nacional de Chile (southamerica-west1)
-- Sector: Justicia, Persecución Penal y Seguridad Pública
-- ==============================================================================

CREATE OR REPLACE VIEW `project-0ab8074c-14aa-434e-849.gold_nacional.vw_justicia_criminalidad_y_eficiencia_penal_comunal` AS
SELECT 
  cut_comuna,
  nombre_comuna,
  nombre_region,
  poblacion_2024,
  crecimiento_intercensal_pct,
  tasa_hacinamiento_2024_pct,
  ingreso_medio_persona_esi_clp,
  tasa_desocupacion_ene_pct,
  unidades_policiales_carabineros_pdi,
  tribunales_poder_judicial,
  fiscalias_locales_mp,
  casos_policiales_totales,
  denuncias_totales,
  detenciones_flagrancia_totales,
  casos_dmcs_mayor_connotacion,
  casos_homicidios,
  casos_violencia_intrafamiliar_vif,
  tasa_dmcs_por_100k_hab,
  autopsias_homicidio_sml,
  empresas_servicios_apoyo_seguridad_sii_n,
  ventas_servicios_apoyo_seguridad_uf,
  ordenes_compra_seguridad_orden_publico,
  gasto_oc_seguridad_y_defensa_uf,
  reclamos_sernac_seguridad_privada,
  ejecucion_nacional_interior_seguridad_mm_clp,
  ejecucion_nacional_ministerio_publico_mm_clp,
  tipologia_seguridad_comunal
FROM `project-0ab8074c-14aa-434e-849.gold_nacional.v_seguridad_ciudadana_delitos_y_presion_policial_comunal`;
