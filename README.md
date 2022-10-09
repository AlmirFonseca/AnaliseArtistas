<h1>Análise da discografia de artistas</h1>
> Status: Concluído

<h2>Nesse repositório você encontrará códigos para aquisição de dados da discografia do Coldplay (retirados do Spotify, Genius e Deezer) e para a análise exploratória dos dados, incluindo visualização de gráficos e nuvens de palavras. <h2>

<h3>Índice:</h3>
=================

   * [Sobre o projeto](#sobre)
   * [Pré Requisitos](#pre-requisitos)
   * [Como ler esse projeto?](#como-ler)
   * [Documentação](#documentacao)
   * [Nossa Equipe](#equipe)


<h3 id=sobre>Sobre o projeto:</h3>

  Esse projeto tem por finalidade criar uma base de dados da discografia completa da banda "Coldplay"e a partir dessa base de dados, realizar uma análise exploratória e utilizar ferramentas de visualização para representar visualmente os resultados da análise.


<h3 id=pre-requisitos>Pré requisitos:</h3>

1. : Instalar os requerimentos

2. : Possuir os arquivos csv no formato exigido
  

<h3 id=como-ler>Como utilizar esse projeto?</h3>
Para entender e executar esse projeto siga as seguintes instruções:
 
- [ ] Certifique-se que esse repositório está em sua máquina e o acesse:


- [ ] No prompt de comando do seu computador, digite o seguinte código:

```
pip install -r requirements.txt
```

- [ ] Caso queira gerar novamente o arquivo csv da discografia do artista, acesse o seguinte arquivo: database_module/main.py . Não esqueça de atualizar as variáveis,"sp_client_id","sp_client_secret" e "ge_access_token" (caso você deseje inserir as letras na música no arquivo csv). As informações contidas nessas variáveis são geradas pelas plataformas (as duas primeiras pelo Spotify e a última pelo Genius) e possuem tempo de validade.
- [ ] Caso queira as informações sobre os prêmios dos álbuns mais atualizadas, atualize o arquivo csv chamado album_awards.csv contido na pasta "results/COLDPLAY" com o nome dos álbuns na coluna "Album Name" e os seus respectivos prêmios na coluna "Awards", os prêmios recebidos por cada álbum devem ser separados por "/". 
- [ ] Execute o main.py
  
<h3 id=documentacao>Documentação:</h3>
  Caso tenha alguma dúvida quanto a forma de utilização dos códigos, cheque nossa documentação (https://almirfonseca.github.io/AnaliseArtistas/) ou vá no branch gh-pages e siga as orientações no README.md para a documentação mais acessível e estilizada.

  
  <h3 id=equipe>Nossa equipe:</h3>
  
  * [Almir Fonseca](https://github.com/AlmirFonseca)
  
  * [Abner Lucas](https://github.com/AbPCV)
   
  * [Lavínia Dias](https://github.com/LaviniaSD)
  
