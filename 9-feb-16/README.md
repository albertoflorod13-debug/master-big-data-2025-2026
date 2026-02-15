# Sesion Pandas + visuaización con Seaborn

Clase practica de pandas + seaborn sobre el dataset del Titanic.

## Contenido de la sesion

1. Fundamentos
2. Seleccion y filtrado
3. Limpieza de datos
4. Index
5. Groupby avanzado
6. Merge y Join
7. Performance
8. Optimizacion de memoria
9. Copy vs View
10. Limpieza de strings
11. Pipelines
12. Pivot y reshape
13. Fechas
14. Validacion
15. Window functions
16. Visualizacion avanzada
17. IO
18. Cuando NO usar pandas
19. Ejercicios


## Chuleta rapida

### Carga e inspeccion

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/titanic.csv")
df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe(include="all")
```

### Seleccion y filtrado

```python
df["Sex"]                       # Serie
df[["Name", "Sex"]]             # DataFrame
df.loc[df["Age"] >= 60]         # por condicion
df.iloc[:5, :3]                 # por posicion

df.loc[(df["Pclass"] == 3) & (df["Fare"] < 15)]
df.loc[df["Embarked"].isin(["S", "C"])]
df.loc[df["Age"].between(18, 40)]
```

### Limpieza

```python
df.isna().sum()

df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
df = df.dropna(subset=["Embarked"])
```

### Agregacion

```python
df["Pclass"].value_counts()

agg = (
    df.groupby(["Pclass", "Sex"], as_index=False)
      .agg(passengers=("PassengerId", "count"),
           survival_rate=("Survived", "mean"),
           avg_fare=("Fare", "mean"))
      .sort_values("survival_rate", ascending=False)
)
```

### Visualizacion

```python
sns.set_theme(style="whitegrid")

sns.countplot(data=df, x="Pclass")
sns.histplot(data=df, x="Age", bins=20)
sns.barplot(data=agg, x="Pclass", y="survival_rate", hue="Sex")

age_curve = (
    df.assign(age_bin=(df["Age"] // 10) * 10)
      .groupby("age_bin", as_index=False)
      .agg(survival_rate=("Survived", "mean"))
      .sort_values("age_bin")
)
sns.lineplot(data=age_curve, x="age_bin", y="survival_rate", marker="o")

plt.xticks(rotation=30)
plt.tight_layout()
```

### Errores comunes

- `and`/`or` en filtros -> usar `&`/`|` con parentesis
- `SettingWithCopyWarning` -> usar `loc[...]` o `.copy()`
- Graficos sin ordenar -> `sort_values` antes
- Fechas/numeros como texto -> `pd.to_numeric(..., errors="coerce")`
- Nulos masivos -> decidir estrategia (eliminar/imputar/transformar)
