## Como executar

Para executar esse script, é necessário realizar a instação da biblioteca da API do google, pela seguinte linha de comando:
```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Além disso, também é necessário que você instale o pandas, através da seguinte linha de comando:
```python
pip install --upgrade pandas
```

Acesse a API do google e obtenha o código secret, você pode seguir este [tutorial](https://www.hashtagtreinamentos.com/integracao-do-google-sheets-com-python)
para criar e configurar corretamente as suas credenciais de acesso à API da Google.

## Alterações de código para execução

Para configurar a planilha, configure, nas seguintes linhas de código, o ID do arquivo com suas planilhas, e o range de acesso à planilha selecionada
```python
SPREADSHEET_ID1 = 'ID DA SUA PLANILHA DE CADASTRO'
RANGE_NAME1 = 'RANGE DA SUA PLANILHA DE CADASTRO'

SPREADSHEET_ID2 = 'ID DA SUA PLANILHA DE DESTINO'
RANGE_NAME2 = 'RANGE DA SUA PLANILHA DE DESTINO'
```

Para pegar o ID da planilha, basta pegar do próprio link de acesso da mesma, da seguinte maneira:
![https://github.com/JT4v4res/Scripts-musIC/blob/main/src/imgs/exemplo_id_planilha.png.png]()
