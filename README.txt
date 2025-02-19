Requisitos
Antes de rodar o projeto, você precisará configurar uma variável de ambiente que contém a chave de acesso ao MongoDB. O projeto utiliza o MongoDB Atlas (banco de dados na nuvem) para armazenar informações, e a chave de conexão é essencial para que o jogo se comunique com o banco.

Passos para Configurar
1- Criar uma Conta no MongoDB Atlas

Se você ainda não tem uma conta no MongoDB Atlas, crie uma gratuitamente em https://www.mongodb.com/cloud/atlas.
Após criar sua conta, crie um cluster (banco de dados na nuvem) e um usuário para acessar o banco de dados.
Obter a Chave de Conexão

Dentro do painel do MongoDB Atlas, vá até o cluster que você criou e clique em Connect.
Selecione Connect your application e copie a string de conexão. A string estará no formato:
mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
Substitua <username>, <password>, e <dbname> com as credenciais do seu banco de dados.

2- Criar o Arquivo .env

Na raiz do projeto, crie um arquivo chamado .env e adicione a variável de ambiente MONGO_URI com o valor da string de conexão do MongoDB Atlas. O arquivo .env deve ficar assim:
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"

Não adicione seu arquivo .env no GitHub. Ele deve ser mantido localmente para garantir que a chave de acesso não seja compartilhada. O arquivo .env está configurado para ser ignorado no .gitignore.