import pandas as pd

clients = pd.read_excel("id_clients.xlsx",dtype={"ID клиентов": "string"})
db = pd.read_excel("data_base.xlsx", dtype={"code": "string"})

df = db.merge(
    clients,
    left_on="code",
    right_on="ID клиентов",
    how="inner",
    validate="many_to_one"
)

df = df[df["segmca"].isin(["Малые", "Микро"]) & df["period_type"].eq("M")].copy()

df["product"] = df["product"].fillna("Без продукта")

df['date_report'] = pd.to_datetime(df['date_report'])
df['month'] = df['date_report'].dt.to_period('M').astype(str)

df = (
    df.groupby(
        ["code", "pl_type", "product", "month"],
        as_index=False
    )["c_sum"]
    .sum()
)

result = pd.pivot_table(
    df,
    values="c_sum",
    index=["pl_type", "product"],
    columns="month",
    aggfunc="mean"
).reset_index()

result.columns.name = None

result.to_excel("result.xlsx", index=False)