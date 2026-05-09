# Barbarians at the Gate: How AI is Upending Systems Research, Notas e conceitos importantes do documento


Uma das principais razões pelas quais problemas de system performance são adequados para AI-Driven Research (AIDR) é o facto de as soluções geradas serem relativamente fáceis de testar. O modelo pode gerar múltiplas soluções e estas podem ser validadas empiricamente, permitindo verificar quais efetivamente resolvem o problema.

Dito isto, um dos pontos fulcrais do uso de AIDR é, sem dúvida, a validação da precisão das soluções geradas.

Contudo, essa validação nem sempre é trivial. Nem sempre é fácil verificar se um programa gerado por IA está correto, se resolve efetivamente o problema ou até mesmo se responde adequadamente a questões aparentemente simples.

Felizmente, este não é o caso dos problemas de performance de sistemas. Estes são implementados diretamente em artefactos concretos, como bases de dados, sistemas operativos e redes. Assim, basta executar o sistema onde a solução é integrada e medir a sua eficiência através de workloads específicos, avaliando empiricamente a sua performance.

Para evitar overhead e riscos associados a sistemas reais, são frequentemente utilizados simuladores que capturam a essência fundamental desses sistemas. Estes permitem iteração rápida e a baixo custo, possibilitando validação preliminar antes da implementação em ambientes reais. Isso torna systems research particularmente adequado para AI-driven exploration.

## Âmbito de AI-Driven Research

No contexto geral de AI-driven research, o foco apresentado no artigo é relativamente estreito: concentra-se exclusivamente no domínio dos sistemas, nomeadamente no desenvolvimento de soluções, ignorando outros aspetos importantes do processo científico, como:

- Formulação de problemas

- Revisão de literatura

- Escrita científica

Seguir esta abordagem apresenta várias vantagens:

- Redução de alucinações, uma vez que a avaliação é essencialmente empírica (medição de performance).

- Permite aprofundar um domínio específico, desenvolvendo soluções mais eficientes, em vez de dispersar esforços por múltiplas áreas.

- O desenvolvimento de soluções mais eficientes contribui indiretamente para o avanço de outras áreas, ao fornecer melhores infraestruturas.

## Consequências do AI-Driven Research 

Tendo em conta este foco, é importante refletir sobre as suas consequências. Uma das principais é a mudança no papel dos investigadores humanos.

Idealmente, os investigadores deixam de estar focados na implementação direta das soluções e passam a concentrar-se em:

- Formulação de problemas

- Identação de alto nível

- Definição de direção estratégica

Nesse contexto, o investigador assume um papel mais próximo de conselheiro ou orientador da IA, supervisionando e guiando o desenvolvimento das soluções mais eficientes para um determinado problema


# Funcionamento

![Arquitetura do Sistema](../images/ADRS.png)
* Figure 1: The AI-driven Research for Systems (ADRS) architecture shown in the context of the systems research process. ADRS (grey area) automates the Solution and Evaluation
stages

##
Responsabilidades de cada bloco:

- Prompt Generator:
Cria o prompt utilizado para gerar a solução. Este prompt consiste na descrição do problema e no contexto fornecido pelo investigador, que pode incluir código do sistema ou do simulador. O prompt pode também incluir soluções anteriores e as respetivas avaliações (fornecidas pelo Solution Selector), com o objetivo de o refinar e melhorar a geração de novas soluções.

- Solution Generator :
Recebe o prompt do Prompt Generator e envia-o para um ou mais LLMs, de modo a gerar uma nova solução ou a refinar uma solução existente. Normalmente, isto é feito através da atualização direta do código no simulador ou no sistema real.

- Evaluator :
Recebe a solução do Solution Generator e executa-a sobre um conjunto predefinido de workloads (traces). Em seguida, atribui uma pontuação com base na performance obtida na execução e pode utilizar um LLM para fornecer feedback qualitativo. Caso a pontuação atinja um valor suficientemente elevado, o ciclo é terminado.

- Storage:
Armazena as soluções geradas, os seus resultados, as pontuações atribuídas e o feedback fornecido pelo componente Evaluator.

- Solution Selector:
Seleciona um subconjunto de soluções armazenadas em Storage e fornece-as ao Prompt Generator, com o objetivo de refinar o prompt e gerar soluções novas e melhoradas.   

# Prompt Generator

## Formulação Clara do Problema

Uma evolução algorítmica eficaz começa com uma especificação clara e bem delimitada.

O prompt deve definir explicitamente:

- **O problema** – qual é a tarefa principal.
- **Critérios de avaliação** – como a solução será avaliada (correção, otimização, restrições).
- **Contexto** – APIs necessárias, código existente e informação técnica relevante.

Prompts mal estruturados levam a falhas de execução e desperdício de iterações.

---

## Escolha do Programa Base

O baseline influencia diretamente a trajetória da evolução:

- Baselines fracos → desperdício de iterações em correções triviais.
- Baselines muito fortes → limitam a exploração a micro-otimizações.
- Baselines simples, limpos e de qualidade → favorecem melhorias significativas.

