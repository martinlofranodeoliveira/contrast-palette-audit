<!-- public-docs-pt:v1 -->
# Auditoria de contraste de cores

Verifica pares opacos de cores sRGB, calcula contraste e relata os limiares de texto AA/AAA. Não certifica a acessibilidade completa de um site.

**Estado:** edição pública de desenvolvimento. Recursos e limites detalhados estão na referência técnica preservada abaixo.

## Começar em português

**Requisitos:** Python 3.11+; biblioteca padrão.

```sh
git clone https://github.com/martinlofranodeoliveira/contrast-palette-audit.git
cd contrast-palette-audit
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/contrast-palette-audit --help
```

Use um ambiente de desenvolvimento separado. Não envie `.env`, chaves, bancos,
uploads ou dados pessoais ao Git. Nas demonstrações, use somente dados fictícios.

## Documentação e validação

[Licença](LICENSE) · [Catálogo do laboratório](https://github.com/martinlofranodeoliveira#projetos-abertos)

Os comandos acima foram conferidos nos manifests/guia público; não significam que todas as integrações, plataformas ou serviços reais foram exercitados nesta revisão documental.

A referência técnica original abaixo preserva APIs, exemplos, limites e histórico
de funcionalidades. Auxiliares em `community/` são módulos independentes: sua
existência não comprova integração na interface ou no fluxo principal. Ao avaliar
uma funcionalidade, consulte também o teste e o código do módulo correspondente.

## Contribuir

Abra uma issue com objetivo, comportamento observado, versão e um exemplo mínimo
sintético. Para código, inclua testes relevantes, instruções de reprodução e
atualização da documentação. Não envie segredos ou informações de terceiros em
issues, exemplos, capturas ou pull requests. Mudanças úteis e completas têm
preferência sobre alterações feitas apenas para aumentar atividade.

## Licença e autoria

Licença declarada no repositório: **MIT**. Consulte o arquivo de licença e mantenha as atribuições de terceiros.

Nome técnico e URL preservados para manter imports, links e automações existentes.
Título, descrição e tópicos em português facilitam localizar a finalidade do projeto.

<!-- public-docs-pt:end -->

---

## Referência técnica e documentação original

# contrast-palette-audit

Audit explicit foreground/background design-token pairs offline. This small MIT
library and JSON CLI help catch text contrast regressions before a design system
is released. Python 3.11+, standard library only. No browser, telemetry or network.

## Use

From the checkout: `PYTHONPATH=src python3 -m contrast_palette_audit < pairs.json`.
Install with `python3 -m pip install .` and run `contrast-palette-audit pairs.json`.
The command accepts one regular UTF-8 JSON file or `-` (the default) for stdin.
Symlinks, directories and FIFOs are refused. Inputs are limited to 1 MiB, duplicate
JSON object keys and nonfinite numbers are rejected. No input file is modified.
Exit codes: 0 all pairs meet AA for normal text, 1 at least one fails, 2 invalid
input/arguments. Error messages are fixed codes and never include input values.

```json
{"pairs":[{"id":"body","foreground":"#000","background":"#fff"}]}
```

Python: `from contrast_palette_audit import analyze; report = analyze(payload)`.

## Exact API contract

`analyze(payload)` is pure and preserves its input. Accept only a built-in dict
with exactly `pairs`, a built-in list of 0..512 entries. Each entry is a built-in
dict with exactly `id`, `foreground`, `background`. IDs are unique strings of
1..80 printable ASCII characters (U+0020..U+007E). Colors are strings in exactly
`#RGB` or `#RRGGBB` form, ASCII hexadecimal, case insensitive; no whitespace,
alpha, CSS names, variables or implicit compositing. Invalid inputs raise
`ValueError("INPUT_INVALID")`, never return partial reports or echo values.

Expand shorthand digits, divide channels by 255. For each channel c, linearize
with c/12.92 if c<=0.04045, otherwise ((c+0.055)/1.055)**2.4. Relative luminance
is 0.2126*R+0.7152*G+0.0722*B. Contrast is (max(L1,L2)+0.05)/(min(L1,L2)+0.05).
Compare the unrounded ratio to each threshold. Only the reported ratio is rounded
with Python `round(ratio, 6)`; never round a passing threshold upward.

Return exactly:
`{"valid":bool,"pairs":[{"id":str,"ratio":number,"aa":bool,"aa_large":bool,"aaa":bool,"aaa_large":bool}],"summary":{"total":int,"aa_pass":int,"aaa_pass":int}}`.
Preserve input pair order. AA normal text is >=4.5, AA large text >=3,
AAA normal text >=7 and AAA large text >=4.5. `valid` means all normal-text AA
checks passed (including an empty batch). Summary counts are for normal text.
For the example above ratio is 21.0, all flags true and both pass counts are 1.

Formula and thresholds: [W3C relative luminance](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance),
[contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html),
[enhanced contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html).
This implementation checks explicitly supplied opaque sRGB pairs. It does not
inspect CSS, font size, rendered pixels, transparency, images or page semantics,
and it cannot establish whole-site WCAG conformance. The caller decides whether
the large-text criterion applies. No AI or external service is needed at runtime.

## Development

Run `python3 scripts/checks-offline.py` on Linux with Bubblewrap installed. Source
and tests are read-only, home/credentials are absent, network is isolated, effective
capabilities are zero, and source hashes are compared after the checks. The CI
root bootstrap is limited to a disposable GitHub-hosted runner; do not run local
tests with sudo. Original controller acceptance is independent of model tests.

AI-assisted implementation, reviewed through public and independent tests. MIT;
copyright 2026 Martin Lofrano. Bug reports and useful improvements are welcome.
