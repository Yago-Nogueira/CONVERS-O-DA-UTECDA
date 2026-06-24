# ✅ UTECDA PyQt6 Conversion Checklist

Use este checklist para acompanhar seu progresso na conversão de Tkinter para PyQt6.

---

## 📋 Fase 1: Preparação

- [x] Análise inicial do projeto
- [x] Identificação de 19 arquivos
- [x] Estratégia de conversão definida
- [x] Guias e scripts criados
- [ ] **Próximo:** Escolha sua opção (1, 2 ou 3)

---

## 🔄 Fase 2: Conversão Automática (Opcional)

Se escolheu Opção 1 ou Opção 3:

- [ ] Execute: `python CONVERT_TO_PYQT6.py`
- [ ] Verifique o relatório de conversão
- [ ] Revise os arquivos modificados
- [ ] **Próximo:** Fase 3

---

## 📖 Fase 3: Conversão Manual (Se necessário)

Se escolheu Opção 2 ou Opção 3:

### Leitura de Referência
- [ ] Leu PYQT6_CONVERSION_GUIDE.md
- [ ] Entendeu os padrões de conversão
- [ ] Revisou exemplos (Balloon_info.py, util.py)
- [ ] **Próximo:** Comece com arquivo 1

### Arquivo 1: UTECDA.py (PRIORIDADE ALTA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou class declaration (Frame → QWidget ou Toplevel → QDialog)
- [ ] Converteu pack/grid → layouts
- [ ] Converteu bind() → connect()
- [ ] Testou compilação (sem erros de import)
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 2: principal.py (PRIORIDADE ALTA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou class declaration
- [ ] Converteu pack/grid → layouts
- [ ] Converteu bind() → connect()
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 3: recon.py (PRIORIDADE ALTA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou class declaration
- [ ] Converteu pack/grid → layouts
- [ ] Converteu bind() → connect()
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 4: EntryBox.py (PRIORIDADE MÉDIA)
- [ ] Abriu o arquivo
- [ ] Completou conversão começada
- [ ] Converteu EntryBox class
- [ ] Converteu EntryBoxTick class
- [ ] Converteu EntryBoxColorBar class
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 5: qtSimpleDialog.py (PRIORIDADE MÉDIA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou classes
- [ ] Converteu layouts
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 6: maskedentry.py (PRIORIDADE MÉDIA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou classe MaskedWidget
- [ ] Converteu métodos de validação
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 7: tkcalendar_Days.py (PRIORIDADE MÉDIA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou classe Calendar
- [ ] Converteu UI layout
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 8: comp_MAPA.py (PRIORIDADE BAIXA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou class declaration
- [ ] Converteu visualização
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 9: comp_GRADE_MAPA.py (PRIORIDADE BAIXA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou class declaration
- [ ] Converteu visualização
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

### Arquivo 10: ordena.py (PRIORIDADE BAIXA)
- [ ] Abriu o arquivo
- [ ] Converteu imports
- [ ] Atualizou função/classe
- [ ] Testou compilação
- [ ] Testou funcionalidade
- [ ] **Status:** ⏳ (Aguardando)

---

## 🧪 Fase 4: Testes

### Testes Unitários
- [ ] UTECDA.py compila sem erros
- [ ] principal.py compila sem erros
- [ ] recon.py compila sem erros
- [ ] Todos os outros arquivos compilam

### Testes de Integração
- [ ] Aplicação inicia sem erros
- [ ] Janela principal abre
- [ ] Todos os menus funcionam
- [ ] Todos os botões funcionam
- [ ] Todos os diálogos abrem

### Testes Funcionais
- [ ] Entrada de dados funciona
- [ ] Cálculos funcionam corretamente
- [ ] Gráficos renderizam
- [ ] Exportação de dados funciona
- [ ] Importação de dados funciona

### Testes de Interface
- [ ] Campos de texto aceitam entrada
- [ ] Botões respondem ao clique
- [ ] Seleção de arquivo funciona
- [ ] Mensagens de erro mostram corretamente
- [ ] Fechamento da janela funciona

---

## 🔍 Fase 5: Validação Final

### Verificação de Imports
- [ ] Nenhum import de `qt_ui` permanece
- [ ] Nenhum import de `tk` permanece
- [ ] Todos os imports PyQt6 funcionam
- [ ] Nenhuma classe Tkinter referenciada

### Verificação de Código
- [ ] Nenhum `.bind()` sem converter
- [ ] Nenhum `.pack()` sem converter
- [ ] Nenhum `.grid()` sem converter
- [ ] Nenhum `.StringVar()` permanece
- [ ] Nenhum `.IntVar()` permanece
- [ ] Nenhum `.BooleanVar()` permanece

### Verificação de Funcionalidade
- [ ] Cálculos IGRF corretos
- [ ] Análise de ionosfera funcionando
- [ ] Visualizações de mapa corretas
- [ ] Relatórios gerados corretamente
- [ ] Exportações funcionando

---

## ✨ Fase 6: Conclusão

### Limpeza
- [ ] Remover pasta `qt_ui/` (se não mais necessária)
- [ ] Remover `CONVERT_TO_PYQT6.py` (opcional)
- [ ] Atualizar documentação do projeto

### Documentação
- [ ] README atualizado para PyQt6
- [ ] Dependências listadas corretamente
- [ ] Instruções de instalação claras

### Deployment
- [ ] Build final testado
- [ ] Versão incrementada
- [ ] Teste em máquina limpa
- [ ] Pronto para produção

---

## 📊 Progresso Geral

```
Fase 1: Preparação                 ✅ 100%
Fase 2: Conversão Automática       ⏳  0% (Opcional)
Fase 3: Conversão Manual           ⏳  0%
Fase 4: Testes                     ⏳  0%
Fase 5: Validação Final            ⏳  0%
Fase 6: Conclusão                  ⏳  0%

════════════════════════════════════════
Total:                             ✅ 17%
════════════════════════════════════════
```

---

## 📝 Notas de Conversão

### Problemas Encontrados:
```
(Adicionar aqui conforme encontrar)
```

### Soluções Aplicadas:
```
(Adicionar aqui conforme resolver)
```

### Mudanças Específicas:
```
(Notas sobre mudanças específicas por arquivo)
```

---

## 🆘 Suporte Rápido

| Problema | Solução |
|----------|---------|
| "ModuleNotFoundError: No module named 'qt_ui'" | Remova `import qt_ui` ou substitua por PyQt6 |
| "Class X has no method Y" | Verifique a sintaxe PyQt6 correspondente |
| "Widget not visible" | Verifique se setLayout() foi chamado |
| Layout não responde | Use QVBoxLayout/QHBoxLayout corretamente |

---

## ⏱️ Cronograma Estimado

| Fase | Duração Estimada | Status |
|------|------------------|--------|
| Fase 1: Preparação | ✅ Completo | ✅ |
| Fase 2: Conversão Automática | 5 minutos | ⏳ |
| Fase 3: Conversão Manual | 2-4 horas | ⏳ |
| Fase 4: Testes | 1-2 horas | ⏳ |
| Fase 5: Validação | 30-60 min | ⏳ |
| Fase 6: Conclusão | 30 min | ⏳ |
| **Total** | **4-7 horas** | ⏳ |

---

## 🎯 Objetivo Final

Ao completar este checklist:

✅ 100% dos imports de Tkinter/qt_ui removidos
✅ 100% das classes convertidas para PyQt6
✅ 100% dos layouts atualizados
✅ 100% dos eventos adaptados
✅ 100% dos testes passando
✅ 100% da funcionalidade preservada

---

## 📞 Próximo Passo

Escolha uma ação abaixo:

**Rápido:** `python CONVERT_TO_PYQT6.py`

**Completo:** Leia `PYQT6_CONVERSION_GUIDE.md`

**Balanceado:** Ambos!

---

**Status Atual:** 🟡 Aguardando ação do desenvolvedor

Comece agora! ⚡
