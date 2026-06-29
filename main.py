import os
import json

# Archivo de persistencia de datos actualizado a formato estructurado JSON
A = "datos_inv.json"

def p_pro(op, x, p, c, t, cod_barras=""):
    """
    Función de inventario actualizada.
    Soporta formato JSON, código de barras y reglas de negocio dinámicas.
    """
    # Cargar datos existentes desde el archivo JSON si existe
    inventario = []
    if os.path.exists(A):
        with open(A, "r", encoding="utf-8") as f:
            try:
                inventario = json.load(f)
            except json.JSONDecodeError:
                inventario = []

    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        # El código de barras ahora es un campo obligatorio para nuevos registros
        if x == "" or p <= 0 or c < 0 or cod_barras == "":
            print("Error: Datos inválidos o falta el código de barras.")
            return False
        
        # REQUERIMIENTO FINANCIERO: IVA del 12% para Tecnología, 15% para el resto
        if t == "Tecnología":
            iva = p * 0.12
        else:
            iva = p * 0.15
            
        total_con_iva = p + iva
        
        # Lógica de descuento por categoría
        if t == "Tecnología":
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        # Estructura de diccionario limpio para JSON
        nuevo_producto = {
            "codigo_barras": cod_barras,
            "producto": x,
            "precio": p,
            "stock": c,
            "categoria": t,
            "precio_final": p_final
        }
        
        inventario.append(nuevo_producto)
        
        # Escritura estructurada en formato JSON
        with open(A, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=4, ensure_ascii=False)
        print(f"Producto '{x}' guardado con éxito en JSON.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        if not inventario:
            print("No hay datos registrados.")
            return
            
        print("---------------------------------------------------------------------------")
        print("COD BARRAS   | PROD       | PRECIO  | STOCK   | CAT         | PRECIO FINAL")
        print("---------------------------------------------------------------------------")
        for prod in inventario:
            cod1 = prod["codigo_barras"]
            x1 = prod["producto"]
            p1 = prod["precio"]
            c1 = prod["stock"]
            t1 = prod["categoria"]
            pf1 = prod["precio_final"]
            
            print(f"{cod1:<12} | {x1:<10} | ${p1:<6.2f} | {c1:<7} | {t1:<11} | ${pf1:<10.2f}")
            
            # REQUERIMIENTO CONTROL DE CALIDAD: Alerta si el stock es menor a 5 unidades
            if c1 < 5:
                print(f"   ⚠️  [ALERTA CRÍTICA] El producto '{x1}' tiene stock bajo: solo {c1} unidades.")
        print("---------------------------------------------------------------------------")

    elif op == 3:
        # SIMULACIÓN DE REPORTES (Recalculo dinámico del IVA basado en reglas vigentes)
        if not inventario:
            print("No hay datos para procesar el reporte.")
            return
        
        sumatoria = 0
        for prod in inventario:
            precio_base = prod["precio"]
            # Mantiene consistencia con la regla del 12% y 15%
            if prod["categoria"] == "Tecnología":
                iva_calculado = precio_base * 0.12
            else:
                iva_calculado = precio_base * 0.15
            sumatoria += iva_calculado
            
        print(f"Total de IVA acumulado en inventario: ${sumatoria:.2f}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO ACTUALIZADO V2.0 ---")
    
    # Limpieza previa del JSON viejo en caso de pruebas limpias
    if os.path.exists(A):
        os.remove(A)

    # Registrar productos incluyendo el código de barras requerido
    p_pro(1, "Laptop", 800.0, 4, "Tecnología", "7861001")  # Forzamos stock en 4 para ver la alerta
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles", "7861002")
    
    # Listar productos (Desplegará la tabla y evaluará la alerta de stock crítico)
    p_pro(2, "", 0, 0, "")
    
    # Ver reporte de IVA acumulado (Calculado proporcionalmente según la categoría)
    p_pro(3, "", 0, 0, "")