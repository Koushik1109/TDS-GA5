import duckdb
print(duckdb.__version__)
try:
    print(duckdb.sql("SELECT try_strptime('2024-01-01', '%Y-%m-%d')"))
except Exception as e:
    print("try_strptime error:", e)

try:
    print(duckdb.sql("SELECT try_cast('2024-01-01' AS DATE)"))
except Exception as e:
    print("try_cast error:", e)
