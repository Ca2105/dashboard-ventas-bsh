# 📐 Medidas DAX del modelo

Todas las medidas están en la tabla `ventas`. Una medida no guarda un valor fijo: se recalcula según los filtros activos (año, marca, tienda…).

| # | Medida | Fórmula | Qué responde |
|---|---|---|---|
| 1 | **Ventas netas** | `SUM(ventas[importe_neto])` | Total facturado, con los descuentos ya aplicados |
| 2 | **Nº ventas** | `COUNTROWS(ventas)` | Número de operaciones |
| 3 | **Coste total** | `SUMX(ventas, ventas[unidades] * RELATED(productos[coste_unitario]))` | Coste de la mercancía vendida. `SUMX` recorre cada venta y `RELATED` trae el coste desde `productos` a través de la relación |
| 4 | **Margen €** | `[Ventas netas] - [Coste total]` | Beneficio bruto en euros |
| 5 | **Margen %** | `DIVIDE([Margen €], [Ventas netas])` | Qué parte de cada euro vendido es beneficio. `DIVIDE` evita errores si el divisor es 0 |
| 6 | **Ticket medio** | `DIVIDE([Ventas netas], [Nº ventas])` | Gasto medio por compra |
| 7 | **% Garantía extendida** | `DIVIDE(CALCULATE(COUNTROWS(ventas), ventas[garantia_extendida] = "Sí"), [Nº ventas])` | Porcentaje de ventas que incluyen garantía. `CALCULATE` aplica el filtro |
| 8 | **% Devoluciones** | `DIVIDE(CALCULATE(COUNTROWS(ventas), ventas[devolucion] = "Sí"), [Nº ventas])` | Porcentaje de ventas devueltas |
| 9 | **Ventas 2024** | `CALCULATE([Ventas netas], YEAR(ventas[fecha]) = 2024)` | Ventas netas solo de 2024 |
| 10 | **Ventas 2025** | `CALCULATE([Ventas netas], YEAR(ventas[fecha]) = 2025)` | Ventas netas solo de 2025 |
| 11 | **Crecimiento %** | `DIVIDE([Ventas 2025] - [Ventas 2024], [Ventas 2024])` | Crecimiento interanual |

## Funciones clave

- **`SUMX`**: itera fila a fila y suma el resultado de una expresión.
- **`RELATED`**: trae un valor de una tabla relacionada (lado "uno" de la relación).
- **`CALCULATE`**: evalúa una expresión modificando el contexto de filtro. Es la función más importante de DAX.
- **`DIVIDE`**: división segura que devuelve vacío en lugar de error si el divisor es 0.