**Recomendação:** utilizar um baseline mínimo, funcional e bem estruturado.

---

## Fornecimento de Dicas (Solution Hints)

Hints podem:

- Acelerar a convergência.
- Evitar iterações inúteis.

Mas também podem:

- Induzir convergência prematura.
- Limitar a descoberta de soluções inovadoras.

**Recomendação:** testar diferentes níveis de orientação e introduzir feedback humano quando a busca ficar estagnada.

---

## Nível Adequado de Abstração

O nível de acesso às APIs deve alinhar-se com o objetivo:

- Para promover inovação algorítmica → restringir APIs de alto nível.
- Para otimização de execução → permitir bibliotecas altamente otimizadas.

O equilíbrio adequado evita micro-otimizações superficiais.

---

# Solution Generator

## Uso de Ensemble de Modelos

Falhas na busca ocorrem quando existe:

- Exploração excessiva.
- Exploração insuficiente.

**Recomendação:**

Utilizar dois modelos com papéis complementares:

- Modelo de raciocínio → promove exploração e geração de ideias criativas.
- Modelo mais eficiente → refina e otimiza soluções existentes.

O uso de mais de dois modelos pode introduzir instabilidade e conflito de ideias.

---

# Evaluator

## Prevenção de Overfitting

Avaliar com workloads limitados pode gerar soluções que:

- Codificam comportamentos específicos.
- Não generalizam para novos cenários.

**Recomendação:**

- Utilizar conjuntos de teste diversos.
- Incluir edge cases.
- Avaliar robustez em diferentes padrões de execução.

---

## Prevenção de Reward Hacking

Reward hacking ocorre quando a solução explora falhas do avaliador sem resolver o problema real.

**Recomendação:**

Combinar múltiplos sinais de avaliação:

- Correção
- Eficiência
- Robustez

Incluir testes adversariais para impedir exploração indevida do sistema de avaliação.

Objetivo: garantir alinhamento com os requisitos reais do problema.

---

# Solution Selector

## Equilíbrio Entre Exploração e Exploração

A retenção de soluções entre iterações influencia fortemente o resultado final.

- Seletores greedy → convergência rápida, risco de convergência prematura.
- Seletores excessivamente aleatórios → desperdício de recursos.
- Seletores equilibrados → mantêm diversidade e promovem qualidade progressiva.

O rácio exploração/exploração é um parâmetro crítico e deve ser ajustado cuidadosamente para evitar falhas na busca.

# Quando o ADRS Funciona Melhor

Com base na experiência inicial, o ADRS é mais eficaz em problemas que:

- Exigem alterações localizadas.
- São rápidos de avaliar.
- Possuem critérios de verificação claros e confiáveis.

É menos eficaz em problemas que:

- Exigem alterações distribuídas por múltiplos sistemas.
- Dependem de verificadores fracos.
- Envolvem avaliações dispendiosas ou demoradas.

Compreender estes limites permite aplicar ADRS onde tem maior probabilidade de sucesso.

---

# Propriedades Ideais para ADRS

## Alterações Isoladas

Modelos atuais são mais fiáveis quando modificam pequenas partes do código.

ADRS é mais adequado para melhorar componentes isolados como:

- Schedulers
- Gestores de cache
- Load balancers
- Alocadores de recursos

Não é adequado para:

- Protocolos distribuídos complexos
- Sistemas com forte interdependência entre componentes
- Protocolos de consenso que envolvem gestão de estado, comunicação em rede e deteção de falhas

Nestes casos, a complexidade sistémica reduz a eficácia da evolução automática.

---

## Avaliações Confiáveis

Deve ser fácil:

- Determinar qual solução é melhor.
- Verificar equivalência semântica entre soluções.

Exemplo favorável:
- Melhorar um load balancer → mede-se facilmente o fator de desequilíbrio.
- Duas soluções são equivalentes se encaminharem pedidos para réplicas do mesmo serviço.

Exemplo problemático:
- Modificar planos de execução de queries.
- Provar equivalência semântica geral pode ser impossível.
- Apenas certas transformações garantem preservação semântica.

A clareza na verificação é essencial para evitar soluções incorretas.

---

## Avaliações Eficientes

A avaliação deve ser:

- Rápida
- Financeiramente viável

ADRS pode exigir centenas ou milhares de iterações.

Se cada avaliação:

- Demorar muitas horas
- Custar centenas de euros

O processo torna-se impraticável (meses ou anos de execução).

Exemplos de cenários problemáticos:

- Workloads intensivos em GPU
- Compressão de pesos com ciclos longos
- Treino distribuído em larga escala

Eficiência na avaliação é um fator crítico de viabilidade.

---

# Limitações Fundamentais

ADRS não é a melhor abordagem para problemas que:

- Podem ser formulados diretamente como problemas de otimização.
- Podem ser resolvidos eficientemente por solvers existentes (ex: programação linear inteira – ILP).

Nestes casos, métodos clássicos de otimização são mais adequados e eficientes.