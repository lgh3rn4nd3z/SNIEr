-- ============================================
-- Script para insertar datos dummy en PLADESHI
-- ============================================

-- 1. Insertar nuevo cuadro
INSERT INTO PLADESHI.Cuadros (Descripcion)
VALUES ('Proyeccion de Consumo de Gas Natural 2025-2040');

-- Obtener el ID del cuadro insertado (usar en los siguientes inserts)
-- DECLARE @CuadroId INT = SCOPE_IDENTITY();

-- 2. Insertar series dummy
INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Consumo Industrial', 1250, 1320, 1410, 1505, 1620, 1750, 1890, 2050, 2230, 2420, 2630, 2860, 3100, 3360, 3640, 3950);

INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Consumo Residencial', 450, 475, 502, 530, 560, 592, 626, 662, 700, 740, 782, 826, 873, 922, 974, 1030);

INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Consumo Comercial', 320, 338, 357, 377, 398, 421, 445, 470, 497, 525, 555, 587, 620, 655, 692, 732);

-- 3. Relacionar series con el cuadro
-- NOTA: Reemplaza @CuadroId y @SerieId con los IDs reales despues de ejecutar los INSERTs anteriores
-- Puedes verificar los IDs con: SELECT * FROM PLADESHI.Cuadros; SELECT * FROM PLADESHI.Serie;

-- Ejemplo (ajusta los IDs segun corresponda):
-- INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId1);
-- INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId2);
-- INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId3);

-- 4. Insertar metadatos para las series
-- NOTA: Reemplaza @SerieId1, @SerieId2, @SerieId3 con los IDs reales

-- Metadatos para Serie 1 (Consumo Industrial)
-- INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Area Tecnica Responsable', 'Direccion de Planeacion Energetica');
-- INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Fuente de Informacion', 'SENER - Sistema de Informacion Energetica');
-- INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Fecha y hora de descarga', '2024-01-15 10:30:00');
-- INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Nota', 'Datos proyectados basados en escenario de crecimiento moderado');

-- ============================================
-- VERSION CON VARIABLES (ejecutar en bloque)
-- ============================================

DECLARE @CuadroId INT;
DECLARE @SerieId1 INT;
DECLARE @SerieId2 INT;
DECLARE @SerieId3 INT;

-- Insertar cuadro
INSERT INTO PLADESHI.Cuadros (Descripcion)
VALUES ('Proyeccion de Demanda Electrica 2025-2040');
SET @CuadroId = SCOPE_IDENTITY();

-- Insertar series
INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Demanda Sector Industrial', 2100, 2205, 2315, 2431, 2553, 2680, 2814, 2955, 3103, 3258, 3421, 3592, 3771, 3960, 4158, 4366);
SET @SerieId1 = SCOPE_IDENTITY();

INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Demanda Sector Residencial', 890, 925, 962, 1000, 1040, 1082, 1125, 1170, 1217, 1265, 1316, 1369, 1423, 1480, 1539, 1601);
SET @SerieId2 = SCOPE_IDENTITY();

INSERT INTO PLADESHI.Serie (MMPCD, [2025], [2026], [2027], [2028], [2029], [2030], [2031], [2032], [2033], [2034], [2035], [2036], [2037], [2038], [2039], [2040])
VALUES ('Demanda Sector Servicios', 650, 676, 703, 731, 760, 791, 822, 855, 889, 925, 962, 1000, 1040, 1082, 1125, 1170);
SET @SerieId3 = SCOPE_IDENTITY();

-- Relacionar con cuadro
INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId1);
INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId2);
INSERT INTO PLADESHI.CuadroSerie (CuadrosId, SerieId) VALUES (@CuadroId, @SerieId3);

-- Metadatos para Serie 1
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Area Tecnica Responsable', 'Direccion de Planeacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Fuente de Informacion', 'SENER - Sistema de Informacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Fecha y hora de descarga', '2024-01-15 10:30:00');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId1, 'Nota', 'Datos proyectados basados en escenario de crecimiento moderado');

-- Metadatos para Serie 2
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId2, 'Area Tecnica Responsable', 'Direccion de Planeacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId2, 'Fuente de Informacion', 'SENER - Sistema de Informacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId2, 'Fecha y hora de descarga', '2024-01-15 10:30:00');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId2, 'Nota', 'Proyeccion basada en crecimiento poblacional estimado');

-- Metadatos para Serie 3
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId3, 'Area Tecnica Responsable', 'Direccion de Planeacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId3, 'Fuente de Informacion', 'SENER - Sistema de Informacion Energetica');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId3, 'Fecha y hora de descarga', '2024-01-15 10:30:00');
INSERT INTO PLADESHI.Metadatos (SerieId, Campo, Valor) VALUES (@SerieId3, 'Nota', 'Incluye comercio, hoteles y servicios publicos');

PRINT 'Datos insertados correctamente!';
PRINT 'Cuadro ID: ' + CAST(@CuadroId AS VARCHAR);
PRINT 'Series IDs: ' + CAST(@SerieId1 AS VARCHAR) + ', ' + CAST(@SerieId2 AS VARCHAR) + ', ' + CAST(@SerieId3 AS VARCHAR);
