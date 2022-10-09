<h1>Análise da discografia de artistas</h1>
> Status: Concluído

<h2>Nesse repositório você encontrará códigos para aquisição de dados da discografia de um artista (retirados do Spotify, Genius e Deezer) e para a análise exploratória dos dados, incluindo visualização de gráficos e nuvens de palavras. <h2>

<h3>Índice:</h3>
=================

   * [Sobre o projeto](#sobre)
   * [Pré Requisitos](#pre-requisitos)
   * [Como ler esse projeto?](#como-ler)
   * [Documentação](#documentacao)
   * [Nossa Equipe](#equipe)


<h3 id=sobre>Sobre o projeto:</h3>

  Esse projeto tem por finalidade criar um módulo universal para extrair dados da discografia completa de um artista e a partir dessa base de dados, realizar uma análise exploratória e utilizar ferramentas de visualização para representar visualmente os resultados da análise.


<h3 id=pre-requisitos>Pré requisitos:</h3>

1. : Instalar os requerimentos

2. : Possuir arquivos csv no formato exigido (caso não possua um arquivo csv do seu artista, use o módulo "database_module" para gerar arquivos compatíveis.)
  
⚠️ Atenção: Esse repositório analisa dados da banda "Coldplay", por esse motivo o arquivo principal referencia a pasta aonde estão contidos os csvs desse grupo. Caso você queria fazer uma análise completa de outro artista, é necessário criar um arquivo csv com a coluna "Album Name" e "Awards", contendo o nome dos álbuns e os prêmios recebidos separados por "/". Após criar os csv's, mude o path para os csv's no arquivo main.


<h3 id=como-ler>Como utilizar esse projeto?</h3>
Para entender e executar esse projeto siga as seguintes instruções:
 
- [ ] No prompt de comando do seu computador, digite o seguinte código:

```
pip install requirements.txt
```

- [ ] Gere os arquivos dos artista no seguinte arquivo: database_module/main.py . Não esqueça de atualizar as variáveis "artist_name","sp_client_id","sp_client_secret" e "ge_access_token" (caso você deseje inserir as letras na música no arquivo csv). As três últimas são geradas pelas plataformas (Spotify, Spotify e Genius, respectivamente) e possuem tempo de validade.
- [ ] Crie um arquivo csv chamado album_awards.csv que contém uma coluna chamada "Album Name" e outra chamada "Awards"elas devem conter o nome dos álbuns e os prêmios recebidos por cada álbum separados por "/". Insira esse arquivo na pasta  na pasta "results/<nome_do_seu_artista>".
- [ ] No arquivo "main.py" altere os parâmetros recebidos por "reader.is_valid" e "reader.add_awards" para o path dos arqquivos contidos na pasta de seu artista.
- [ ] Execute o main.py
  
<h3 id=documentacao>Documentação:</h3>
  Caso tenha alguma dúvida quanto a forma de utilização dos códigos, cheque nossa documentação:
  ()

  
  <h3 id=equipe>Nossa equipe:</h3>
  
  * [Almir Fonseca](https://github.com/AlmirFonseca)
  
  * [Abner Lucas](https://github.com/AbPCV)
   
  * [Lavínia Dias](https://github.com/LaviniaSD)
  
