# Phase 2: Autenticação - Context

**Gathered:** 2026-04-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Login JWT com três perfis (admin, professor, responsável) e rotas protegidas por papel. O sistema autentica usuários, redireciona para o dashboard correto conforme o perfil, e permite recuperação de senha por email. Cadastro de usuários, dashboards com dados reais e gestão de permissões são fases posteriores.

</domain>

<decisions>
## Implementation Decisions

### Login UX
- Layout split screen: lado esquerdo com nome do sistema + tagline em fundo colorido, lado direito com o formulário
- Toggle de visibilidade de senha (ícone de olho dentro do input)
- Validação on blur — cada campo valida quando o usuário sai dele
- Botão de login mostra spinner e fica desabilitado durante a requisição
- Mensagem de erro de autenticação: Claude decide (preferência por mensagem genérica por segurança)
- Posição do link "Esqueci minha senha": Claude decide

### Recuperação de Senha
- Fluxo: Claude decide (link por email é mais simples para protótipo)
- Após solicitar: confirmação direta — "Email enviado para xxx@xxx.com"
- Validade do token de recuperação: 24 horas
- Após redefinir senha com sucesso: login automático, redireciona para dashboard do perfil

### Armazenamento e Expiração de Token
- Storage: **localStorage** (mudança deliberada do sessionStorage original — com prazo longo, persistência entre abas faz sentido)
- Prazo do JWT: 7 dias (referência do usuário: 7–30 dias)
- Renovação: automática — cada requisição bem-sucedida estende o prazo
- Quando token expira ou 401 recebido: redirect silencioso para /login, limpando storage
- Tratamento de 401 no frontend: Claude decide (interceptor axios global)

### Roteamento por Perfil
- Destinos pós-login: Claude decide (provavelmente rotas distintas — /admin, /professor, /responsavel)
- Dashboard desta fase (Phase 2): placeholder com "Bem-vindo, [nome]!" — conteúdo real vem nas fases seguintes
- Acesso a rota de outro perfil por URL direta: redirect silencioso para o dashboard do próprio perfil
- Logout: menu dropdown do usuário (clica no nome/avatar, aparece opção "Sair")
- Layout base: Claude decide (provavelmente compartilhado, menu/links adaptados por perfil)
- Header logado: Nome + tipo de perfil — ex: "João Silva (Professor)"

### Claude's Discretion
- Mensagem exata de erro de credenciais inválidas
- Posicionamento do link "Esqueci minha senha"
- Fluxo exato de recuperação (link ou OTP)
- Rotas específicas por perfil (/admin, /professor, /responsavel ou variantes)
- Layout base compartilhado vs. layouts distintos por perfil
- Tratamento de 401 via interceptor axios
- Skeletons, spinners e estados de loading nas páginas internas

</decisions>

<specifics>
## Specific Ideas

- Token JWT com prazo de 7 dias (usuário considerou até 30 dias) — escolher 7 dias para protótipo, renovação automática cobre o resto
- Mudança de sessionStorage → localStorage foi decisão consciente: com prazo longo de sessão, perder o token ao fechar a aba é inconveniente sem ganho real de segurança para um protótipo
- Após redefinir senha: login automático (não redirecionar para /login e pedir que faça login novamente)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-autentica-o*
*Context gathered: 2026-04-26*
