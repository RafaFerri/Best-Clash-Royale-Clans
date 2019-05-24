
# Projeto similar ao descrito no Notebook, porém com mais volumes de dados e 
# rodado em Spark, instalado localmente. Executado com pyspark.

# Tempo estimado: 29 segundos com 200.000 matches / 400.000 hitóricos

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions as f
from pyspark.sql.types import IntegerType

def converte_coluna(df, col):
    df = df.withColumn(col, df[col].cast(IntegerType()))
    return df

if __name__ == "__main__":
    # Criando um SparkSession e importando a base de dados
    spark = SparkSession.builder.appName("Matches").getOrCreate()
    matches = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/Users/rafaelferri/Arquivos/Clash/PartidasClash200k.csv")
    
    #Editando o tipo das informações nas colunas
    matches = converte_coluna(matches, "Trophy")
    matches = converte_coluna(matches, "Crowns Won")
    matches = converte_coluna(matches, "Crowns Lost")
    matches = converte_coluna(matches, "Result")
       
    #Encontrando os melhores clãs pelo critério de acima de 10 vitórias e ordenado por % de Vitória
    ClasVitorias = matches.groupBy("Clan").sum("Result").orderBy("sum(Result)", ascending=False)
    ClasContagem = matches.groupby("Clan").count().orderBy("count", ascending=False)
    MelhoresClas = ClasVitorias.join(ClasContagem, "Clan")
    
    MelhoresClas = converte_coluna(MelhoresClas, "sum(Result)")
    MelhoresClas = converte_coluna(MelhoresClas, "count")
    MelhoresClas = MelhoresClas.withColumn("PercVitoria", f.round(MelhoresClas["sum(Result)"]/MelhoresClas["count"]*100, 1))
    
    TopMelhoresClas = MelhoresClas.filter(MelhoresClas["sum(Result)"] > 450)
    TopMelhoresClas = TopMelhoresClas.orderBy("PercVitoria", ascending=False)
    
    print(TopMelhoresClas.show())
    
    spark.stop()