
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
Column('pedido',Integer),
Column('desc',String),
Column('unid',String),
Column('nat',Integer),
Column('valor_ab',Float),
Column('valor_prod',Float),
Column('valor_un',Float),
Column('quantidade_a',Float),
Column('quantidadef',Float),
Column('quantidad_s',Float),
Column('emissao',DateTime),
Column('entrega',DateTime),
Column('oc_pedido',String),
Column('urls',String),
Column('lote_pedidos',String),
Column('loja_responsavel',String),
Column('status_pedidos',String),
Column('totais',Float),
Column('datas_entrega',DateTime),
Column('datas',DateTime),
Column('cliente_pedidos',String),
Column('referencias_pedidos',Integer),
schema="logistica",extend_existing=True)

