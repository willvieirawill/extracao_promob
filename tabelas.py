
from sqlalchemy import Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, MetaData, Float, Integer,ForeignKey,DateTime, Boolean, String, Column
from datetime import datetime


from config import mssq_datawharehouse

engine = mssq_datawharehouse()
metadata = MetaData()
metadata_obj = MetaData(schema="logistica")



dim_pedidos_promob = Table(
"dim_pedidos_promob",
metadata,
Column('cod_pedido',Integer, primary_key=True),
Column('ref_pedido',String),
Column('Nomes',String),
Column('quantidadesolicitada',Integer),
Column('quantidadefaturada',Integer),
Column('quantidadeemaberto',Integer),
Column('valorunitario',Float),
Column('valorprodutos',Float),
Column('referenciaprodutos',String),
Column('unidade',String),
Column('ncm',String),
Column('urls',String),
Column('lote_pedidos',String),
Column('status_pedidos',String),
Column('tipo_pedidos',String),
Column('totais',Float),
Column('datas_entrega',DateTime),
Column('datas',DateTime),
Column('cliente_pedidos',Integer),
Column('pedido_oc',String),
Column('referencias_pedidos',Integer),
schema="logistica",extend_existing=True)

       

 