from enum import Enum

class OperacaoER(Enum):
    UNIAO = "|"
    CONCAT = "."
    FECHO = "*"
    INTERROGACAO = "?"

__prioridade = {
    OperacaoER.UNIAO: 2,
    OperacaoER.CONCAT: 1,
    OperacaoER.FECHO: 0,
    OperacaoER.INTERROGACAO: 0
}


def prioridade(operacao):
    return __prioridade[operacao]