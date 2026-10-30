"""
Genera el dataset simulado de ventas de electrodomésticos (Balay, Bosch y Siemens, 2024-2025).
Crea 4 tablas en la carpeta data/: ventas, productos, tiendas y calendario.
Uso: python generar_dataset.py
"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
out = "data/"

# Productos
cats = {  # categoria: precio base Bosch
 "Lavadoras":520,"Frigoríficos":850,"Lavavajillas":560,"Hornos":480,"Placas de inducción":420,"Secadoras":610}
brand_f = {"Balay":0.78,"Bosch":1.0,"Siemens":1.28}
margin = {"Balay":0.20,"Bosch":0.25,"Siemens":0.30}
rows=[];pid=1
for b,f in brand_f.items():
    for c,p in cats.items():
        for gama,gf in [("Básica",0.85),("Media",1.0),("Alta",1.35)]:
            pvp=round(p*f*gf*rng.uniform(0.95,1.05),-1)-1
            rows.append(dict(id_producto=f"P{pid:03d}",marca=b,categoria=c,gama=gama,
              modelo=f"{b[:3].upper()}-{c[:3].upper()}-{gama[0]}{pid:02d}",
              pvp=pvp,coste_unitario=round(pvp*(1-margin[b]-rng.uniform(-0.03,0.03)),2)))
            pid+=1
prod=pd.DataFrame(rows)

tiendas=pd.DataFrame([
 ("T01","Tienda Madrid Centro","Madrid","Comunidad de Madrid",1.35),
 ("T02","Tienda Madrid Norte","Madrid","Comunidad de Madrid",1.15),
 ("T03","Tienda Barcelona","Barcelona","Cataluña",1.25),
 ("T04","Tienda Valencia","Valencia","Comunidad Valenciana",0.95),
 ("T05","Tienda Sevilla","Sevilla","Andalucía",0.85),
 ("T06","Tienda Bilbao","Bilbao","País Vasco",0.80),
 ("T07","Online","Online","Online",1.10)],
 columns=["id_tienda","tienda","ciudad","region","peso"])

# Estacionalidad mensual
season={1:1.15,2:0.8,3:0.9,4:0.9,5:0.95,6:1.05,7:1.2,8:0.85,9:0.95,10:1.0,11:1.6,12:1.3}
cat_season={"Frigoríficos":{6:1.4,7:1.5,8:1.3},"Secadoras":{10:1.3,11:1.4,12:1.4,1:1.3}}
dates=pd.date_range("2024-01-01","2025-12-31")
w=np.array([season[d.month]*(1.08 if d.year==2025 else 1)*(0.7 if d.dayofweek==6 else 1.25 if d.dayofweek==5 else 1) for d in dates])
N=10000
fechas=rng.choice(dates,N,p=w/w.sum())
tw=tiendas.peso.values; tsel=rng.choice(tiendas.id_tienda,N,p=tw/tw.sum())
bw={"Balay":0.40,"Bosch":0.38,"Siemens":0.22}
ventas=[]
for i,(fe,t) in enumerate(zip(fechas,tsel)):
    fe=pd.Timestamp(fe)
    b=rng.choice(list(bw),p=list(bw.values()))
    cw=np.array([cat_season.get(c,{}).get(fe.month,1)*(1.3 if c in("Lavadoras","Frigoríficos") else 1) for c in cats])
    c=rng.choice(list(cats),p=cw/cw.sum())
    g=rng.choice(["Básica","Media","Alta"],p=[0.4,0.4,0.2])
    p=prod[(prod.marca==b)&(prod.categoria==c)&(prod.gama==g)].iloc[0]
    bf = fe.month==11 and fe.day>=20
    rebajas = fe.month in (1,7)
    desc = rng.choice([0.15,0.20,0.25]) if bf else rng.choice([0.10,0.15]) if rebajas else rng.choice([0,0,0,0.05,0.10])
    uds = 1 if rng.random()<0.94 else 2
    ventas.append(dict(id_venta=f"V{i+1:05d}",fecha=fe.date(),id_tienda=t,id_producto=p.id_producto,
      id_vendedor=f"{t}-{rng.integers(1,6):02d}" if t!="T07" else "ONLINE",
      unidades=uds,pvp_unitario=p.pvp,descuento_pct=desc,
      importe_neto=round(p.pvp*uds*(1-desc),2),
      garantia_extendida="Sí" if (t!="T07" and rng.random()<0.28) or rng.random()<0.08 else "No",
      instalacion="Sí" if c in("Hornos","Placas de inducción","Lavavajillas") and rng.random()<0.6 else "No",
      devolucion="Sí" if rng.random()<0.03 else "No"))
v=pd.DataFrame(ventas).sort_values("fecha").reset_index(drop=True)
v["id_venta"]=[f"V{i+1:05d}" for i in range(len(v))]
v.to_csv(out+"ventas.csv",index=False,encoding="utf-8")
prod.to_csv(out+"productos.csv",index=False,encoding="utf-8")
tiendas.drop(columns="peso").to_csv(out+"tiendas.csv",index=False,encoding="utf-8")

# Tabla calendario
cal = pd.DataFrame({"fecha": pd.date_range("2024-01-01", "2025-12-31")})
meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
cal["anio"] = cal.fecha.dt.year
cal["mes_num"] = cal.fecha.dt.month
cal["mes"] = [f"{x:02d}-{meses[x-1]}" for x in cal.mes_num]
cal["anio_mes"] = cal.fecha.dt.strftime("%Y-%m")
cal["trimestre"] = "T" + cal.fecha.dt.quarter.astype(str)
cal["fecha"] = cal.fecha.dt.strftime("%Y-%m-%d")
cal.to_csv(out + "calendario.csv", index=False, encoding="utf-8")
print("Dataset generado en", out)
